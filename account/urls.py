from django.urls import path, re_path
from . import views

app_name = 'account'
urlpatterns = [
	# path('signup', views.SignUp.as_view(), name='signup'),
	# path('signup/student/', views.StudentSignUp.as_view() , name='student_signup'),
	# path('signup/faculty/', views.FacultySignUp.as_view(), name='faculty_signup'),
	path('profile', views.profile, name='profile'),
	path('profile/students/', views.StudentProfile.as_view(), name='student_profile'),
	path('profile/students/active-quizes',
         views.ActiveQuizList.as_view(),
         name='active_quizes'),
	path('profile/faculty/', views.FacultyProfile.as_view(), name='faculty_profile'),
]
