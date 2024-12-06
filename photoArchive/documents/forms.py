from django import forms
from .models import Document, Image, Tag

class DocumentForm(forms.ModelForm):
    new_tags = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите новые теги, разделенные запятыми'})
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Document
        fields = ['name', 'description', 'created_at', 'tags', 'new_tags']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'created_at': 'Дата создания',
            'tags': 'Теги',
            'new_tags': 'Новые теги',
        }
        widgets = {
            'created_at': forms.DateInput(attrs={'type': 'date'}),
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

ImageFormSet = forms.modelformset_factory(Image, form=ImageForm, extra=10)

class SearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Название'
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control'}),
        label='Дата начала'
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control'}),
        label='Дата окончания'
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='Теги'
    )
