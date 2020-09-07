from django.db import models
from django.utils import timezone
import datetime


class Question(models.Model):
    question_text = models.CharField(max_length=2083)
    publishing_date = models.DateTimeField('Date Published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.publishing_date <= timezone.now()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    votes_count = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
