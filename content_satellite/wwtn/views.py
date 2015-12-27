from django.shortcuts import render, redirect
from models import Ticker
import json

"""
def index(request):
    print request
    context = {
        'ticker_box_options':_get_ticker_box_options()
    }
    return render(request, 'risk_ratings/index.html', context)


def generate_markup(request):

    if not request.POST:
        raise

    questionnaire = Questionnaire.objects.get(name=request.POST['team_name'])
    ticker_symbol = request.POST['ticker_symbol']
    ticker = Ticker.objects.get(symbol = ticker_symbol)

    questions_and_responses = []

    for q in questionnaire.get_questions():

        q_label_key = 'question_label_%d' % q.id
        q_text_key = 'question_text_%d' % q.id
        r_key = 'decision_%d' % q.id
        r_detail_key = 'decision_detail_%d' % q.id

        questions_and_responses.append({
            'number':q.list_order,
            'q_label':request.POST.get(q_label_key, q.label),
            'q_text':request.POST.get(q_text_key, q.text),
            'r_short':request.POST.get(r_key, '').capitalize(),
            'r_detail':request.POST.get(r_detail_key,'')
        })

    count_negative_responses = len([qr for qr in questions_and_responses if qr['r_short'].lower()=='no'])
    crushability = get_crushability(count_negative_responses, len(questions_and_responses))

    _save_responses(ticker, questionnaire, questions_and_responses, count_negative_responses)

    context = {
        'is_stock_advisor': questionnaire.name.startswith('sa_'),
        'is_rule_breakers': questionnaire.name.startswith('rb'),
        'questions_and_responses': questions_and_responses,
        'ticker':ticker,
        'count_negative_responses':count_negative_responses,
        'crushability':crushability,
        'previous_rating_url':request.POST.get('previous_url',None),
        'previous_rating':request.POST.get('previous_score',None),
        'previous_crushability': get_crushability(request.POST['previous_score']) if 'previous_score' in request.POST else None,
        'changes_from_previous':request.POST.get('changes_from_previous',None),
    }

    return render(request, 'risk_ratings/markup.html', context)
