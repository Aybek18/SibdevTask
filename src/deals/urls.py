from django.urls import path

from deals.views import DealCreateAPIView

urlpatterns = [path("", DealCreateAPIView.as_view(), name="deals-create")]
