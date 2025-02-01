from django.urls import path
from .views import FileConversionAPIView, ComputeWEATAPIView, WEATScoreAPIView, GetRelatedWordsAPIView, MakeDatasetAPIView
from .views import LoadModelAPIView, EvaluateModelAPIView, GetGraphURLAPIView, UploadDatasetAPIView, UploadCsvAndSetSeatsAPIView


from . import views

urlpatterns = [
    path('convert/', FileConversionAPIView.as_view(), name='file-conversion'),
    path('load_model/', LoadModelAPIView.as_view(), name='load-model'),
     #path('load_external_model/', views.LoadExternalModelAPIView.as_view(), name='load_external_model'),
    path('evaluate_model/', EvaluateModelAPIView.as_view(), name='evaluate_model'),
    path('get_graph_url/', GetGraphURLAPIView.as_view(), name='get_graph_url'),
    path('upload_dataset/', UploadDatasetAPIView.as_view(), name='upload_dataset'),
    path('compute_weat/', ComputeWEATAPIView.as_view(), name='compute_weat'),
    path('get_seat_score/', WEATScoreAPIView.as_view(), name='get_seat_score'),
    path('get_related_words/', GetRelatedWordsAPIView.as_view(), name = 'get_related_words' ),
    path('make_dataset/', MakeDatasetAPIView.as_view(), name = 'make_dataset'),
    path('seat_col_file/', UploadCsvAndSetSeatsAPIView.as_view(), name = 'seat_col_file'),
]
