from django import template
from django.urls import reverse
from ..models import NavigationItem, SiteSettings

register = template.Library()

@register.simple_tag
def get_navigation_items():
    """Retourne les éléments de navigation principaux"""
    return NavigationItem.objects.filter(
        parent__isnull=True, 
        is_active=True
    ).order_by('order')

@register.simple_tag
def get_site_settings():
    """Retourne les paramètres du site"""
    settings = SiteSettings.objects.first()
    if not settings:
        settings = SiteSettings.objects.create(
            site_name="Bijoux & Créations",
            buy_button_text="ACHETER MAINTENANT",
            buy_button_url="#"
        )
    return settings

@register.filter
def get_nav_url(item):
    """Génère l'URL appropriée pour un élément de navigation"""
    if item.is_external or item.url.startswith(('http://', 'https://', '#')):
        return item.url
    try:
        return reverse(item.url)
    except:
        return item.url