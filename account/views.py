from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from quiz.models import Quiz
from django.views.generic import ListView

# Create your views here.


def profile(request):
    if request.user.user_type=='S':
        return redirect(reverse('account:student_profile'))
    if request.user.user_type=='F':
        return redirect(reverse('account:faculty_profile'))


class StudentProfile(TemplateView):
    template_name = 'account/student_profile.html'

    def get_context_data(self, **kwargs):
        active_quizes = Quiz.objects.all().filter(status='P')
        score_cards = self.request.user.score_cards.all()
        context = super(StudentProfile, self).get_context_data(**kwargs)
        context['active_quizes'] = active_quizes
        context['score_cards'] = score_cards
        return context


class FacultyProfile(TemplateView):

	def get(self, request):
		return render(request, 'account/faculty_profile.html')


class ActiveQuizList(ListView):
    queryset = Quiz.objects.filter(status='P')
    template_name = 'account/active_quiz_list.html'
    context_object_name = 'active_quizes'

    # def get_context_data(self, **kwargs):
    #    pass
