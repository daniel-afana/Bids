from django.conf.urls import url, include
from rest_framework import routers
from bids_app import views

router = routers.DefaultRouter()
router.register(r'channels', views.ChannelViewSet)
router.register(r'campaigns', views.CampaignViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
