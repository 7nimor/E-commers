from django.forms import forms


class UploadObjBucket(forms.Form):
    upload_file = forms.FileField(max_length=200, allow_empty_file=False)
