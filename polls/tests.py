from django.test import TestCase
from polls.models import Question
from django.utils import timezone
import datetime
from django.test.utils import setup_test_environment
from django.urls import reverse


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_date(self):
        date = timezone.now()+ datetime.timedelta(days=15)
        question_in_future = Question(publishing_date=date)
        self.assertIs(question_in_future.was_published_recently(), False)

    def test_was_published_recently_with_same_date(self):
        date = timezone.now()
        question = Question(publishing_date=date)
        self.assertIs(question.was_published_recently(), True)

    def test_was_published_recently_with_past_date(self):
        date = timezone.now() - datetime.timedelta(days=2)
        question = Question(publishing_date=date)
        self.assertIs(question.was_published_recently(), False)

    def test_was_published_recently_with_last_date(self):
        date = timezone.now() - datetime.timedelta(days=1)
        question = Question(publishing_date=date)
        self.assertIs(question.was_published_recently(), True)


def create_question(question_text, days):
    publishing_date = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text= question_text, publishing_date= publishing_date)


class IndexViewTests(TestCase):
    def test_no_question_scenario(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Polls are Available")
        self.assertQuerysetEqual(response.context["question_set"], [])

    def test_past_question_scenario(self):
        create_question("Past_Question", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["question_set"], ['<Question: Past_Question>'])

    def test_future_question_scenario(self):
        create_question("Future_Question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["question_set"], [])

    def test_Past_and_future_question_scenario(self):
        create_question("Future_Question", 30)
        create_question("Past_Questions", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["question_set"], ['<Question: Past_Questions>'])

    def test_two_past_question_scenario(self):
        create_question("Past_Question1", -6)
        create_question("Past_Question2", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["question_set"],
                                 ['<Question:Past_Question2>', '<Question:Past_Question1>'])

