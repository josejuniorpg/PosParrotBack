from django import forms
from .models import OrderProduct
from apps.pos_systems.models import Product


class OrderProductForm(forms.ModelForm):
    """
    Custom form for OrderProduct in Django Admin.
    Dynamically filters products based on the selected order.
    """

    class Meta:
        model = OrderProduct
        fields = 'product', 'quantity', 'order',



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not getattr(self.instance, 'order', None):
            print("No order")
            self.fields['product'].queryset = Product.objects.all()
            return
        # todo: Product Status
        if self.instance.order:
            self.fields['product'].queryset = Product.objects.filter(restaurants=self.instance.order.restaurant)
        else:
            self.fields['product'].queryset = Product.objects.none()
