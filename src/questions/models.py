from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    user = models.ForeignKey(User)
    question = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self, ):
        return self.question
    
class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self, ):
        return self.answer
    
    
class UserAnswer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer, null=True, blank=True)
    importance_level = models.CharField(max_length=120, default='Somewhat Important',null=True, blank=True)
    points = models.IntegerField(default='20')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __unicode__(self, ):
        return self.answer.answer
    
    
class MatchAnswer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer, null=True, blank=True)
    importance_level = models.CharField(max_length=120, default='Somewhat Important',null=True, blank=True)
    points = models.IntegerField(default='20')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __unicode__(self, ):
        return self.answer.answer

