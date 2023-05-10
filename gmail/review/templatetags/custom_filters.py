from django import template
from review.models import Message

register = template.Library()

@register.filter(name='get_message_by_id')
def get_message_by_id(message_id):
    return Message.objects.get(pk=message_id)


