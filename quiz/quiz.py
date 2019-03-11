from django.conf import settings
from .models import Quiz, Question, ScoreCard, ScorePoints, Answer
from decimal import Decimal
import time


class AllAttempt(Exception):
    pass


class ActiveQuiz(object):
    def __init__(self, request):
        self.session = request.session
        active_quiz = self.session.get(settings.ACTIVE_QUIZ_SESSION_ID)
        if not active_quiz:
            active_quiz = self.session[settings.ACTIVE_QUIZ_SESSION_ID] = {}
        self.active_quiz = active_quiz

    def stuff_questions(self, quiz_pk):
        quiz = Quiz.objects.get(id=quiz_pk)
        #self.session.set_expiry(60)
        question_set = quiz.get_questions()
        question_count = len(question_set)
        self.active_quiz['questions'] = {str(i+1): question_set[i].id for i in range(question_count)}
        self.active_quiz['response'] =  {str(i+1): None for i in range(question_count)}
        self.active_quiz['detail'] = {'code': quiz.code, 
                                      'title': quiz.title, 
                                      'duration': quiz.duration * 60,
                                      'start_time': time.monotonic(),
                                      'total_marks': quiz.get_total_marks()}

    def is_live(self):
        current = time.monotonic()
        start = self.active_quiz['detail']['start_time']
        duration = self.active_quiz['detail']['duration']
        if current - start < duration:
            return True
        

    def get_questions_order(self):
        orders = [int(i) for i in self.active_quiz['questions'].keys()]
        return orders

    def get_question(self, order):
        order = str(order)
        questions = self.active_quiz['questions']
        quest_id = questions[order]
        question = Question.objects.get(id=quest_id)
        return (int(order), question)

    def get_next_question(self, order):
        response = self.active_quiz['response']
        unattempts = [i+1 for i in range(len(response)) if not response[str(i+1)]] 
        if unattempts:
            for v in unattempts:
                if v > order:
                    return v
            return unattempts[0]
        else:
            raise AllAttempt()

        
    def update_response(self, order, resp):
        user_response = self.active_quiz['response']
        user_response[str(order)] = int(resp)
        self.save()

    def get_response(self, order):
        user_response = self.active_quiz['response']
        return user_response[str(order)]

    def get_summary(self):
        questions = self.active_quiz['questions']
        answers = self.active_quiz['response']
        no_attempt = len(answers)
        no_correct = 0
        for i in range(len(questions)):
            if answers[str(i+1)]:
                question = Question.objects.get(id=questions[str(i+1)])
                ans = answers[str(i+1)]
                if question.check_ans(ans):
                    no_correct = no_correct + 1
            else:
                no_attempt = no_attempt - 1
        return (len(questions), no_attempt, no_correct)

    def get_score(self, request):
        detail = self.active_quiz['detail']
        questions = self.active_quiz['questions']
        response = self.active_quiz['response']
        score_card = ScoreCard.objects.create(student=request.user, 
                                              quiz_title=detail['title'],
                                              quiz_code=detail['code'],
                                              total_marks=detail['total_marks'])

        for i in range(len(questions)):
            qn = Question.objects.get(id=questions[str(i+1)])
            res = response[str(i+1)]
            if res:
                ans = Answer.objects.get(id=res)
            else:
                ans = None
            code = detail['code']
            quiz = Quiz.objects.get(code=code)
            mk = quiz.get_marks(qn.id)
            if res:
                if qn.check_ans(res):                    
                    mark_obtained = round(Decimal(mk[0]),2)
                else:
                    mark_obtained = -mk[1]*mk[0]
                    mark_obtained = round(mark_obtained,2)
            else:
                mark_obtained = round(Decimal(0),2)
            ScorePoints.objects.create(score_card=score_card,
                                       question=qn,
                                       answer_given=ans,
                                       mark_obtained=mark_obtained)
        sp = ScorePoints.objects.filter(score_card=score_card)
        sp_list = [x.mark_obtained for x in sp]
        score_card.obtained_marks = sum(sp_list)
        score_card.save()
        return score_card

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.ACTIVE_QUIZ_SESSION_ID]
        self.save()

