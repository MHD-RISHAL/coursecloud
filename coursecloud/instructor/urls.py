from django.urls import path
from .views import *

urlpatterns=[
    path('instructor',InstructorRegview.as_view(),name='instructor')
    
]