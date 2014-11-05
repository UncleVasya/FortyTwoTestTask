from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def edit_link(obj):
    app, model = obj._meta.app_label, obj._meta.module_name

    return '<a href=%s>admin</a>' % \
           reverse('admin:%s_%s_change' % (app, model), args=[obj.id])
