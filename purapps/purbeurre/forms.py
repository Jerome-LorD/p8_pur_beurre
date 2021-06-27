from django import forms


class SearchProduct(forms.Form):
    product_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control me-2",
                "placeholder": "Produit",
            }
        ),
    )


# class AuthorCreateView(CreateView):
#     model = Author
#     fields = ['name']
