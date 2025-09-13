from django import forms

class ExampleForm(forms.Form):
    # Example fields, adjust as needed
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
