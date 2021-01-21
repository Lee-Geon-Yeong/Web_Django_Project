from django.template import Library
register = Library()

@register.filter(is_safe=True)
def has_liked(obj, user):
    return obj.has_likes(user) 
