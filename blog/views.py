from django.shortcuts import render,get_object_or_404, redirect
from django.utils import timezone
from .models import Post,Comment
from .forms import PostForm,CommentForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator



def post_list(request):
    postspage = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    paginator = Paginator(postspage, 5) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    query=request.GET.get('q')
    if query:
        posts=posts.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) 
        ).distinct()

    return render(request, 'blog/post_list.html',  {'posts': posts})

def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post=post
            comment.save()
            return redirect('post_detail', pk=post.pk)

    return render(request, 'blog/post_detail.html', {'post': post,'form': form,})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, 'Yollandı!')
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
