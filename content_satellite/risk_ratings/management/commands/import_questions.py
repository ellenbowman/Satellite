import urllib
import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from risk_ratings.models import Question, Questionnaire, Hint

RISK_RATINGS_DATA_DIR = 'risk_ratings\\data\\questions\\'

TEMPLATE_TYPES = {
    'sa_david':'sa_david.txt',
    'sa_tom':'sa_tom.txt',
    'rb':'rb.txt',
    'beta':'beta.txt'
    }

class Command(BaseCommand):

    def handle(self, *args, **options):

        for tt in TEMPLATE_TYPES:
            try:
                questionnaire = Questionnaire.objects.get(name=tt)
                questionnaire.question_set.all().delete()
            except:
                questionnaire = Questionnaire.objects.create(name=tt)

            questions_file = RISK_RATINGS_DATA_DIR + TEMPLATE_TYPES[tt]
            with open(questions_file) as f:
                lines = f.readlines()
                for l in lines:
                    tokens = l.split('::')
                    tokens = [t.strip() for t in tokens]

                    try:
                        question_number = int(tokens[0])
                        question_label = tokens[1]
                        question_text = tokens[2]
                        hint_name = tokens[3]

                        hint_matches = Hint.objects.filter(name=hint_name)
                        question_hint = hint_matches[0] if hint_matches else None

                        question = Question.objects.create(questionnaire=questionnaire, label=question_label,
                        text=question_text, list_order=question_number, hint=question_hint)

                    except Exception as e:
                        print e
                        print 'error', l[:15]

    	print 'finished script'

        print 'summary:'
        for q in Questionnaire.objects.all():
            print q.name, q.question_set.count()
