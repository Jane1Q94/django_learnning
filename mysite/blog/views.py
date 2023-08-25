from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .models import Post
from .forms import CommenctForm, EmailPostForm


def post_list(request):
    obj_list = Post.published.all()
    paginator = Paginator(obj_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page})


def post_detail(request, year, month, day, post):
    post: Post = get_object_or_404(Post, slug=post, status='published',
                                   publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = False
    if request.method == 'POST':
        comment_form = CommenctForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            new_comment = True
            return redirect(post.get_absolute_url())
    else:
        comment_form = CommenctForm()
    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'new_comment': new_comment
    })


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    send = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} ({cd['email']}) recommends you reading '{post.title}'"
            message = f"Read '{post.title}' at {post_url}\n\n{cd['name']}'s recomments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            send = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'send': send})


from django.views.generic import ListView


class PostListView(ListView):
    queryset = Post.published.all()
    # query results, default is object_list if don't specify any context_object_name
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'  # default is blog/post_list.html
    # default page result is page_obj
