from django.db import models
from django.conf import settings
import datetime

# Create your models here.

class Subject(models.Model):   # Repository
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, 
                              on_delete='models.CASCADE', 
                              related_name='repos')

    def get_modules(self):
        modules = Module.objects.filter(subject=self)
        return modules

    def __str__(self):
        return self.title


class Repository(Subject):
    class Meta:
        proxy = True


class Module(models.Model):
    title = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='modules')

    def __str__(self):
        return self.title


class Topic(models.Model):
    title = models.CharField(max_length=100)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Question(models.Model):
    topic = models.ForeignKey(Topic, models.CASCADE)
    question = models.TextField(max_length=1000)
    explanation = models.TextField(max_length=1000, blank=True, null=True)

    def get_ans_choice(self):
        ans_set = Answer.objects.filter(question=self)
        return [(x.id,x.answer) for x in ans_set ]

    def right_ans(self):
        return Answer.objects.filter(question=self, is_correct=True)

    def given_ans(self, guess):
        return Answer.objects.get(id=guess)

    def check_ans(self, guess):
        ans = Answer.objects.get(id=guess)
        return ans.is_correct



class Answer(models.Model):
    question = models.ForeignKey(Question, 
                                 on_delete=models.CASCADE, 
                                 related_name="answers")
    answer = models.CharField(max_length=500)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.answer


class Quiz(models.Model):
    STATUS = (
        ('U', 'unpublished'),
        ('P', 'published'),
        ('E', 'expired'),
    )
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    created_on  = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    questions = models.ManyToManyField(Question, through="Pattern")
    last_published = models.DateTimeField(null=True)
    #duration = models.DurationField(help_text="*duration is in minutes")
    duration = models.PositiveSmallIntegerField(help_text="*duration is in minutes")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, 
                               on_delete='models.CASCADE',
                               limit_choices_to={'user_type': 'F'},
                               related_name='quizes')
    status = models.CharField(max_length=1, choices=STATUS, default='U')

    def __str__(self):
        return self.title

    def get_published(self):
        self.status = 'P'
        self.last_published = datetime.datetime.now()
        self.save()

    def get_questions(self):
        pat = Pattern.objects.filter(quiz=self)
        question_set = [p.question for p in pat]
        return question_set

    def count_questions(self):
        count = len(self.get_questions())
        return count

    def get_marks(self, q_pk):
        qn = Question.objects.get(id=q_pk)
        p = Pattern.objects.get(quiz=self, question=qn)
        return (p.mark, p.negative_mark)

    def get_total_marks(self):
        q_set = self.get_questions()
        total = sum([self.get_marks(q.id)[0] for q in q_set])
        return total 


class Pattern(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    mark = models.PositiveSmallIntegerField()
    negative_mark = models.DecimalField(max_digits=4, 
                                        decimal_places=2,
                                        help_text="in fraction")
    

class ScoreCard(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                on_delete='models.CASCADE',
                                limit_choices_to={'user_type': 'S'},
                                related_name='score_cards')
    quiz_title = models.CharField(max_length=50)
    quiz_code = models.CharField(max_length=10)
    total_marks = models.PositiveSmallIntegerField()
    obtained_marks = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    total_candidate = models.PositiveSmallIntegerField(null=True)
    rank = models.PositiveSmallIntegerField(null=True)
    date = models.DateField(auto_now_add=True)


class ScorePoints(models.Model):
    score_card = models.ForeignKey(ScoreCard, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_given = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    mark_obtained = models.DecimalField(max_digits=3, decimal_places=2)
