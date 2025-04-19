from dataclasses import fields

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import reverse
from slugify import slugify

# Create your models here.
translate_dict = {
        'а' : 'a', 'б' : 'b', 'в' : 'v', 'г' : 'g', 'д' : 'd', 'е' : 'e', 'ж' : 'zh', 'з' : 'z',
        'и' : 'i', 'й' : 'y', 'к' : 'k', 'л' : 'l', 'м' : 'm', 'н' : 'n', 'о' : 'o', 'п' : 'p',
        'р' : 'r', 'с' : 's', 'т' : 't', 'у' : 'u', 'ф' : 'f', 'х' : 'h', 'ц' : 'ts', 'ч' : 'ch',
        'ш' : 'sh', 'щ' : 'sht', 'ъ' : 'y', 'ы' : 'y', 'ь' : '\'', 'ю' : 'yu', 'я' : 'ya', 'А' : 'A',
        'Б' : 'B', 'В' : 'V', 'Г' : 'G', 'Д' : 'D', 'Е' : 'E', 'Ж' : 'Zh', 'З' : 'Z', 'И' : 'I',
        'Й' : 'Y', 'К' : 'K', 'Л' : 'L', 'М' : 'M', 'Н' : 'N', 'О' : 'O', 'П' : 'P', 'Р' : 'R',
        'С' : 'S', 'Т' : 'T', 'У' : 'U', 'Ф' : 'F', 'Х' : 'H', 'Ц' : 'Ts', 'Ч' : 'Ch', 'Ш' : 'Sh',
        'Щ' : 'Sht', 'Ъ' : 'Y', 'Ь' : '\'', 'Ю' : 'Yu', 'Я' : 'Ya', ' ': ' ',
    }

def translate(input_str):
    return ''.join(translate_dict.get(char, char) for char in input_str)



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=PostModel.Status.PUBLISHED)

class PostModel(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100, unique_for_date='publish')
    content = models.TextField()
    publish = models.DateTimeField(default=timezone.now, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts',
                               null=True)

    tags = models.ManyToManyField('TagsModel', blank=True, related_name='tags')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'year': self.publish.year,
                                              'month': self.publish.month,
                                              'day': self.publish.day,
                                              'post_slug': self.slug})



class CommentModel(models.Model):
    post = models.ForeignKey(PostModel,
                             on_delete=models.CASCADE, related_name='comments')

    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created']
        indexes = [
            models.Index(fields = ['created'])
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class TagsModel(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name
        self.slug = slugify(translate(self.name))
        return super(TagsModel, self).save(*args, **kwargs)
