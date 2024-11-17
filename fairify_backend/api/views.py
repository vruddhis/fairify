import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.conf import settings
from .utils.convert import convert_to_augmented_csv

class FileConversionAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        swap_gender = request.data.get('swap_gender', 'false').lower() == 'true'

        if not file:
            return Response({"error": "No file was uploaded."}, status=400)
        temp_path = os.path.join(settings.MEDIA_ROOT, file.name)
        with open(temp_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        try:

            augmented_data = convert_to_augmented_csv(temp_path, swap_gender=swap_gender)
            os.remove(temp_path)

            return Response({"augmented_data": augmented_data}, status=200)
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return Response({"error": str(e)}, status=500)
