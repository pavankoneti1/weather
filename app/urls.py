from django.urls import path
from .views import *
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('classView', forecast30DaysCls, basename='class forecast')

urlpatterns = [
    path('30days/', home),
    # path('', forecast30Days),
]