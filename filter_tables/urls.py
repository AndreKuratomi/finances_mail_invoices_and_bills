from django.urls import path
from .views import SendEmailView

urlpatterns = [
    path('email/', SendEmailView.as_view())
]