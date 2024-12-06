from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Tag(BaseModel):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Document(BaseModel):
    description = models.TextField(verbose_name='Описание')
    tags = models.ManyToManyField(Tag, related_name='documents', blank=True, verbose_name='Теги')
    uploaded_at = models.DateTimeField(default=timezone.now, verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

class Image(models.Model):
    document = models.ForeignKey(Document, related_name='images', on_delete=models.CASCADE, verbose_name='Документ')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f"Image for {self.document.name}"
