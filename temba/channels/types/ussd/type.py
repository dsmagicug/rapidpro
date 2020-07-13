from django.utils.translation import ugettext_lazy as _

from temba.channels.types.ussd.views import ClaimView
from temba.contacts.models import TEL_SCHEME

from ...models import ChannelType


class USSDType(ChannelType):
	"""
	An USSD channel
	"""

	code = "US"
	category = ChannelType.Category.PHONE

	courier_url = r"^us/(?P<uuid>[a-z0-9\-]+)/(?P<action>status|receive)$"

	name = "USSD"
	icon = "icon-channel-ussd"

	claim_blurb = _(
		"""Connect your external USSD  instance, we'll walk you through
					   the steps necessary to get your USSD gateway connection working in a few minutes."""
	)
	claim_view = ClaimView

	schemes = [TEL_SCHEME]
	max_length = 182

	attachment_support = False
