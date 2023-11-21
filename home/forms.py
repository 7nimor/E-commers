from django import forms


class UploadObjBucket(forms.Form):
    upload_file = forms.CharField(max_length=1000)
