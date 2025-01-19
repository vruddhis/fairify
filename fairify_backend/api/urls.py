from django.urls import path
from .views import FileConversionAPIView
from .views import LoadModelAPIView, EvaluateModelAPIView

from . import views

urlpatterns = [
    path('convert/', FileConversionAPIView.as_view(), name='file-conversion'),
    path('load_model/', LoadModelAPIView.as_view(), name='load-model'),
     #path('load_external_model/', views.LoadExternalModelAPIView.as_view(), name='load_external_model'),
     path('evaluate_model/', EvaluateModelAPIView.as_view(), name='evaluate_model'),
]
