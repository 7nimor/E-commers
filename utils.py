from kavenegar import *


def send_otp_code(phone_number,code):
    api = KavenegarAPI('554B5A4138556E577530697257525246757A48314B7956495131396752684A54382B6F455361335666576B3D')
    params = {f'sender': '1000689696', 'receptor': {phone_number}, 'message': f'برگام جوجو کار کرد{code}'}
    response = api.sms_send(params)
