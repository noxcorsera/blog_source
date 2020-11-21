from .models import Post, EmailSubscription
from .forms import CommentForm, EmailForm

from django.shortcuts import render, get_object_or_404
from django.views import generic


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

#class PostDetail(generic.DetailView):
#    model = Post
#    template_name = 'post_detail.html'

def about(request):
    template_name = 'about.html'
    return render(request, template_name)

class PhotosPage(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'photos.html'

def subscribe(request):
    template_name = 'subscribe.html'
    # new subscription
    if request.method == 'POST':
        email_form = EmailForm(data=request.POST)
        if email_form.is_valid():
            new_email = email_form.save(commit=False)
            new_email.save()
            new_email_status = True
    else:
        email_form = EmailForm()
        new_email_status = False

    return render(request, template_name, {'email_form': email_form,
                                           'new_email': new_email_status})

def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
