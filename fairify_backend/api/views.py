import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.conf import settings
from .utils.convert import convert_to_jsonl

class FileConversionAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file was uploaded."}, status=400)
        temp_path = os.path.join(settings.MEDIA_ROOT, file.name)
        with open(temp_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        try:
            converted_data = convert_to_jsonl(temp_path)

            os.remove(temp_path)

            return Response({"converted_data": converted_data}, status=200)
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return Response({"error": str(e)}, status=500)
