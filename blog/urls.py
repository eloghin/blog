from django.urls import path
from blog import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog_post_list'),
    path('about/', views.AboutView.as_view(), name="blog_about"),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name="blog_post_detail"),
    path('post/new/', views.CreatePostView.as_view(), name="blog_post_new"),
    path('post/<int:pk>/edit/', views.UpdatePostView.as_view(), name="blog_post_edit"),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name="blog_post_delete"),
    path('drafts/', views.DraftListView.as_view(), name="blog_post_draft_list"),

    path('post/<int:pk>/comment/', views.add_comment_to_post, name="blog_add_comment_to_post"),
    path('comment/<int:pk>/approve/', views.comment_approve, name="blog_comment_approve"),
    path('comment/<int:pk>/delete/', views.comment_remove, name="blog_comment_delete"),
    path('post/<int:pk>/publish', views.post_publish, name="blog_post_publish"),

]
