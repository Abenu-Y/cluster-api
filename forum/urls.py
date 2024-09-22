from django.urls import path
from .views import registerUser,loginUser,checkUser,question
from .question_view import addnewquestion,get_all_questions,delete_question,get_question_title_and_description,total_question,update_question,searched_questions

from .answer_view import add_new_answer,get_answers,delete_specific_answer,update_specific_answer



urlpatterns = [
    path('users/register/', registerUser),
    path('users/login/', loginUser),
    path('users/check/',checkUser),
    path('users/abene/',question),
    path('questions/new-question/',addnewquestion),
    path('question/getallquestions/<int:offset>/<int:limit>/',get_all_questions),
    path('questions/delete/<int:QID>',delete_question),
    path('questions/titdescription/<int:QuestID>',get_question_title_and_description),
    path('questions/noOfquestion',total_question),
    path('questions/update/<int:QID>',update_question),
    path('questions/searchedquestion',searched_questions),
    path('answers/new-answer',add_new_answer),
    path('answers/<str:answerdetail>',get_answers),
    path('answers/delete/<int:ID>/<int:AnsID>', delete_specific_answer),
    path('answers/update/<int:UID>',update_specific_answer)
]