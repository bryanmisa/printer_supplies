from django import template
from django.template import Library, Node

register = template.Library()


@register.filter
def can_do(user, permission_code):
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.role == 'admin':
        return True
    if hasattr(user, 'has_permission'):
        return user.has_permission(permission_code)
    return False


@register.filter
def has_role(user, role):
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.role == 'admin':
        return True
    return user.role == role


@register.inclusion_tag('rbac/permissions_required.html')
def permission_required_tag(permission_code):
    return {'permission_code': permission_code}


class IfCanDoNode(Node):
    def __init__(self, permission_code, nodelist_true, nodelist_false):
        self.permission_code = permission_code
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        user = context.get('user')
        permission_code = self.permission_code.resolve(context)

        if can_do(user, permission_code):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)


def if_can_do(parser, token):
    try:
        tag_name, permission_code = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("Usage: {% if_can_do 'permission_code' %}")

    nodelist_true = parser.parse(('else', 'endif_can_do'))
    token = parser.next_token()

    if token.contents == 'else':
        nodelist_false = parser.parse(('endif_can_do',))
        parser.next_token()
    else:
        nodelist_false = template.NodeList()

    return IfCanDoNode(parser.compile_filter(permission_code), nodelist_true, nodelist_false)


register.tag('if_can_do', if_can_do)