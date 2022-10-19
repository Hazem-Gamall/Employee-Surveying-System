
from urllib import request
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Survey, EmployeeSurvey, Answer
from .serializers import AnswerSerializer, SurveySerializer, EmployeeSurveySerializer, QuestionSerializer
from employee.models import Employee
from .tasks import notify_employees
import datetime

today = datetime.date.today()


class SurveyViewSet(RetrieveModelMixin,
                    UpdateModelMixin,
                    ListModelMixin,
                    CreateModelMixin,
                    GenericViewSet):
    # queryset = Answer.objects.all()
    serializer_class = EmployeeSurveySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        employee_object = self.request.user.employee
        return employee_object.survey_set.filter(survey__start_date__lte=today)

    @action(detail=True, methods=['GET', 'POST', 'PATCH'], permission_classes=[IsAuthenticated])
    def SubmitAnswer(self, request, pk):
        # if request.method == 'GET':
        #     employee_survey = EmployeeSurvey.objects.get(pk=pk)
        #     questions = employee_survey.survey.questions.all()
        #     serializer = QuestionSerializer(questions, many=True)
        #     return Response(serializer.data)
        if request.method == 'POST':
            employee_object = self.request.user.employee
            employee_survey = employee_object.survey_set.get(id=pk)
            if employee_survey.survey.is_expired:
                return Response({'errors': 'You cannot submit answers because This Survey was ended!'})
            if employee_survey.answers.all():
                return Response({'error':'you post answers already, you need to use patch method'})

            else:

                if employee_survey.survey.questions.count() == len(request.data):
            
                    serializer = AnswerSerializer(data=request.data, many=True)
                    serializer.is_valid(raise_exception=True)
                    answers = serializer.save()
                    employee_survey = EmployeeSurvey.objects.get(pk=pk)
                    survey_questions = employee_survey.survey.questions.all()
                    for answer in answers:
                        if answer.question not in survey_questions:
                            return Response({'errors': 'This Question Not in This Survey '})
                        employee_survey.answers.add(answer)
                    employee_survey.is_submitted = 'True'
                    employee_survey.save()
                    return Response(serializer.data)
                else:
                    return Response('Please, Answer All questions') 


        elif request.method == 'PATCH':
            employee_object = self.request.user.employee
            employee_survey = employee_object.survey_set.get(id=pk)
            if not employee_survey.answers.all():
                return Response({'error':'you need to post answers before using patch method!'})
            if employee_object.survey_set.get(id=pk).survey.is_expired:
                return Response({'errors': 'You cannot submit answers because This Survey was ended!'})

            answers = request.data
            employee_survey = EmployeeSurvey.objects.get(pk=pk)
            survey_questions = employee_survey.survey.questions.all()
            for answer in answers:
                if answer['question'] not in survey_questions.values_list('id', flat=True):
                    return Response({'errors': 'This Question Not in This Survey '})

            serializer = AnswerSerializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            if employee_object.survey_set.get(id=pk).answers.all():
                for answer in request.data:
                    answer_object = employee_survey.answers.get(
                        question__id=answer['question'])
                    answer_object.rating = answer['rating']
                    answer_object.save()
                # employee_survey.answers.add(answer)
            
            employee_survey.is_submitted = 'True'
            employee_survey.save()


            return Response(serializer.data)
