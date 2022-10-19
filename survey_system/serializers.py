from dataclasses import field
from rest_framework import serializers
from .models import Answer, Survey , EmployeeSurvey, Questions

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['id', 'description']
class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    is_expired = serializers.SerializerMethodField()
    class Meta:
        model = Survey
        fields = ['id','survey_type', 'end_date', 'start_date', 'description', 'title', 'questions', 'is_expired']

    def get_is_expired(self, obj):
        return obj.is_expired
class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['rating', 'question']
class EmployeeSurveySerializer(serializers.ModelSerializer):
    rater = serializers.StringRelatedField()
    get_rated = serializers.StringRelatedField()
    answers = AnswerSerializer(many=True)
    survey = SurveySerializer()
    class Meta:
        model = EmployeeSurvey
        fields = ['id','is_submitted', 'rater', 'get_rated', 'survey', 'submited_date', 'answers']
class WebsocketEmployeeSurveySerializer(serializers.ModelSerializer):
    rater = serializers.StringRelatedField()
    get_rated = serializers.StringRelatedField()
    survey = SurveySerializer()
    url = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeSurvey
        fields = ['id', 'rater', 'get_rated','url', 'survey']

    def get_url(self, obj):
        return obj.get_absolute_url()