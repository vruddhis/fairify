import os
import json
from uuid import uuid4
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.conf import settings
from .utils.convert import convert_to_augmented_csv
from .utils.storage import save_augmented_dataset_to_file, load_augmented_dataset_from_file
import torch
from transformers import GPT2LMHeadModel
from countergenedit import get_generative_model_evaluator, pt_to_generative_model  #,api_to_generative_model
from countergenedit.tools.utils import get_device
from countergen import aggregators
from countergen.tools.api_utils import ApiConfig
from .dataset import DatasetRegistry
import countergen

class FileConversionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        swap_gender = request.data.get('swap_gender', 'false').lower() == 'true'

        if not file:
            return Response({"error": "No file was uploaded."}, status=400)
        print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
        print(f"Uploaded file name: {file.name}")


        if not os.path.exists(settings.MEDIA_ROOT):
            print("Media root directory does not exist. Creating it...")
            os.makedirs(settings.MEDIA_ROOT)
        else:
            print("Media root directory exists.")

        temp_path = os.path.join(settings.MEDIA_ROOT, file.name)
        
        
        print(f"Temp file path: {temp_path}")

        try:
           
            with open(temp_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            print(f"File saved successfully at {temp_path}")

      
            augmented_dataset, augmented_rows = convert_to_augmented_csv(temp_path, swap_gender=swap_gender)

         
            augmented_file_name = "augmented_dataset.jsonl"
            augmented_file_path = os.path.join(settings.MEDIA_ROOT, augmented_file_name)
            save_augmented_dataset_to_file(augmented_dataset, augmented_file_path)
            print(f"Augmented dataset saved successfully at {augmented_file_path}")
            augmented_file_url = f"{settings.MEDIA_URL}{augmented_file_name}"

            DatasetRegistry.set_dataset(augmented_dataset)
            print("Successfuly set dataset")



            os.remove(temp_path)
            print(f"Temp file removed: {temp_path}")

            return Response({
                "message": "Augmented dataset created successfully.",
                "augmented_file_url": request.build_absolute_uri(augmented_file_path),
                "augmented_file_name": augmented_file_name
            }, status=200)

        except Exception as e:
            print(f"Error occurred: {e}")  
            if os.path.exists(temp_path):
                os.remove(temp_path)
                print(f"Temp file removed due to error: {temp_path}")
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
        
class EvaluateModelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            model = ModelRegistry.get_model()
            model_evaluator = ModelRegistry.get_model_evaluator()
            aggregator = ModelRegistry.get_aggregator()
            model_name = model.name if hasattr(model, 'name') else "UnknownModel"
            aug_ds = DatasetRegistry.get_dataset()
            
            
            results = countergen.evaluate(aug_ds.samples, model_evaluator, aggregator)
            aggregator.display({model_name: results})  

            return Response({
                "message": "Evaluation completed successfully.",
                "results": results
            }, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


"""class LoadExternalModelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        model_name = request.data.get("model_name")
        api_key = request.data.get("api_key")  # API Key for external API
        api_base_url = request.data.get("api_base_url", "https://api.openai.com/v1")  # Default to OpenAI

        if not model_name or not api_key:
            return Response({"error": "Model name and API key are required."}, status=400)

        try:
            apiconfig = ApiConfig(api_key, api_base_url)
            model_ev = get_generative_model_evaluator(
                api_to_generative_model(model_name, apiconfig=apiconfig), "probability"
            )

            aggregator = aggregators.PerformanceStatsPerCategory()

            ModelRegistry.set_model(None, model_ev, aggregator)

            return Response({
                "message": f"Model '{model_name}' loaded from external API and stored successfully.",
                "aggregator": "PerformanceStatsPerCategory ready"
            }, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)"""