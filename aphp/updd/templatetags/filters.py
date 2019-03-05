from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name="add_class")
def add_class(field, class_name):
    return field.as_widget(attrs={
        "class": " ".join((field.css_classes(), class_name))
})

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@register.filter(name="reduce_string")
def reduce_string(string, length):
    return string if len(string) < int(length) else string[:int(length)]+"..."