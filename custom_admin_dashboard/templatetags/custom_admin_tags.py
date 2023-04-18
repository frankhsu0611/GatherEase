from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def custom_dashboard_url(context):
    return reverse('home_dashboard')
