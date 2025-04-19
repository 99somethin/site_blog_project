from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.post_search, name='post_search'),
    path('', views.ShowPosts.as_view(), name='home_page'),
    path('<int:id>/share/', views.SharePost.as_view(), name='post_share'),
    path('<int:id>/comment/', views.CommentView.as_view(), name='post_add_comment'),
    path('<str:year>/<str:month>/<str:day>/<slug:post_slug>/', views.one_post, name='post_detail'),
]