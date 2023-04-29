from django.urls import path
from .views import AdListView, AdCreateView, AdDetailView, AdUpdateView, AdDestroyView, AdImageView

urlpatterns = [
    path('', AdListView.as_view()),
    path('<int:pk>/', AdDetailView.as_view()),
    path('create/', AdCreateView.as_view()),
    path('<int:pk>/update/', AdUpdateView.as_view()),
    path('<int:pk>/delete/', AdDestroyView.as_view()),
    path('<int:pk>/upload_image/', AdImageView.as_view()),
]
