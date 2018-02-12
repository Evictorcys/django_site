from django import template
from django.utils.safestring import mark_safe
import markdown
from django.template.defaultfilters import stringfilter

register = template.Library()

from ..models import Post

@register.simple_tag
def total_posts():
    return Post.published.count()

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


