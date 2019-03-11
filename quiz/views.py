from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import TemplateView, ListView, DetailView, RedirectView
from .forms import RepoForm, ModuleForm, TopicForm
from .forms import QuestionForm, QuizForm, FillQuizForm, MCQForm
from django.urls import reverse_lazy, reverse
from .models import Subject, Module, Topic, Answer, Question, Quiz, Pattern, Repository
from django.forms import modelformset_factory, inlineformset_factory
from .quiz import ActiveQuiz, AllAttempt
import time


# Create your views here.

class CreateRepository(CreateView):
    template_name = "quiz/create_repository.html"
    form_class = RepoForm
    success_url = reverse_lazy("quiz:list_repo")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CreateRepository, self).form_valid(form)

class RepositoryList(TemplateView):
    template_name = "quiz/repository_list.html"


def repository_detail(request, pk):
    repo = Subject.objects.get(id=pk)
    modules = repo.modules.all()
    topics = modules[0].topic_set.all()
    topic_pk = topics[0].id
    return HttpResponseRedirect(reverse('quiz:topic_questions', 
                                        args=(pk, topic_pk)))


class ManageRepository(TemplateView):
    template_name = "quiz/manage_repo.html"
    
    def get_context_data(self, **kwargs):
        repo = Subject.objects.get(id=self.kwargs['pk'])
        context = super(ManageRepository, self).get_context_data(**kwargs)
        context['repo'] = repo
        return context


def manage_modules(request, pk):
    """
    Create and Edit Modules of Repository
    """
    repo = Repository.objects.get(pk=pk)
    ModuleInlineFormset = inlineformset_factory(Repository, Module, fields=('title',))
    if request.method == "POST":
        formset = ModuleInlineFormset(request.POST, instance=repo)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse_lazy('quiz:manage_repo',
                                                     args=(pk)))
    else:
        formset = ModuleInlineFormset(instance=repo)
    return render(request, 'quiz/add_module.html', {'formset': formset})



def delete_module(request, pk, module_pk):
    module = Module.objects.get(id=module_pk)
    module.delete()
    return HttpResponseRedirect(reverse("quiz:manage_repo", kwargs={'pk': pk}))


def add_topics(request, pk, module_pk):
    """
    Add and edit multiple topics to the given module
    """
    repo = Repository.objects.get(pk=pk)
    module = Module.objects.get(pk=module_pk)
    TopicInlineFormset = inlineformset_factory(Module, Topic, fields=('title',))
    if request.method == 'POST':
        formset = TopicInlineFormset(request.POST, instance=module)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse_lazy('quiz:manage_repo',
                                                     args=(pk)))

    else:
        formset = TopicInlineFormset(instance=module)
        return render(request, 'quiz/add_topics.html', {'formset': formset})



class AddTopic(CreateView):
    template_name = "quiz/add_topic.html"
    model = Topic
    form_class = TopicForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        success_url = reverse_lazy("quiz:manage_repo", kwargs={'pk': pk})
        return success_url

    def form_valid(self, form):
        module = Module.objects.get(id=self.kwargs['module_pk'])
        form.instance.module = module
        return super(AddTopic, self).form_valid(form)


class RepoQuestions(TemplateView):
    template_name = "quiz/repo_contents.html"


    def get_context_data(self, **kwargs):
        repo = Subject.objects.get(id=self.kwargs['pk'])
        context = super(RepoQuestions, self).get_context_data(**kwargs)
        context['repo'] = repo
        return context

class ListTopicQuestions(ListView):
    template_name = "quiz/topic_questions_list.html"
    
    def get_queryset(self):
        topic = Topic.objects.get(id=self.kwargs['topic_pk'])
        questions = topic.question_set.all()
        return questions

    def get_context_data(self, **kwargs):
        repo = Subject.objects.get(id=self.kwargs['pk'])
        topic = Topic.objects.get(id=self.kwargs['topic_pk'])
        context = super(ListTopicQuestions, self).get_context_data(**kwargs)
        context['repository'] = repo
        context['topic'] = topic
        return context


def add_question(request, pk, topic_pk):
    AnswerFormSet = modelformset_factory(Answer,fields=('answer', 'is_correct'), extra=4)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            created_question = question_form.save(commit=False)
            created_question.topic = Topic.objects.get(id=topic_pk)
            created_question.save()
            formset = AnswerFormSet(request.POST)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.question = created_question
                    instance.save()
                return HttpResponseRedirect(reverse('quiz:topic_questions', args=(pk, topic_pk,)))
    else:
        question_form = QuestionForm()
        formset = AnswerFormSet(queryset=Answer.objects.none())
        return render(request, 
                      'quiz/add_question.html', 
                      {'question_form': question_form ,'formset': formset})


def delete_question(request, pk, topic_pk, quest_pk):
    question = get_object_or_404(Question, id=quest_pk)
    question.delete()
    return HttpResponseRedirect(reverse('quiz:topic_questions', args=(pk, topic_pk,)))


###### QUIZ VIEWS #######

class CreateQuiz(CreateView):
    template_name = "quiz/create_quiz.html"
    form_class = QuizForm
    success_url = reverse_lazy("account:profile")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CreateQuiz, self).form_valid(form)

class ListQuiz(TemplateView):
    template_name = "quiz/quiz_list.html"


class QuizDetail(DetailView):
    model = Quiz
    


class QuizDelete(DeleteView):
    pass

def add_question_to_quiz(request, pk, topic_pk, quest_pk):
    if request.method == 'POST':
        form = FillQuizForm(request.POST)
        question = get_object_or_404(Question, id=quest_pk)
        if form.is_valid():
            quiz = get_object_or_404(Quiz, id=form.cleaned_data['quiz'])
            quiz_questions = quiz.get_questions()
            if question not in quiz_questions:
                p = Pattern(question=question, 
                            quiz=quiz , 
                            mark=form.cleaned_data['mark'],
                            negative_mark=form.cleaned_data['negative_mark'])
                p.save()
        return HttpResponseRedirect(reverse('quiz:topic_questions', args=(pk, topic_pk,)))
    else:
        form = FillQuizForm()
        return render(request, 'quiz/add_question_to_quiz.html', {'form': form})

def remove_question_from_quiz(request, quiz_pk, quest_pk ):
    quiz = Quiz.objects.get(id=quiz_pk)
    quest = Question.objects.get(id=quest_pk)
    pat = Pattern.objects.get(quiz=quiz, question=quest)
    pat.delete()
    return HttpResponseRedirect(reverse('quiz:quiz_detail', args=(quiz_pk)))



def publish_quiz(request, pk):
    quiz = Quiz.objects.get(id=pk)
    quiz.status = 'P'
    quiz.save()
    return HttpResponseRedirect(reverse('quiz:quiz_detail', args=(pk)))


def start_quiz(request, quiz_pk):
    quiz = ActiveQuiz(request)
    quiz.stuff_questions(quiz_pk)
    return HttpResponseRedirect(reverse('quiz:fetch_question', kwargs={'order': 1}))
    #return HttpResponse(quiz.session.get_expiry_age())


def fetch_question(request, order):
    quiz = ActiveQuiz(request)
    current = time.monotonic()
    if not quiz.is_live():
       return HttpResponseRedirect(reverse('quiz:submit_quiz'))
    q = quiz.get_question(order=order) # get tuple of order_no and question (order, question)
    orders = quiz.get_questions_order()
    unattempts = [i for i in orders if not quiz.get_response(i)]
    if request.method == 'POST':
        form = MCQForm(q[1], request.POST)
        if form.is_valid():
            cd = form.cleaned_data['answers']
            quiz.update_response(order, cd)
            try: 
                next_ord = quiz.get_next_question(int(order))
                return HttpResponseRedirect(reverse('quiz:fetch_question', 
                                                    kwargs={'order': next_ord}))
            except AllAttempt:
                return HttpResponseRedirect(reverse('quiz:fetch_question', kwargs={'order': 1}))
    else:
        resp = quiz.get_response(q[0])
        form = MCQForm(q[1], initial={'answers': resp})
        return render(request, 'quiz/fetch_quiz_question.html', {'form': form, 
                                                                 'question': q,
                                                                 'orders': orders})


def submit_quiz(request):
    quiz = ActiveQuiz(request)
    summary = quiz.get_summary()
    return render(request, 'quiz/quiz_summary.html', {'summary': summary})

def exit_quiz(request):
    quiz = ActiveQuiz(request)
    quiz.get_score(request)
    quiz.clear()
    return redirect(reverse('account:profile'))

