from .models import Listing, Bid,Comment
from django.forms import ModelForm

class ListingFrom(ModelForm):
    class Meta:
        model = Listing
        fields = ["name", "description", "price", "image", "category"]

class BidForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["amount"].widget.attrs["class"] = "form-control"
    
    class Meta:
        model = Bid
        fields = ["amount"]

class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["comment"].widget.attrs["class"] ="form-control"

    class Meta:
        model = Comment
        fields =["comment"]