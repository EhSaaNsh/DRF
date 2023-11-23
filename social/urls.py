from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('posts/', views.PostsView.as_view(), name='posts'),
    path('post/create/', views.CreatePostView.as_view()),
    path('posts/detail/<int:post_id>/', views.PostDetailView.as_view()),
    path('posts/update/<int:post_id>/', views.UpdatePostView.as_view()),
    path('posts/delete/<int:post_id>/', views.DeletePostView.as_view()),
    path('posts/<int:post_id>/', views.CommentAddToPostView.as_view()),
    path('posts/comment/reply/<int:post_id>/<int:comment_id>/', views.AddReplyToCommentView.as_view()),
    path('posts/vote/<int:post_id>/', views.PostLikeView.as_view())
]