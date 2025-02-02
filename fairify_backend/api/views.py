import os
import json
import csv
import io
import errno
from uuid import uuid4
from django.core.files.storage import default_storage
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
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
from .utils.csv_to_sets import load_word_sets_from_csv
from .utils.weat import compute_weat_effect
from transformers import AutoTokenizer, AutoModel
from .models import ModelRegistry
from django.core.files.base import ContentFile
from seat_custom.custom_seat import get_attribute_words

class UploadCsvAndSetSeatsAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser) 

    def post(self, request, *args, **kwargs):
        try:
            csv_file = request.FILES.get('file')
            seat_number = int(request.data.get('number'))

            if not csv_file:
                return Response({"error": "CSV file is required."}, status=400)
            
            if seat_number not in [1, 2, 3, 4]:
                return Response({"error": "Seat number must be between 1 and 4."}, status=400)
            csv_data = csv_file.read().decode('utf-8')
            csv_reader = csv.reader(io.StringIO(csv_data))
            data_list = [row[0] for row in csv_reader]
            if seat_number == 1:
                DatasetRegistry.set_seat1(data_list)
            elif seat_number == 2:
                DatasetRegistry.set_seat2(data_list)
            elif seat_number == 3:
                DatasetRegistry.set_seat3(data_list)
            elif seat_number == 4:
                DatasetRegistry.set_seat4(data_list)

            return Response({
                "message": f"Seat data for Seat{seat_number} uploaded successfully.",
                "number_of_entries": len(data_list)
            }, status=200)

        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=500)

class MakeDatasetAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            seat1_data = DatasetRegistry.get_seat1()  
            seat2_data = DatasetRegistry.get_seat2()  
            seat3_data = DatasetRegistry.get_seat3()  
            seat4_data = DatasetRegistry.get_seat4()  

            max_length = max(len(seat1_data), len(seat2_data), len(seat3_data), len(seat4_data))

        
            def pad_list(lst, length):
                return lst + [""] * (length - len(lst))

            seat1_data = pad_list(seat1_data, max_length)
            seat2_data = pad_list(seat2_data, max_length)
            seat3_data = pad_list(seat3_data, max_length)
            seat4_data = pad_list(seat4_data, max_length)

            csv_filename = "seat_dataset.csv"
            csv_filepath = os.path.join(default_storage.location, csv_filename)  

            with open(csv_filepath, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Seat1", "Seat2", "Seat3", "Seat4"]) 
                for row in zip(seat1_data, seat2_data, seat3_data, seat4_data):
                    writer.writerow(row)

            DatasetRegistry.set_seat_dataset(csv_filepath)

            return Response({"message": "Dataset created and stored successfully.", "csv_filename": csv_filename}, status=200)

        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=500)

SEAT_FUNCTIONS = {
    1: DatasetRegistry.set_seat1,
    2: DatasetRegistry.set_seat2,
    3: DatasetRegistry.set_seat3,
    4: DatasetRegistry.set_seat4
}

class GetRelatedWordsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            print(request.data)
            category = request.data.get("word")
            top_n = request.data.get("number")

            
            if not category or top_n is None:
                return Response({"error": "Invalid input. Provide a valid word and a number (1-4)."}, status=400)
            top_n = int(top_n)
            related_words = get_attribute_words(category, top_n)
            SEAT_FUNCTIONS[top_n](related_words)

            return Response(related_words, status=200)

        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=500)

class ComputeWEATAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            dataset_path = DatasetRegistry.get_seat_dataset()
            print("dataset path is", dataset_path)
            if not dataset_path:
                return Response({"error": "No dataset found in DatasetRegistry."}, status=400)
            
            try:
                target_1, target_2, attr_1, attr_2, headings = load_word_sets_from_csv(dataset_path)
            except Exception as e:
                return Response({"error": f"Error processing CSV: {str(e)}"}, status=500)

    
            model_name = ModelRegistry.model_name
            if not model_name:
                return Response({"error": "Model name is not set. Please load a model first."}, status=400)

            try:
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModel.from_pretrained(model_name, output_hidden_states=True)
            except Exception as e:
                return Response({"error": f"Error loading model {model_name}: {str(e)}"}, status=500)

            try:
                effect_size = compute_weat_effect(target_1, target_2, attr_1, attr_2, tokenizer, model)
                print(effect_size)
                DatasetRegistry.set_seat_results(effect_size)
                return Response({
                    "message": "WEAT computation completed successfully.",
                    
                    "headings": headings
                }, status=200)
            except Exception as e:
                return Response({"error": f"Error during WEAT computation: {str(e)}"}, status=500)

        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=500)
    
class WEATScoreAPIView(APIView):
    @classmethod
    def get_seat_results(cls):
        seat_results = DatasetRegistry.get_seat_results()  
        if seat_results is None:
            raise ValueError("No SEAT results are set.")
        return seat_results

    def get(self, request, *args, **kwargs):
        try:
            seat_results = self.get_seat_results()
            return Response({"seat_results": seat_results}, status=200)
        
        except ValueError as ve:
            return Response({"error": str(ve)}, status=400)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

        
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
                "message": "Augmented dataset created successfully."
            }, status=200)

        except Exception as e:
            if isinstance(e, OSError) and e.errno == errno.EPIPE:
                print("Broken pipe error ignored")
            else:
                print(f"Error occurred: {e}")  
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    print(f"Temp file removed due to error: {temp_path}")
                return Response({"error": str(e)}, status=500)



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

            ModelRegistry.set_model(model, model_evaluator, aggregator, model_name)

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
            model_name = model.model_name if hasattr(model, 'model_name') else "GPT 2"
            aug_ds = DatasetRegistry.get_dataset()
            s = aug_ds.samples
            print("this is happening")
            results = countergen.evaluate_and_print(aug_ds.samples, model_evaluator, aggregator) #aggregate of the performance of each variation in each sample
            
            buf = io.BytesIO()
            aggregator.display({model_name: results})  
            plt.savefig(buf, format='png') 
            buf.seek(0)  


            filename = 'plots/evaluation_plot.png'
            file_path = default_storage.save(filename, buf)
            
            image_url = f'{settings.MEDIA_URL}{filename}'
            DatasetRegistry.set_image(image_url)
            return Response({
                "message": "Evaluation completed successfully.",
                "plot_url": image_url
            }, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class GetGraphURLAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            image_url = DatasetRegistry.get_image()
            return Response({"image_url": image_url}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

import pandas as pd

class UploadDatasetAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded."}, status=400)

        try:
            file_name = "uploaded_dataset.csv"
            
            file_path = os.path.join(default_storage.location, file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with default_storage.open(file_path, 'wb') as f:
                f.write(file.read())

            df = pd.read_csv(file_path)
            if len(df.columns) != 4:
                return Response({"error": "Invalid CSV format. There must be exactly 4 columns"}, status=400)
            DatasetRegistry.set_seat_dataset(file_path)
            return Response({"message": "Dataset uploaded and registered successfully."}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        
"""class LoadExternalModelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        model_name = request.data.get("model_name")
        api_key = request.data.get("api_key")  
        api_base_url = request.data.get("api_base_url")  

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