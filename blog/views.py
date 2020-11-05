from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm, EmailPostForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView,
                                    DetailView, CreateView,
                                    UpdateView, DeleteView)


# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'



class PostListView(ListView):
    model = Post
    paginate_by = 3

    def get_queryset(self):
        return Post.published.order_by('-published_date') #custom model manager
        # return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date') #default model manager



class PostDetailView(DetailView):
    model = Post
    # template_name = 'post_detail.html'
    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs['slug'] )



class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post



class UpdatePostView(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post



class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog_post_list')



class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    redirect_field_name = 'blog/post_detail.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull = True).order_by('-created_date')


################################################
################################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog_post_detail', pk=post.pk)


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    new_comment = None
    if request.method =='POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('blog_post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':comment_form, 'new_comment': new_comment})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog_post_detail', slug=comment.post.slug)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect ('blog_post_detail', slug=comment.post.slug)


def post_share(request, pk):
    post = get_object_or_404(Post, pk=pk, status='published')
    sent = False
    if request.method == "POST":
        #Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                    f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                    f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'unicornsinpython@gmail.com',
                    [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post_share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
