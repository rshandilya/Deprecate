from django.urls import path, re_path
from . import views 

app_name = "quiz"

urlpatterns = [
	#path('', views.list_quiz_repos, name='list_repos'),
	path('repo/create/', views.CreateRepository.as_view(), name='create_repo'),
	path('repo/list', views.RepositoryList.as_view(), name='list_repo'),
    re_path(r'^repo/detail/(?P<pk>\d+)/$',
            views.repository_detail, 
            name='repo_detail'),
	re_path(r'^repo/(?P<pk>\d+)/$',
            views.ManageRepository.as_view(), 
            name='manage_repo'),
	re_path(r'^repo/(?P<pk>\d+)/add-module/$',
            views.manage_modules, 
            name='add_modules'),
	re_path(r'^repo/(?P<pk>\d+)/module/(?P<module_pk>\d+)/delete/$',
		    views.delete_module, 
		    name='delete_module'),
	re_path(r'^repo/(?P<pk>\d+)/module/(?P<module_pk>\d+)/add-topics/$',
		    views.add_topics, 
		    name='add_topics'),
	re_path(r'^repo/(?P<pk>\d+)/questions/$', views.RepoQuestions.as_view(), name='repo_questions'),
	re_path(r'^repo/(?P<pk>\d+)/topic/(?P<topic_pk>\d+)/questions/$',
		    views.ListTopicQuestions.as_view(), 
		    name='topic_questions'),
	re_path(r'^repo/(?P<pk>\d+)/topic/(?P<topic_pk>\d+)/add-questions/$',
		    views.add_question, 
		    name='add_question'),
	re_path(r'^repo/(?P<pk>\d+)/topic/(?P<topic_pk>\d+)/delete-question/(?P<quest_pk>\d+)/$',
		    views.delete_question, 
		    name='delete_question'),
	re_path(r'^repo/(?P<pk>\d+)/topic/(?P<topic_pk>\d+)/add-question-to-quiz/(?P<quest_pk>\d+)/$',
		    views.add_question_to_quiz, 
		    name='add_question_to_quiz'),
	re_path(r'^create$', views.CreateQuiz.as_view(), name='create_quiz'),
	re_path(r'^list$', views.ListQuiz.as_view(), name='list_quiz'),
	re_path(r'^(?P<pk>\d+)/detail$',
		    views.QuizDetail.as_view(), 
		    name='quiz_detail'),
	re_path(r'^(?P<quiz_pk>\d+)/remove/question(?P<quest_pk>\d+)/$', 
		    views.remove_question_from_quiz, 
		    name='remove_question_from_quiz'),
	re_path(r'^(?P<pk>\d+)/delete$', 
		    views.QuizDelete.as_view(), 
		    name='delete_quiz'),
	re_path(r'^(?P<pk>\d+)/publish$', 
		    views.publish_quiz, 
		    name='publish_quiz'),
	re_path(r'^start/(?P<quiz_pk>\d+)/$', 
		    views.start_quiz, 
		    name='start_quiz'),
	re_path(r'^fetch-question/(?P<order>\d+)$', 
		    views.fetch_question, 
		    name='fetch_question'),
	re_path(r'^submit/$', 
		    views.submit_quiz, 
		    name='submit_quiz'),
	re_path(r'^exit/$', 
		    views.exit_quiz, 
		    name='exit_quiz'),
]
