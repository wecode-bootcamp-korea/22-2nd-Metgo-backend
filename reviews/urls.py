from django.urls import path
from .views      import MasterReviewView

urlpatterns = [
    path('/<int:master_id>', MasterReviewView.as_view())
]

