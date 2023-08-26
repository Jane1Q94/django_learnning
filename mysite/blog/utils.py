from django.db.models import Count, QuerySet
from .models import Post


def get_post_similar_posts(post: Post) -> QuerySet:
    """get similar post according to tags
    """
    post_tag_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tag_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        some_tags=Count('tags')).order_by('-some_tags', '-publish')[:4]

    return similar_posts
