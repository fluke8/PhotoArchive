from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Document, Image, Tag
from django.urls import reverse_lazy
from .forms import DocumentForm, ImageForm, ImageFormSet
from django.shortcuts import render, redirect
from .forms import SearchForm
from django.urls import reverse
from django.forms import modelformset_factory
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required

def superuser_required(user):
    return user.is_superuser

def document_search(request):
    form = SearchForm()
    results = Document.objects.all()
    tags = Tag.objects.all()  

    if request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            tag_ids = form.cleaned_data.get('tags')

            if name:
                results = results.filter(name__icontains=name)
            if start_date:
                results = results.filter(created_at__gte=start_date)
            if end_date:
                results = results.filter(created_at__lte=end_date)
            if tag_ids:
                results = results.filter(tags__id__in=tag_ids).distinct()

    return render(request, 'photoArchive/document_search.html', {'form': form, 'results': results, 'tags': tags})

class DocumentDetailView(DetailView):
    model = Document
    template_name = 'photoArchive/document_detail.html'
    context_object_name = 'document'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = Image.objects.filter(document=self.object)
        return context

def document_create_view(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=10)

    if request.method == 'POST':    
        form = DocumentForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

        if form.is_valid() and image_formset.is_valid():
            document = form.save()

            new_tags = form.cleaned_data.get('new_tags', '')
            if new_tags:
                new_tag_names = [tag.strip() for tag in new_tags.split(',')]
                for tag_name in new_tag_names:
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        document.tags.add(tag)

            for image_form in image_formset:
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.document = document
                    image.save()
                    print(f"Saved image: {image.image.url}")
                else:
                    print('No data in image form')

            print(f"Saved document: {document}")
            return redirect(reverse('document_search'))
    else:
        form = DocumentForm()
        image_formset = ImageFormSet(queryset=Image.objects.none())

    context = {
        'form': form,
        'image_formset': image_formset,
        'tags': Tag.objects.all(),
    }
    return render(request, 'photoArchive/document_form.html', context)

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class DocumentUpdateView(UpdateView):
    model = Document
    template_name = 'photoArchive/document_form.html'
    form_class = DocumentForm
    success_url = reverse_lazy('document_search')

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(superuser_required), name='dispatch')
class DocumentDeleteView(DeleteView):
    model = Document
    template_name = 'photoArchive/document_confirm_delete.html'
    success_url = reverse_lazy('document_search')
