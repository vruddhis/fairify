import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.conf import settings
from .utils.convert import convert_to_augmented_csv
import torch
from transformers import GPT2LMHeadModel
from countergenedit import get_generative_model_evaluator, pt_to_generative_model
from countergenedit.tools.utils import get_device
from countergen import aggregators

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


from .models import ModelRegistry

class LoadModelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        model_name = request.data.get("model_name")
        if not model_name:
            return Response({"error": "Model name is required."}, status=400)

        try:
            device = get_device()
            model = GPT2LMHeadModel.from_pretrained(model_name).to(device)
            model_evaluator = get_generative_model_evaluator(
                pt_to_generative_model(model), "probability"
            )

            aggregator = aggregators.PerformanceStatsPerCategory()

            ModelRegistry.set_model(model, model_evaluator, aggregator)

            return Response({
                "message": f"Model '{model_name}' loaded and stored successfully.",
                "aggregator": "PerformanceStatsPerCategory ready"
            }, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

