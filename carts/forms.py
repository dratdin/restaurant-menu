from django import forms

from .models import Cart

class CartForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CartForm, self).__init__(*args, **kwargs)

    def clean(self):
        session_key = self.request.session.session_key
        cleaned_data = super(CartForm, self).clean()
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



