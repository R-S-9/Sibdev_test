from django import forms

from .models import CustomerLog, PurchasedItems


class CustomerForm(forms.ModelForm):

    class Meta:
        model = CustomerLog
        fields = "__all__"


class PurchasedItemsForm(forms.ModelForm):

    file = forms.FileField(
        required=False,
    )

    class Meta:
        model = PurchasedItems
        fields = "__all__"


class UploadFileForm(forms.Form):
    file = forms.FileField()



