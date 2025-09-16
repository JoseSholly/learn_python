from django import template
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

register = template.Library()

@register.filter
def pygmentize(code, language='python'):
    lexer = get_lexer_by_name(language)
    formatter = HtmlFormatter()
    return highlight(code, lexer, formatter)