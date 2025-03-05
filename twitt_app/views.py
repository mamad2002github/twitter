from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, FormView, CreateView
from .forms import AddCommentForm
from twitt_app.models import Post, Comment,Like



# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = "twitt_app/list_post.html"
    context_object_name = "posts"
    paginate_by = 4


    def get_queryset(self):
        posts = super(PostListView, self).get_queryset()
        return posts.all().order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['title'] = "Post List"
        context['welcome'] = 'welcome to twitter'
        return context

class PostCommentView(DetailView):
    model =Post
    template_name = "twitt_app/detail_post.html"

    def get_context_data(self, **kwargs):
        context = super(PostCommentView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)
        return context

class AddCommentView(FormView):
    model = Comment
    form_class = AddCommentForm
    template_name = "twitt_app/Add_comment.html"

    def dispatch(self, request, *args, **kwargs):
        """ گرفتن پست بر اساس pk و ذخیره برای استفاده در متدهای دیگر """
        self.current_post = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ ارسال اطلاعات پست به قالب """
        context = super().get_context_data(**kwargs)
        context['post'] = self.current_post
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.current_post  # اتصال کامنت به پست
        comment.author = self.request.user  # نویسنده
        comment.save()

        # ریدایرکت به لیست کامنت‌های پست
        return redirect(reverse('post_comments', kwargs={'pk': self.current_post.pk}))


class LikePostView(LoginRequiredMixin,DetailView):
    model = Like
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(post=post, author=request.user)
        if not created:
            like.delete()  # اگر کاربر قبلاً لایک کرده باشد، لایک را حذف کن
        return HttpResponseRedirect(reverse('post_list'))