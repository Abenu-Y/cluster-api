from rest_framework import serializers
from .models import User,Question,Answer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userid', 'username', 'firstname', 'lastname', 'email'] 


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id','questionid','userid','title','description','created_at','tag']       


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['answerid','questionid','userid','answer']           