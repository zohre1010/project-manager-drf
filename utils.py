from django.contrib.auth.mixins import UserPassesTestMixin
from kavenegar import *


def send_otp_code(phone_number, otp):
	try:
		api = KavenegarAPI('')
		params = {
			'sender': '',
			'receptor': phone_number,
			'message': f'{otp} کد تایید شما '
		}
		response = api.sms_send(params)
		print(response)
	except APIException as e:
		print(e)
	except HTTPException as e:
		print(e)

