from django.urls import path
from .views import RegisterApiView, VerifyEmailView
urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name="verify-email")
]
