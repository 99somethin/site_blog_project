from django import template
from ..models import PostModel
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.simple_tag(name='posts_count')
def total_posts():
    return PostModel.published.count()


@register.inclusion_tag('blog/inclusions/latest_posts.html')
def show_latest_posts(count=2):
    latest_posts = PostModel.published.all().order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag(name='most_comment_posts')
def get_most_commented_posts(count=3):
    return PostModel.published.annotate(
        comments_count=Count('comments')).exclude(comments_count=0).order_by('-comments_count')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))