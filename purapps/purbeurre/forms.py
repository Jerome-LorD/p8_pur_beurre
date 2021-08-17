"""Purbeurre forms module."""
from django import forms


class SearchProduct(forms.Form):
    """Search product."""

    product_name = forms.CharField(
        label="",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control me-2",
                "id": "products",
                "placeholder": "Produit",
            }
        ),
    )
