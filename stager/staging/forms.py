from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from stager.staging.models import *

def validate_file_size(self, file_field):
    content = self.cleaned_data[file_field]
    if content and content._size > settings.MAX_UPLOAD_SIZE:
        raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
    return content

class LinkSizeAdminForm(forms.ModelForm):
    class Meta:
        model = Link

    def clean_file_link(self):
        return validate_file_size(self, 'file_link')

class CompSizeAdminForm(forms.ModelForm):
    class Meta:
        model = Comp

    def clean_background(self):
        return validate_file_size(self, 'background')

class SlideSizeAdminForm(forms.ModelForm):
    class Meta:
        model = Comp

    def clean_backgroundfield(self):
        return validate_file_size(self, 'backgroundfield')

    def clean_image(self):
        return validate_file_size(self, 'image')

class ClientLogoSizeAdminForm(forms.ModelForm):
    class Meta:
        model = Client

    def clean_logo(self):
        return validate_file_size(self, 'logo')
