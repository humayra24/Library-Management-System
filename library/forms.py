from django import forms
from .models import Book, Author, Wishlist

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'category', 'author', 'image']

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.all()



class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['book']