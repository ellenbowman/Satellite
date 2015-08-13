from django.shortcuts import render, redirect
from models import Ticker, TickerProfile, Questionnaire, RiskRatingDraft, get_crushability, CRUSHABILITY_CUTOFFS, Feedback, RiskRatingDraft, DataImportLog
from forms import FeedbackForm
import json

def _get_ticker_box_options():
    options = [str('%s (%s)') % (str(t.symbol), str(t.company_name)) for t in Ticker.objects.all()]
    options.sort()
    return options

def get_crushability_scale_markup():
    markup = []
    for i in range(0, len(CRUSHABILITY_CUTOFFS)):
        min_val = 0 if i==0 else CRUSHABILITY_CUTOFFS[i-1][0]
        markup.append("- %d-%d: %s" % (min_val, CRUSHABILITY_CUTOFFS[i][0], CRUSHABILITY_CUTOFFS[i][1]))
    return '<br/>'.join(markup)

def index(request):
    print request
    context = {
        'ticker_box_options':_get_ticker_box_options()
    }
    return render(request, 'risk_ratings/index.html', context)

def activity_log_index(request):
    print request
    context = {
        'page_title':"Activity Log",
        'drafts': RiskRatingDraft.objects.all().order_by('-timestamp'),
        'data_imports': DataImportLog.objects.all().order_by('-timestamp')
    }
    return render(request, 'risk_ratings/activity_log_index.html', context)

def create_risk_rating_unsupported_lookup(request, error_message):
    '''
    displays the risk ratings landing page, with an error message at the top
    '''
    context = {
        'error':error_message
    }
    return render(request, 'risk_ratings/index.html', context)

def create_risk_rating(request):
    team_name = request.GET['team_name']
    ticker_symbol = request.GET['ticker'].split('(')[0].strip().upper() # split() in case company name was included

    try:
        ticker = Ticker.objects.get(symbol=ticker_symbol)
        tickerprofile = TickerProfile.objects.get(ticker=ticker)
    except:
        return create_risk_rating_unsupported_lookup(request, error_message='ticker %s is not in our system' % ticker_symbol)

    try:
        questionnaire = Questionnaire.objects.get(name=team_name)
        questions = questionnaire.get_questions()
    except:
        return create_risk_rating_unsupported_lookup(request, error_message='questionnaire %s is not in our system' % team_name)

    ticker_snapshot_url = 'http://www.fool.com/quote/%s/%s/%s' % (ticker.exchange.lower(), ticker.symbol.lower(), ticker.symbol.lower())

    context = {
        'page_title':"Create Risk Rating",
        'ticker_stats':tickerprofile,
        'ticker':ticker.symbol,
        'snapshot_url':ticker_snapshot_url,
        'company_name':ticker.company_name,
        'team_name':team_name,
        'questions':questions,
        'previous_url':request.GET['previous_url'].split('?')[0] if 'previous_url' in request.GET else None,
        'previous_score':request.GET['previous_score'] if 'previous_score' in request.GET else None,
        'crushability_scale_markup':get_crushability_scale_markup()
    }
    return render(request, 'risk_ratings/ticker_detail.html', context)

def _save_responses(ticker, questionnaire, responses_as_list, crushability_count):
    draft = RiskRatingDraft()
    draft.questionnaire_name=questionnaire.name
    draft.ticker_symbol=ticker.symbol
    draft.crushability_count=crushability_count
    draft.responses_json = json.dumps(responses_as_list)
    draft.save()

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


def contact(request):

    if request.POST:
        form = FeedbackForm(request.POST)

        if form.is_valid():

            context = {
                'page_title':"Feedback",
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'comments': form.cleaned_data['comments'],
            }

            try:
                Feedback.objects.create(name=context['name'], email=context['email'], comments=context['comments'])
            except Exception as e:
                context['error'] = str(e)

            return render(request, 'risk_ratings/contact_thanks.html', context)
    else:
        form = FeedbackForm()

    context = {
            'page_title':"Feedback",
            'feedbacks':Feedback.objects.all(),
            'form': form,
        }

    return render(request, 'risk_ratings/contact.html', context)
