from django import template
from django.template.loaders.app_directories import load_template_source

register = template.Library()

def do_jquery_template(parser, token):
    """
    Dump the template in, wrapped in script tags for jQuery.tmpl
    
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument: the name of the template to include" % bits[0]
    
    template_name = bits[1]
    
    if template_name[0] in ('"', "'") and template_name[-1] == template_name[0]:
        template_name = template_name[1:-1]
        
    if len(bits) > 2:
        template_id = bits[2]
        if template_id[0] in ('"', "'") and template_id[-1] == template_id[0]:
            template_id = template_id[1:-1]
    else:
        template_id = template_name.rsplit('/',1)[-1].rsplit('.',1)[0]
    
    source, path = load_template_source(template_name)
    
    source = "<script type='text/html' id='%s'>\n%s\n</script>" % (
        template_id, source
    )
    
    return template.TextNode(source)

register.tag("jquery_template", do_jquery_template)
