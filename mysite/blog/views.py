from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


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
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


from django.views.generic import ListView


class PostListView(ListView):
    queryset = Post.published.all()
    # query results, default is object_list if don't specify any context_object_name
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'  # default is blog/post_list.html
    # default page result is page_obj
