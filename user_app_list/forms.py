from django import forms
from django.utils.translation import ugettext as _


class SearchForm(forms.Form):
    first_name = forms.CharField(label=_(u'First name'), required=False)
    last_name = forms.CharField(label=_(u"Last name"), required=False)
    phone = forms.IntegerField(label=_(u"Phone"), required=False)
    address = forms.CharField(label=_(u"Address"), required=False)
