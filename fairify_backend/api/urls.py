from django.urls import path
from .views import FileConversionAPIView
from .views import LoadModelAPIView

urlpatterns = [
    path('convert/', FileConversionAPIView.as_view(), name='file-conversion'),
    path('load_model/', LoadModelAPIView.as_view(), name='load-model'),
]
