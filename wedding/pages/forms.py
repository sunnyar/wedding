from django import forms
from .models import Page
from .models import Address, Rsvp, PhotoContent
from .models import Wedding, Contact, Theme
from tinymce.widgets import TinyMCE
from photologue.models import Photo
from localflavor.in_.forms import INStateSelect, INPhoneNumberField
from django.forms.extras.widgets import SelectDateWidget
from datetime import date
from calendar import monthrange
from audiofield.models import AudioFile
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class WeddingForm(forms.ModelForm) :

    #user_domain = forms.CharField(help_text='Choose your domain(e.g: karan-shruti, karan-and-shruti, karan-&-shruti)')
    class Meta :
        model = Wedding
        exclude = ('user',)
        widgets = {
                    'location' : INStateSelect(),
                    'wedding_date': SelectDateWidget(years=range(2014, 2021)),
        }


class PageForm(forms.ModelForm):

    body = forms.CharField(widget=SummernoteWidget(attrs={'width': '100%', 'height': '400px'}))
    class Meta:
        model = Page
        exclude = ("user", "slug", "created",)


class PhotoForm(forms.ModelForm):

    class Meta:
        model = PhotoContent
        fields = ('image', 'title', 'caption', 'crop_from', 'tags',)


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        widgets = {
            'street': forms.Textarea(attrs={'cols': 30, 'rows': 5}),
            'state' : INStateSelect(),
        }
        exclude = ("user",)


class RsvpForm(forms.ModelForm):

#    contact = INPhoneNumberField(label="Contact Number")
    class Meta:
        model = Rsvp
        widgets = {
#                    'connect': forms.RadioSelect,
                    'response': forms.RadioSelect
                }


class ContactForm(forms.ModelForm):

    phone_num = INPhoneNumberField(label="Phone Number")
    class Meta:
        model = Contact
        widgets = {
            'message': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }
        exclude = ('created',)


class ThemeForm(forms.ModelForm):

    class Meta :
        model = Theme
        widgets = {'name': forms.RadioSelect}
        exclude = ('user','member',)


class AudioFileForm(forms.ModelForm):

    class Meta:
        model = AudioFile
        fields = ('audio_file',)


class CreditCardField(forms.IntegerField):
    @staticmethod
    def get_cc_type(number):
        """
        Gets credit card type given number. Based on values from Wikipedia page
        "Credit card number".
        http://en.wikipedia.org/w/index.php?title=Credit_card_number
        """
        number = str(number)
        #group checking by ascending length of number
        if len(number) == 13:
            if number[0] == "4":
                return "Visa"
        elif len(number) == 14:
            if number[:2] == "36":
                return "MasterCard"
        elif len(number) == 15:
            if number[:2] in ("34", "37"):
                return "American Express"
        elif len(number) == 16:
            if number[:4] == "6011":
                return "Discover"
            if number[:2] in ("51", "52", "53", "54", "55"):
                return "MasterCard"
            if number[0] == "4":
                return "Visa"
        return "Unknown"

    def clean(self, value):
        """Check if given CC number is valid and one of the
           card types we accept"""
        if value and (len(value) < 13 or len(value) > 16):
            raise forms.ValidationError("Please enter in a valid "+\
                "credit card number.")
        elif self.get_cc_type(value) not in ("Visa", "MasterCard",
                                             "American Express"):
            raise forms.ValidationError("Please enter in a Visa, "+\
                "Master Card, or American Express credit card number.")
        return super(CreditCardField, self).clean(value)


class CCExpWidget(forms.MultiWidget):
    """ Widget containing two select boxes for selecting the month and year"""
    def decompress(self, value):
        return [value.month, value.year] if value else [None, None]

    def format_output(self, rendered_widgets):
        html = u' / '.join(rendered_widgets)
        return u'<span style="white-space: nowrap">%s</span>' % html


class CCExpField(forms.MultiValueField):
    EXP_MONTH = [(x, x) for x in xrange(1, 13)]
    EXP_YEAR = [(x, x) for x in xrange(date.today().year,
                                       date.today().year + 15)]
    default_error_messages = {
        'invalid_month': u'Enter a valid month.',
        'invalid_year': u'Enter a valid year.',
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        fields = (
            forms.ChoiceField(choices=self.EXP_MONTH,
                error_messages={'invalid': errors['invalid_month']}),
            forms.ChoiceField(choices=self.EXP_YEAR,
                error_messages={'invalid': errors['invalid_year']}),
        )
        super(CCExpField, self).__init__(fields, *args, **kwargs)
        self.widget = CCExpWidget(widgets =
            [fields[0].widget, fields[1].widget])

    def clean(self, value):
        exp = super(CCExpField, self).clean(value)
        if date.today() > exp:
            raise forms.ValidationError(
            "The expiration date you entered is in the past.")
        return exp

    def compress(self, data_list):
        if data_list:
            if data_list[1] in forms.fields.EMPTY_VALUES:
                error = self.error_messages['invalid_year']
                raise forms.ValidationError(error)
            if data_list[0] in forms.fields.EMPTY_VALUES:
                error = self.error_messages['invalid_month']
                raise forms.ValidationError(error)
            year = int(data_list[1])
            month = int(data_list[0])
            # find last day of the month
            day = monthrange(year, month)[1]
            return date(year, month, day)
        return None


class PaymentForm(forms.Form):
    number = CreditCardField(required = True, label = "Card Number")
    holder = forms.CharField(required = True, label = "Card Holder Name",
        max_length = 60)
    expiration = CCExpField(required = True, label = "Expiration")
    ccv_number = forms.IntegerField(required = True, label = "CCV Number",
        max_value = 9999, widget = forms.TextInput(attrs={'size': '4'}))

    def __init__(self, *args, **kwargs):
        self.payment_data = kwargs.pop('payment_data', None)
        super(PaymentForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned = super(PaymentForm, self).clean()
        if not self.errors:
            ## Enter the Payment Process code here
            pass
        return cleaned