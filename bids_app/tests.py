from django.test import TestCase
from bids_app.models import Channel, Campaign
from bids_app.serializers import ChannelSerializer, CampaignSerializer
from rest_framework.test import APIClient, APIRequestFactory, APITestCase
from rest_framework.request import Request
from rest_framework import status
from django.core.urlresolvers import reverse
from bids_app.views import ChannelViewSet, CampaignViewSet
import pdb


class ModelTestCase(TestCase):
    
    """This class defines the test suite for the models."""

    def setUp(self):
        chan = Channel.objects.create(
            name="Test channel name",
            slug="Test channel slug",
            bid_types=(["CPM", "CPC"])
        )

        Campaign.objects.create(
            name="Test campaign name",
            channel=chan,
            bid = 1,
            bid_type = ("CPM")
        )
    
    def test_channel_obj_is_created(self):
        test_channel = Channel.objects.get(name="Test channel name")
        self.assertIsInstance(test_channel, Channel)

    def test_campaign_obj_is_created(self):
        test_campaign = Campaign.objects.get(name="Test campaign name")
        self.assertIsInstance(test_campaign, Campaign)


class APITestCaseTempl(APITestCase):

    client = APIClient()
    factory = APIRequestFactory()
    chan_pk = 1
    camp_pk = 1

    def setUp(self):

        self.chan1 = Channel.objects.create(
            name="Test channel name",
            slug="Test channel slug",
            bid_types=(["CPM", "CPC"])
        )

        self.chan_pk = self.chan1.pk

        Channel.objects.create(
            name="Test channel 2",
            slug="Test channel 2 slug",
            bid_types=(["CPI"])
        )

        camp1 = Campaign.objects.create(
            name="Test campaign name",
            channel=self.chan1,
            bid = 1,
            bid_type = ("CPM")
        )

        self.camp_pk = camp1.pk


class GetListTest(APITestCaseTempl):

    """ Channels and campaigns list """

    def test_get_all_channels(self):

        # get API response
        response = self.client.get(reverse('channel-list'))

        # get data from db
        channels = Channel.objects.all()

        request = self.factory.get('/')
        serializer_context = {
            'request': Request(request),
        }
        serializer = ChannelSerializer(instance=channels, context=serializer_context, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_campaigns(self):

        # get API response
        response = self.client.get(reverse('campaign-list'))

        # get data from db
        campaigns = Campaign.objects.all()

        request = self.factory.get('/')
        serializer_context = {
            'request': Request(request),
        }
        serializer = CampaignSerializer(instance=campaigns, context=serializer_context, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetDetailTest(APITestCaseTempl):

    """ Detail page for channel and campaign """

    def test_get_valid_single_channel(self):
        response = self.client.get(reverse('channel-detail', kwargs={'pk': self.chan_pk}))
        channel = Channel.objects.get(name="Test channel name")

        request = self.factory.get('/')
        serializer_context = {
            'request': Request(request),
        }
        serializer = ChannelSerializer(instance=channel, context=serializer_context)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_channel(self):
        response = self.client.get(
            reverse('channel-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_valid_single_campaign(self):
        response = self.client.get(reverse('campaign-detail', kwargs={'pk': self.camp_pk}))
        campaign = Campaign.objects.get(name="Test campaign name")

        request = self.factory.get('/')
        serializer_context = {
            'request': Request(request),
        }
        serializer = CampaignSerializer(instance=campaign, context=serializer_context)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_campaign(self):
        response = self.client.get(
            reverse('campaign-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateChannelListTestCase(APITestCaseTempl):

    def setUp(self):

        self.channel_data = {
            'name': 'Test channel 3',
            'slug':'Test channel slug 3',
            'bid_types':["CPC"]
            }

        self.response = self.client.post(
            reverse('channel-list'),
            self.channel_data,
            format="json")

    def test_can_create_a_channel_list(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


class CreateCampaignListTestCase(APITestCaseTempl):

    def test_can_create_a_campaign_list(self):

        campaign_data = {
            'name': 'Test campaign 3',
            'channel': '/channels/{}/'.format(self.chan1.pk),
            'bid': 3,
            'bid_type': "CPC"
            }
        
        response = self.client.post(
            reverse('campaign-list'),
            campaign_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdateChannelTestCase(APITestCaseTempl):

    def test_valid_update_channel(self):

        valid_info = {
            "name": "Updated name",
            "slug":"Updated slug",
            "bid_types": ["CPM"]
        }

        response = self.client.put(
            reverse('channel-detail', kwargs={'pk':self.chan_pk}),
            valid_info,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_update_channel(self):

        invalid_info = {
            'name': '',
            'slug':'invalid info slug',
            'bid_types': 'invalid bid type'
        }

        response = self.client.put(
            reverse('channel-detail', kwargs={'pk': self.chan_pk}),
            invalid_info,
            format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateCampaignTestCase(APITestCaseTempl):

    def test_valid_update_campaign(self):

        valid_campaign_data = {
            'name': 'Updated campaign name',
            'channel': '/channels/{}/'.format(self.chan_pk),
            'bid': 3,
            'bid_type':"CPM"
            }
        
        response = self.client.put(
            reverse('campaign-detail', kwargs={'pk': self.camp_pk}),
            valid_campaign_data,
            format="json"
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_update_campaign(self):

        invalid_info = {
            'name': 'Updated campaign name',
            'channel': '/channels/{}/'.format(self.chan_pk),
            'bid': 3,
            'bid_type':["CPZZ"]
        }

        response = self.client.put(
            reverse('campaign-detail', kwargs={'pk': self.camp_pk}),
            invalid_info,
            format="json"
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteChannelTestCase(APITestCaseTempl):

    def test_valid_delete_channel(self):

        response = self.client.delete(
            reverse('channel-detail', kwargs={'pk':self.chan_pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_invalid_delete_channel(self):

        response = self.client.delete(
            reverse('channel-detail', kwargs={'pk': 30})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteCampaignlTestCase(APITestCaseTempl):

    def test_valid_delete_campaign(self):

        response = self.client.delete(
            reverse('campaign-detail', kwargs={'pk':self.camp_pk})
        )
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_invalid_delete_campaign(self):

        response = self.client.delete(
            reverse('campaign-detail', kwargs={'pk': 30})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

   