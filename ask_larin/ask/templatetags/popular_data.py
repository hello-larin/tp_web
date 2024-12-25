from django.core.cache import cache
from django import template
from ask.models import *


register = template.Library()

@register.inclusion_tag('tags.html')
def tags():
    tags = cache.get("tags")
    if not tags:
        print("NO CACHE")
        tags = Tag.objects.popular_tags()
        cache.set("tags", tags, timeout=60 * 15)  # Кэшируем на 15 минут
    return {'tags': tags}
        
@register.inclusion_tag('users.html')
def users():
    users = cache.get("users")
    print(users)
    if not users:
        print("NO CACHE")
        users = Profile.objects.popular_users()
        cache.set("users", users, timeout=60 * 15)  # Кэшируем на 15 минут
    return {'users': users}