from django import template
from django.utils.safestring import mark_safe
from re import IGNORECASE, compile, escape as rescape



register = template.Library()


@register.filter(name='highlight')
def highlight(text, search):
    if search == '':
        return text
    rgx = compile(rescape(search), IGNORECASE)
    highlighted = rgx.sub(
            lambda m: '<b style="color:black;background-color:#ffff66">{}</b>'.format(m.group()),
            text
        )
    # highlighted = text.replace(search, '<b style="color:black;background-color:#ffff66">{}</b>'.format(search))
    return mark_safe(highlighted)
