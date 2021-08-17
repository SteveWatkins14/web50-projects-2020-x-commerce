from django import forms
from .models import Bid, Comment, Listing
from .Constants import DEFAULT_NEW_LISTING_IMAGE_URL

class ListingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update({"class": "form-control", "id": "listing-title"})
        self.fields["discription"].widget.attrs.update({"class": "form-control", "id": "listing-discription", "rows": "2"})
        self.fields["price"].widget.attrs.update({"class": "form-control", "id": "listing-price"})
        self.fields["image_url"].widget.attrs.update({"class": "form-control", "id": "listing-image_url", "placeholder": "https://"})
        self.fields["category"].widget.attrs.update({"class": "form-control", "id": "listing-category"})

    def clean_image_url(self):
            image_url = self.cleaned_data['image_url']
            return image_url or DEFAULT_NEW_LISTING_IMAGE_URL
    
    class Meta:
            model = Listing
            exclude = (
                'owner',
                'active',
            )
            
class BidForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.listing = kwargs.pop("listing", None)
        super(BidForm, self).__init__(*args, **kwargs)

        self.fields["amount"].widget.attrs.update({"class": "form-control", "placeholder": "Enter Bid"})

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")

        if self.user == self.listing.owner:
            raise forms.ValidationError("Cannot bid on your own listing.")

        if amount <= self.listing.price:
            raise forms.ValidationError("Bid must be higher than the current price.")
        
        return amount

    class Meta:
        model = Bid
        exclude = (
            'user',
            'listing'
        )

    
class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        
        self.fields["text"].widget.attrs.update({"class": "form-control", "rows": "2"})

    class Meta:
        model = Comment
        exclude = (
            'user',
            'listing',
            'created'
        )
