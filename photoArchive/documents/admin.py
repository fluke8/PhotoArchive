from django.contrib import admin
from .models import Tag, Document, Image

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'uploaded_at')
    search_fields = ('name', 'description')
    list_filter = ('tags', 'created_at', 'uploaded_at')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('document', 'image')
    search_fields = ('document__name',)
