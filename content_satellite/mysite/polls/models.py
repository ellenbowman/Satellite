from django.db import models

class Question(models.Model):
	question_text = models.CharField(max_length=200)
	def __unicode__(self):
		return self.question_text

class Choice(models.Model):
	question = models.ForeignKey(Question)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	max_votes = models.IntegerField(default=15)

class Outfit(models.Model):
	shirt = models.CharField(max_length=300)
	pants = models.CharField(max_length=300)
	shoes = models.IntegerField(default=0)