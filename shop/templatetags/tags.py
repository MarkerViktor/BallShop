from django import template

from shop.models import SportType, Advertisement


register = template.Library()


@register.simple_tag()
def get_categories():
    return SportType.objects.all()


@register.simple_tag()
def get_advertisements():
    return Advertisement.objects.all()
