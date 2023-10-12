from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

@register.filter
@stringfilter
def money(string):
  """ Formats currency with dots """
  regex = "(?=([0-9]{3})+$)"
  parsed = re.sub(regex,'.',string)
  return f"${parsed.strip('.')}"

