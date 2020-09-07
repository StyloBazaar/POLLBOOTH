from django.contrib import admin
from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'publishing_date')


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text', 'votes_count')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)