from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.AuthAPIView.as_view()),
    path('<str:username>/', views.UserDetailAPIView.as_view()),
    path('<str:username>/status/', views.UserStatusAPIView.as_view()),
    path('register/', views.RegisterAPIView.as_view()),
    path('jwt/', obtain_jwt_token),
    path('jwt/refresh/', refresh_jwt_token),
]
