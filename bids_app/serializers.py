from rest_framework import serializers
from bids_app.models import Channel, Campaign



class ChannelSerializer(serializers.HyperlinkedModelSerializer):

    bid_types = serializers.MultipleChoiceField(choices=Channel.BID_TYPES_CHOICES)

    class Meta:
        model = Channel
        fields = ('url', 'name', 'slug', 'bid_types')


class CampaignSerializer(serializers.HyperlinkedModelSerializer):

    channel = serializers.HyperlinkedRelatedField(view_name='channel-detail', queryset=Channel.objects.all())

    class Meta:
        model = Campaign
        fields = ('url', 'name', 'channel', 'bid', 'bid_type')