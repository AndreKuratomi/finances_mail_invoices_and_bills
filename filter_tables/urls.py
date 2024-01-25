from django.urls import path
from .views import EmailAttachByTable

urlpatterns = [
    # path('email/', EmailAttachByTable.as_view())
    path('data/', EmailAttachByTable.as_view())
]