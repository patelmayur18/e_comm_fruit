from django.contrib.auth import get_user_model
from django import forms
from .models import Address

User = get_user_model()




class CheckoutForm(forms.Form):
    shipping_address_line_1 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Address Line 01*'
        }))
    shipping_address_line_2 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Address Line 02*'
        }))
    shipping_zip_code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Zip Code'
        }))
    shipping_city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City'
        }))
    shipping_mobile_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mobile Number'
        }))

    billing_address_line_1 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Address Line 01*'
        }))
    billing_address_line_2 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Address Line 02*'
        }))
    billing_zip_code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Zip Code'
        }))
    billing_city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City'
        }))
    billing_mobile_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mobile Number'
        }))

    selected_shipping_address = forms.ModelChoiceField(Address.objects.none(),
                                                       required=False)
    selected_billing_address = forms.ModelChoiceField(Address.objects.none(),
                                                      required=False)

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        
        super().__init__(*args, **kwargs)

        user = User.objects.get(id=user_id)
        
        shipping_address_qs = Address.objects.filter(user=user,
                                                     address_type='s')
        billing_address_qs = Address.objects.filter(user=user,
                                                    address_type='b')
        print(shipping_address_qs)
        self.fields['selected_shipping_address'].queryset = shipping_address_qs
        self.fields['selected_billing_address'].queryset = billing_address_qs

    def clean(self):
        data = self.cleaned_data

        selected_shipping_address = data.get('selected_shipping_address', None)
        if selected_shipping_address is None:
            if not data.get('shipping_address_line_1', None):
                self.add_error("shipping_address_line_1",
                               "Please fill in this field")
            if not data.get('shipping_address_line_2', None):
                self.add_error("shipping_address_line_2",
                               "Please fill in this field")
            if not data.get('shipping_zip_code', None):
                self.add_error("shipping_zip_code",
                               "Please fill in this field")
            if not data.get('shipping_city', None):
                self.add_error("shipping_city", "Please fill in this field")
            if not data.get('shipping_mobile_number', None):
                self.add_error("shipping_mobile_number",
                               "Please fill in this field")

        selected_billing_address = data.get('selected_billing_address', None)
        if selected_billing_address is None:
            if not data.get('billing_address_line_1', None):
                self.add_error("billing_address_line_1",
                               "Please fill in this field")
            if not data.get('billing_address_line_2', None):
                self.add_error("billing_address_line_2",
                               "Please fill in this field")
            if not data.get('billing_zip_code', None):
                self.add_error("billing_zip_code", "Please fill in this field")
            if not data.get('billing_city', None):
                self.add_error("billing_city", "Please fill in this field")
            if not data.get('billing_mobile_number', None):
                self.add_error("billing_mobile_number",
                               "Please fill in this field")