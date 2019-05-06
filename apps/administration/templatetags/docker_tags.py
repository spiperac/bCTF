from django import template

register = template.Library()


@register.filter(name='get_port')
def get_port(exposed):
    return {dock_port.split('/')[0]: host_port[0]['HostPort'] for dock_port, host_port in exposed.items()}
