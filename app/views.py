from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from app.forms import CommentForm

from app.models import Comments, Post

# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'app/index.html', context)
def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comments.objects.filter(post=post, parent=None)
    form = CommentForm()
    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            if request.POST.get('parent'):
                parent=request.POST.get('parent')
                parent_obj=Comments.objects.get(id=parent)
                if parent_obj:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_obj
                    comment_reply.post = post
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))
            else:
                comment = comment_form.save(commit=False) #In Django, the commit=False parameter is used when you want to save an object to the database, but you want to delay the actual database write until later. This is often used when you want to perform additional processing on the object before it is saved to the database, or when you want to save multiple objects at once and want to ensure that they are all saved in a single database transaction.
                postid = request.POST.get('post_id')
                post = Post.objects.get(id = postid)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug}))

    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count = post.view_count + 1
    post.save()

    context = {
        'post':post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'app/post.html', context)