from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm


# Create your views here.
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})

def post_share(request, post_id):
    #Get post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form sended to save
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # All form fields validated
            cd = form.cleaned_data
            # Sending email post
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading " {}"'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
        else:
            form = EmailPostForm()
            return render(request, 'blog/post/share.html',
                          {'post': post, 'form': form, 'sent': sent})