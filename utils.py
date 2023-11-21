from django.contrib.auth.mixins import UserPassesTestMixin
from kavenegar import *


def send_otp_code(phone_number,code):
    try:
        api = KavenegarAPI('554B5A4138556E577530697257525246757A48314B7956495131396752684A54382B6F455361335666576B3D')
        params = {
            'sender': '',  # optional
            'receptor': '09165597588',  # multiple mobile number, split by comma
            'message': code,
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)

class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin