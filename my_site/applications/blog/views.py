from re import search

from django.db.models import Count
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import PostModel, TagsModel
from django.views.generic import View, ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from my_site.settings import EMAIL_HOST_USER
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity

class ShowPosts(View):
    def get(self, request, *args, **kwargs):
        tag_slug = request.GET.get('item', 'all')
        if tag_slug == 'all':
            posts = PostModel.published.all()
        else:
            posts = PostModel.published.filter(tags__slug=tag_slug)

        paginator = Paginator(posts, 2)
        current_page = request.GET.get('page', 1)
        posts = paginator.get_page(current_page)

        return render(request, 'blog/index.html', context={'posts': posts})


class SharePost(View):

    def get_post(self, **kwargs):
        return get_object_or_404(PostModel, id=kwargs.get('id', 1), status=PostModel.Status.PUBLISHED)

    def get(self, request, *args, **kwargs):
        form = EmailPostForm()
        post = self.get_post(**kwargs)
        return render(request, 'blog/share_post.html', context={'form': form,
                                                                    'sent': False, 'post': post})
    def post(self, request, *args, **kwargs):
        form = EmailPostForm(request.POST)
        post = self.get_post(**kwargs)
        sent = False
        if form.is_valid():
            cd = form.cleaned_data

            post_url = request.build_absolute_uri(
                post.get_absolute_url())

            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s ({cd['email']}) comments: {cd['comments']}"

            send_mail(subject, message, EMAIL_HOST_USER,
                      [cd['send_to_email']])
            sent = True

        return render(request, 'blog/share_post.html', context={'form': form, 'post': post, 'sent': sent})




def one_post(request, **kwargs):
    post = get_object_or_404(PostModel,
                             publish__year=kwargs.get('year'),
                             publish__month=kwargs.get('month'),
                             publish__day=kwargs.get('day'),
                             slug=kwargs.get('post_slug'),
                             status=PostModel.Status.PUBLISHED)

    comments = post.comments.filter(active=True)
    form = CommentForm()
    tags = post.tags.all()

    similar_posts = (PostModel.published.filter(tags__in=tags)
                     .exclude(slug=post.slug).annotate(similar_tags=Count('tags')).order_by('similar_tags'))

    return render(request, 'blog/detail.html',
                  context={'post': post, 'comments': comments,
                           'form': form, 'tags': tags,
                           'similar_posts': similar_posts})


class CommentView(View):
    def get(self, request, *args, **kwargs):
        form = CommentForm()
        return render(request, 'blog/comments.html', context={'forms': form})

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        post = get_object_or_404(PostModel.published, id=kwargs.get('id'))

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

        return redirect(reverse('post_detail', kwargs={
            'year': post.publish.year,
            'month': post.publish.month,
            'day': post.publish.day,
            'post_slug': post.slug
        }))

def post_search(request):
    form = SearchForm()
    search = []
    query = None

    if request.GET.get('query', False):
        try:
            form = SearchForm(request.GET)
        except:
            form = SearchForm()

        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'content')
            search_query = SearchQuery(query)
            search = PostModel.published.annotate(similarity=TrigramSimilarity('title', query)) \
                .filter(similarity__gt=0.1).order_by('-similarity')
            if not search:
                search =  PostModel.published.annotate(s_vector=search_vector).filter(s_vector=search_query)

        return render(request, 'blog/search.html', {'form': form, 'query': query, 'results': search})

    return render(request, 'blog/search.html', {'form': form, 'query': query, 'results': search})

