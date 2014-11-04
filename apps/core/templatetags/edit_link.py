from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.tag
def edit_link(parser, token):
    try:
        tag_name, obj_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return EditLinkNode(obj_name)


class EditLinkNode(template.Node):
    def __init__(self, obj_name):
        self.obj = template.Variable(obj_name)

    def render(self, context):
        obj = self.obj.resolve(context)
        app, model = obj._meta.app_label, obj._meta.module_name

        return '<a href=%s>admin</a>' % \
               reverse('admin:%s_%s_change' % (app, model), args=[obj.id])
