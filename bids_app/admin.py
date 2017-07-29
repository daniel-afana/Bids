from django.contrib import admin
from bids_app.models import Channel, Campaign


class CampaignInline(admin.StackedInline):
    model = Campaign

class ChannelAdmin(admin.ModelAdmin):
    model = Channel
    inlines = [CampaignInline]


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Campaign)