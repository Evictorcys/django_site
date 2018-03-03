from django import template
from django.utils.safestring import mark_safe
import markdown
from django.template.defaultfilters import stringfilter
from django.db.models import Count

register = template.Library()

from ..models import Post

@register.simple_tag
def total_posts():
    return Post.published.count()


# 分配标签（assignment tag）类似简单标签（simple tags）但是他们将结果存储在给予的变量中。2.0中删除了。
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
                total_comments=Count('comments')
            ).order_by('-total_comments')[:count]


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=3):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.filter(name='markdown')
@stringfilter
def markdown_format(text):
    return mark_safe(markdown.markdown(text,extensions=
                                       ['markdown.extensions.fenced_code',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.tables'],
                                       safe_mode=True,
                                       enable_attributes=False))


