from django import forms

from .models import Cart

class CartFormCreate(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CartFormCreate, self).__init__(*args, **kwargs)

    def clean(self):
        session_key = self.request.session.session_key
        cleaned_data = super(CartFormCreate, self).clean()
        name = cleaned_data.get('name')
        if Cart.objects.filter(name=name, session_key=session_key).exists():
            raise forms.ValidationError(
                'You already have %(name)s cart, you need to choose another name',
                params={'name': name},
            )

    class Meta:
        model = Cart
        fields = [
            'name',
            'description'
        ]

class CartFormUpdate(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id')
        super(CartFormUpdate, self).__init__(*args, **kwargs)

    def clean(self):
        session_key = self.request.session.session_key
        cleaned_data = super(CartFormUpdate, self).clean()
        name = cleaned_data.get('name')
        try:
            cart = Cart.objects.get(name=name, session_key=session_key)
            if int(cart.id) != int(self.id):
                raise forms.ValidationError(
                    'You already have %(name)s cart, you need to choose another name',
                    params={'name': name},
                )
        except Cart.DoesNotExist:
            pass

    class Meta:
        model = Cart
        fields = [
            'name',
            'description'
        ]
