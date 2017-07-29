from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from bids_app.models import Channel, Campaign
# from snippets.permissions import IsOwnerOrReadOnly
from bids_app.serializers import ChannelSerializer, CampaignSerializer
# from rest_framework import permissions


class ChannelViewSet(viewsets.ModelViewSet):

    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save()
    
class CampaignViewSet(viewsets.ModelViewSet):

    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    def perform_create(self, serializer):
        serializer.save()