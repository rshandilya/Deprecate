from django import forms
from .models import Subject, Module, Topic, Question, Answer, Quiz
from django.forms.widgets import RadioSelect, CheckboxInput
from django.forms.models import BaseModelFormSet


class RepoForm(forms.ModelForm):
	class Meta:
		model = Subject
		fields = ('title', 'slug')	


class ModuleForm(forms.ModelForm):
	class Meta:
		model = Module
		fields = ('title',)


class TopicForm(forms.ModelForm):
	class Meta:
		model = Topic
		fields = ('title',)


class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ('question', 'explanation',)
		

class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ('answer', 'is_correct')

class AnswerFormSet(BaseModelFormSet):
	def __init__(self, *args, **kwargs):
		super(AnswerFormSet, self).__init__(*args, **kwargs)
		self.queryset = Answer.objects.none()
		self.fields = ('answer', 'is_correct')
		self.extra = 4


class QuizForm(forms.ModelForm):
	class Meta:
		model = Quiz
		fields = ('title', 'code', 'duration')


class FillQuizForm(forms.Form):
	mark = forms.IntegerField()
	negative_mark = forms.DecimalField(min_value=0, decimal_places=2, max_value=1)

	def __init__(self, *args, **kwargs):
		super(FillQuizForm,self).__init__(*args, **kwargs)
		quiz_option = Quiz.objects.all()
		choice_list = [(q.id, q.title) for q in quiz_option]
		self.fields['quiz'] = forms.ChoiceField(choices=choice_list)


class TestQuestionForm(forms.Form):
	def __init__(self, question, *args, **kwargs):
		super(TestQuestionForm, self).__init__(*args, **kwargs)
		choice_list = question.get_ans_choice()
		self.fields["answers"] = forms.ChoiceField(choices=choice_list,
                                                   widget=RadioSelect)

class MCQForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(MCQForm, self).__init__(*args, **kwargs)
        choice_list = question.get_ans_choice()
        self.fields["answers"] = forms.ChoiceField(choices=choice_list,
                                                   widget=RadioSelect)
	
        
        
        
