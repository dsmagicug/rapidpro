from smartmin.views import SmartFormView

from django import forms
from django.utils.translation import ugettext_lazy as _

from temba.utils.fields import ExternalURLField
from temba.utils.uuid import uuid4

from ...models import Channel
from ...views import ALL_COUNTRIES, ClaimViewMixin


class ClaimView(ClaimViewMixin, SmartFormView):
	class USSDClaimForm(ClaimViewMixin.Form):
		number = forms.CharField(
			max_length=14,
			min_length=1,
			label=_("Number"),
			help_text=_("The USSD service code you are connecting"),
		)
		country = forms.ChoiceField(
			choices=ALL_COUNTRIES, label=_("Country"), help_text=_("The country this phone number is used in")
		)

		start_message = forms.CharField(
			max_length=64,
			required=False,
			help_text=_(
				"Optional message to send to rapidPro at session start"
			),
		)

		timeout = forms.IntegerField(
			initial=30,
			required=False,
			label=_("USSD Request Time out"),
			help_text=_("USSD Request Response time out in seconds. Default is 30 seconds"),
		)
		strip_prefix = forms.BooleanField(
			initial=False,
			required=False,
			label=_("Strip USSD Prefix in request"),
			help_text=_("Use only if USSD gateway concatenates responses to subsequent requests "),
		)

	form_class = USSDClaimForm

	def form_valid(self, form):
		org = self.request.user.get_org()
		data = form.cleaned_data

		timeout = data.get("timeout", 30)
		strip_prefix = data.get("strip_prefix", False)
		number = data["number"]
		start_message = data["start_message"]
		country = data["country"]

		role = Channel.ROLE_SEND + Channel.ROLE_RECEIVE

		config = {

			Channel.CONFIG_USSD_START_MSG_KEY: start_message,
			Channel.CONFIG_USSD_TIMEOUT_KEY: timeout,
			Channel.CONFIG_USSD_STRIP_PREFIX_KEY: strip_prefix,
			Channel.CONFIG_CALLBACK_DOMAIN: org.get_brand_domain(),
		}
		self.object = Channel.add_config_external_channel(
			org, self.request.user, country, number, "US", config, role=role, parent=None
		)

		config = self.object.config

		self.object.config = config
		self.object.save()

		return super().form_valid(form)
