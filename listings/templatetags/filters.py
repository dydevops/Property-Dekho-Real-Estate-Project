from django import template

register = template.Library()

@register.filter(name='format_price')
def format_price(value):
    if value >= 10000000:
        return f"{value/10000000:.2f} Cr"
    elif value >= 100000:
        return f"{value/100000:.2f} Lakh"
    elif value >= 1000:
        return f"{value/1000:.2f} K"
    else:
        return str(value)