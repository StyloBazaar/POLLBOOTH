from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import loader
from .models import Question, Choice
from django.views import generic


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "question_set"

    def get_queryset(self):
        return Question.objects.filter(publishing_date__lte=timezone.now())


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"


class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/result.html"


#def index(request):
    #question_set = Question.objects.all()
    #template = loader.get_template('polls/index.html')
    #context = {'question_set': question_set}
    # SHORTCUT for RENDERING Context with template is as below:
    # return render(request, 'polls/index.html', context)
    #return HttpResponse(template.render(context, request))


#def details(request, question_id):
    #try:
     #   question = Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
     #   raise Http404("Question Does not Exist")
    # There is a shortcut in Django for getting an object and returning http404 error if object doesn't exist
    # The above four lines could be replaced as below
    # question = get_object_or_404(Question, pk=Question_id)
    #return render(request, "polls/details.html", {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {'question': question, 'error_message': 'Please Select a choice' })
    else:
        selected_choice.votes_count += 1
        selected_choice.save()
        return redirect('polls:result', question_id)


#def result(request, question_id):
    #question = get_object_or_404(Question, pk=question_id)
    #return render(request, "polls/result.html", {'question': question})
