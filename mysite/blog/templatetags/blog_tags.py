import markdown
from django import template
from django.utils.safestring import mark_safe
from django.db.models import Count
from ..models import Post

register = template.Library()


@register.simple_tag(name="total_posts")
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    # inclusion_tag must return a dictionary.
    return {'latest_posts': latest_posts}


@register.simple_tag(takes_context=True)
def get_most_commented_posts(context, count=5):
    most_commented_posts = Post.published.annotate(
        total_comments=Count('comments')).order_by('-total_comments')[:count]
    context['most_commented_posts'] = most_commented_posts
    return ''


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
