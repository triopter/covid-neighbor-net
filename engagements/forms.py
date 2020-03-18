from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


from neighbors.models import Role, NeighborProfile, Country, Address
from engagements.models import EngagementStatus, Engagement


class RequesterRegistrationForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea, label=_("I need help with..."))

    address_line_1 = forms.CharField(label=_("Address"))
    address_line_2 = forms.CharField(required=False, label=_("Address Line 2"))
    city = forms.CharField(label=_("City"))
    region = forms.CharField(label=_("State or Province"))
    postal_code = forms.CharField(label=_("Postal Code"))
    country = forms.ChoiceField(choices=Country.choices, label=_("Country"))

    given_name = forms.CharField(label=_("Given Name"))
    surname = forms.CharField(required=False, label=_("Surname (optional)"))
    email = forms.EmailField(label=_("Email"))
    phone = forms.CharField(
        required=False,
        label=_("Phone"),
        help_text=_("If you prefer to be contacted by phone, please enter your number here"),
    )
    password = forms.CharField(
        widget=forms.PasswordInput, label=_("Password")
    )  # Do we want to bother with a "confirm password" field?

    terms = forms.BooleanField(
        label=_("I agree to the terms and conditions")
    )  # I guess we need terms and conditions?

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label

    def save(self):
        User = get_user_model()

        # create User
        user = User.objects.create_user(
            self.cleaned_data['email'],
            self.cleaned_data['email'],
            self.cleaned_data['password'],
            **{
                'first_name': self.cleaned_data['given_name'],
                'last_name': self.cleaned_data['surname'],
            },
        )

        # create Neighbor
        neighbor = NeighborProfile.objects.create(
            **{
                'user': user,
                'given_name': self.cleaned_data['given_name'],
                'surname': self.cleaned_data['surname'],
                'email': self.cleaned_data['email'],
                'phone': self.cleaned_data['phone'],
            }
        )

        # Add Requester role

        # create Address
        address = Address.objects.create(
            **{
                'owner': neighbor,
                'address_line_1': self.cleaned_data['address_line_1'],
                'address_line_2': self.cleaned_data['address_line_2'],
                'city': self.cleaned_data['city'],
                'region': self.cleaned_data['region'],
                'postal_code': self.cleaned_data['postal_code'],
                'country': self.cleaned_data['country'],
            }
        )

        # create Engagement
        engagement = Engagement.objects.create(
            **{
                'requester': user,
                'address': address,
                'description': self.cleaned_data['description'],
                'status': EngagementStatus.REQUESTED,
            }
        )

        return engagement
