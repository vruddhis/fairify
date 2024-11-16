from django.urls import path
from .views import FileConversionAPIView

urlpatterns = [
    path('convert/', FileConversionAPIView.as_view(), name='file-conversion'),
]
