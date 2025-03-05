from django.urls import path
from . import views
from .views import LikePostView

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:pk>/comments', views.PostCommentView.as_view(), name='post_comments'),
    path('<int:pk>/comments/Add', views.AddCommentView.as_view(), name='Add_comments'),
    path('<int:pk>/like/', LikePostView.as_view(), name='like_post'),
]