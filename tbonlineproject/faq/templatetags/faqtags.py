import re

from django import template

from faq.models import QuestionCategory, QuestionAndAnswer

register = template.Library()


class QuestionsByCategories(template.Node):
    def __init__(self, categories, var_name):
        self.categories = categories
        self.var_name = var_name

    def render(self, context):
        try:
            context[self.var_name] =  QuestionCategory.objects.filter(pk__in=self.categories)
        except:
            pass
        return ""

def do_get_question_categories(parser, token):
    
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])

    m = re.search(r'(\"[0-9,]+\") as (\w+)', arg)
    
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
    
    category_string, var_name = m.groups()
    category_string = category_string[1:-1]
    
    try:
        categories = [int(i) for i in category_string.rsplit(",")]
    except ValueError:
        raise template.TemplateSyntaxError("List of question and answer "
                            "categories must be comma separated integers")
        
    return QuestionsByCategories(categories, var_name)

register.tag('get_question_categories', do_get_question_categories)
