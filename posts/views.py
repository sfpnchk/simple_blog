from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, CreateView, DetailView, FormView, DeleteView, UpdateView

from posts.forms import PostCreateForm, CommentForm
from posts.models import Posts, Comment


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Posts
    form_class = PostCreateForm
    template_name = 'posts/post_create.html'
    success_url = '/posts/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.author.has_perm('posts.publish'):
            form.instance.status = 'PUBLISHED'
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Posts
    success_url = '/posts/'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == self.request.user:
            return super(PostDeleteView, self).dispatch(request, *args, **kwargs)
        elif self.request.user.has_perm('posts.delete_news') is True:
            return super(PostDeleteView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied('You are dont have permissions for this')


class PostDetailView(DetailView):
    model = Posts
    template_name = 'posts/post_detail.html'
    context_object_name = 'posts'

    def get_object(self, queryset=None):
        return Posts.objects.get(id=self.kwargs['pk'], status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm
        comments = Comment.objects.filter(post=self.object)
        context['comments'] = comments
        context['can_delete'] = self.request.user.has_perm(
            'news.delete_news') or self.request.user == self.object.author
        context['can_change'] = self.request.user.has_perm(
            'news.change_news') or self.request.user == self.object.author

        return context


class PostUpdateView(UpdateView):
    model = Posts
    fields = ('title', 'content')
    template_name = 'posts/post_update.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == self.request.user:
            return super(PostUpdateView, self).dispatch(request, *args, **kwargs)
        elif self.request.user.has_perm('posts.delete_news') is True:
            return super(PostUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied('You are dont have permissions for this')


class PostListView(ListView):
    queryset = Posts.objects.filter(status='published')
    template_name = 'posts/home.html'
    context_object_name = 'post_list'
    ordering = '-posted_date'
    paginate_by = 3


class CommentView(FormView):
    model = Posts
    form_class = CommentForm
    success_url = '/posts/'

    def form_valid(self, form):
        news = Posts.objects.get(id=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.post = news
        comment = form.save()
        return super().form_valid(form)
