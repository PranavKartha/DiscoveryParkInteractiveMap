from django.db import models
from  datetime import date
# Create your models here.
class PatternManager(models.Manager):
    def basic_validator(self, postData):
        error = {}
        if len(postData['resp']) == 0:
            error['resp'] = "Please Enter your response"
        return error
class AreaManager(models.Manager):
    def basic_validator(self, postData):
        return {}
class Pattern(models.Model):
    Response = models.TextField()
    Trans_Type = models.CharField(max_length = 100)
    Area_Visited = models.CharField(max_length = 100)
    Emotion = models.CharField(max_length = 50)
    Activity = models.CharField(max_length = 50)
    Response_Date = models.DateField(auto_now_add=True)

    object = PatternManager()

class Area(models.Model):
    Area_name = models.CharField(max_length = 100)
    Word_Count = models.TextField()
    Trans_Count = models.TextField()
    Emotion_Count = models.TextField()
    Activity_Count = models.TextField()
    Top5Word_Count = models.TextField()


    object = AreaManager()