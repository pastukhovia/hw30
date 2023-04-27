from django.urls import path
from .views import AdListView, AdCreateView, AdDetailView, update_ad, delete_ad, AdImageView

urlpatterns = [
    path('', AdListView.as_view()),
    path('<int:pk>/', AdDetailView.as_view()),
    path('create/', AdCreateView.as_view()),
    path('<int:pk>/update/', update_ad),
    path('<int:pk>/delete/', delete_ad),
    path('<int:pk>/upload_image/', AdImageView.as_view()),
]
