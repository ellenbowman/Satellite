from django import template
register = template.Library()
from risk_ratings import hint_manager


@register.assignment_tag(takes_context=True)
def get_hint(context, question):
    if question.hint:
        method_to_call = getattr(hint_manager, question.hint.function_name)
        ts = context['ticker_stats']
        return method_to_call(ts)
    return None, None


HEADINGS_FOR_QUESTION_NUMBER = {
    1:'The Company',
    6:'Financials',
    11: 'The Competition',
    14: 'The Stock',
    17: 'Management',
    19: 'Service Specifics',
    21: 'Foolishness'
}

@register.filter
def strong_label_for_question_number(question_number):
    if question_number in HEADINGS_FOR_QUESTION_NUMBER:
        return '<strong>%s</strong><br/>' % HEADINGS_FOR_QUESTION_NUMBER[question_number]
    return ''

@register.filter
def heading_for_question_number(question_number):
    if question_number in HEADINGS_FOR_QUESTION_NUMBER:
        return '<h3>%s</h3>' % HEADINGS_FOR_QUESTION_NUMBER[question_number]
    return ''
