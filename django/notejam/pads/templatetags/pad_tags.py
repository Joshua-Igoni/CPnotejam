# pads/templatetags/pad_tags.py
from django import template
from pads.models import Pad

register = template.Library()


def do_get_pads(parser, token):
    try:
        tag_name, as_, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires the syntax:  {% %s as <varname> %}"
            % (token.contents.split()[0], token.contents.split()[0])
        )

    if as_ != "as":
        raise template.TemplateSyntaxError("Format is: %s as VARNAME" % tag_name)

    return GetPadsNode(var_name)


class GetPadsNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
     
        request = context.get("request")
        user    = getattr(request, "user", None)

        if user and user.is_authenticated:
            context[self.var_name] = Pad.objects.filter(user=user)
        else:
            context[self.var_name] = Pad.objects.none()
        return ""


register.tag("get_pads", do_get_pads)
