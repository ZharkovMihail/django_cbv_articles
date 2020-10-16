from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Articles(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец статьи", blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    url = models.SlugField(max_length=130, unique=True)

    def get_absolute_url(self):
        return reverse("detail_page", kwargs={"slug": self.url})

    def get_absolute_url_to_update_page(self):
        return reverse("update_page", kwargs={"slug": self.url})

    def get_absolute_url_to_delete_page(self):
        return reverse("delete_page", kwargs={"slug": self.url})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'
