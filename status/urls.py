from django.urls import path
from . import views

app_name = 'status'

urlpatterns = [
    path('', views.StatusAPIView.as_view()),
    path('create/', views.StatusCreateAPIView.as_view()),
    # path('<int:pk>/', views.StatusDetailsAPIView.as_view()),
    path('<int:id>/', views.StatusDetailsAPIView.as_view()),
    path('<int:id>/update/', views.StatusUpdateAPIView.as_view()),
    path('<int:id>/delete/', views.StatusDeleteAPIView.as_view())
]
