from django.test import TestCase, Client
from django.urls import reverse
from .models import Document, Image, Tag
from .forms import DocumentForm, ImageForm, SearchForm
from django.contrib.auth.models import User

class DocumentViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')
        self.document = Document.objects.create(name='Test Document', created_at='2023-10-01')
        self.tag = Tag.objects.create(name='Test Tag')
        self.document.tags.add(self.tag)
        self.image = Image.objects.create(document=self.document, image='..\photoArchive\media\images\\3AnoICfQyaM_6ksWdQm.jpg')

    def test_document_search_view(self):
        response = self.client.get(reverse('document_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoArchive/document_search.html')

        # Test search with name
        response = self.client.get(reverse('document_search'), {'name': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Document')

        # Test search with date range
        response = self.client.get(reverse('document_search'), {'start_date': '2023-09-01', 'end_date': '2023-10-01'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Document')

        # Test search with tags
        response = self.client.get(reverse('document_search'), {'tags': [self.tag.id]})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Document')

    def test_document_detail_view(self):
        response = self.client.get(reverse('document_detail', args=[self.document.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoArchive/document_detail.html')
        self.assertContains(response, 'Test Document')

    def test_document_create_view(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('document_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoArchive/document_form.html')

        # Test document creation
        response = self.client.post(reverse('document_create'), {
            'name': 'New Document',
            'description': 'New Description',
            'created_at': '2023-10-02',
            'new_tags': 'New Tag',
            'tags': [self.tag.id],
        })
        self.assertEqual(response.status_code, 200)

    def test_document_update_view(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('document_update', args=[self.document.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoArchive/document_form.html')

        # Test document update
        response = self.client.post(reverse('document_update', args=[self.document.id]), {
            'name': 'Updated Document',
            'description': 'Updated Description',
            'created_at': '2023-10-02',
            'new_tags': 'Updated Tag',
            'tags': [self.tag.id],
        })
        self.assertEqual(response.status_code, 302)
        self.document.refresh_from_db()
        self.assertEqual(self.document.name, 'Updated Document')

    def test_document_delete_view(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('document_delete', args=[self.document.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoArchive/document_confirm_delete.html')

        # Test document deletion
        response = self.client.post(reverse('document_delete', args=[self.document.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('document_search'))
        self.assertFalse(Document.objects.filter(id=self.document.id).exists())
