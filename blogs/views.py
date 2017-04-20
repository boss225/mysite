from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, File
from .forms import PostForm, CommentForm, UploadFileForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def post_list(request):
    posts_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(posts_list, 5)
    pageNumber = request.GET.get('page')
    try:
        posts = paginator.page(pageNumber)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments_list = post.comments.filter(post_id=pk)
    paginator = Paginator(comments_list, 5)
    pageNumber = request.GET.get('page')

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blogs:post_detail', pk=post.pk)
    else:
        form = CommentForm()

    try:
        comments = paginator.page(pageNumber)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_detail.html', {'post': post,'form':form,'comments':comments})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        formfile = UploadFileForm(request.POST, request.FILES)
        if ( form.is_valid() and formfile.is_valid() ):
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            postid = get_object_or_404(Post, pk=post.pk)
            upload(request.FILES['file'])
            file = File()
            file.post = postid
            file.title = request.POST['title']
            file.link = '/static/upload/'+request.FILES['file'].name
            file.save()

            return redirect('blogs:post_detail', pk=post.pk)
    else:
        form = PostForm()
        formfile = UploadFileForm()

    return render(request, 'blog/post_edit.html', {'form': form, 'formfile':formfile})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk) 
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        formfile = UploadFileForm(request.POST, request.FILES)
        if formfile.is_valid():
            upload(request.FILES['file'])
            file = File()
            file.post = post
            file.title = request.POST['title']
            file.link = '/static/upload/'+request.FILES['file'].name
            file.save()
            
        if form.is_valid():    
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('blogs:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        formfile = UploadFileForm()

    return render(request, 'blog/post_edit.html', {'form': form, 'formfile':formfile})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()

    return redirect('blogs:post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()

    return redirect('blogs:post_list')


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blogs:post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blogs:post_detail', pk=comment.post.pk)

def upload(f): 
    file = open('blogs/static/upload/'+f.name, 'wb+') 
    for chunk in f.chunks():
        file.write(chunk)