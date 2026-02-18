from django.urls import path
from portal.views import NewsPostCreateView, PortalUserCheckAPIView

urlpatterns = [
    path('create-news/', NewsPostCreateView.as_view()),
    path('check-username/', PortalUserCheckAPIView.as_view()),
]
