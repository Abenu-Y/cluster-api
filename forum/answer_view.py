from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Answer, Question
from django.http import JsonResponse

@api_view(['POST'])
def add_new_answer(request):
    try:
        # Get data from the request body
        answer_text = request.data.get('answer')
        question_id = request.data.get('questionID')

        if not answer_text:
            return Response({'msg': 'Please provide the answer!'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the user ID from the request (assuming the user is authenticated)
        user_id = request.user.userid

        # Check if the question exists
        question = Question.objects.filter(questionid=question_id).first()
        if not question:
            return Response({'msg': 'Question not found!'}, status=status.HTTP_404_NOT_FOUND)

        # Create and save the new answer
        Answer.objects.create(userid_id=user_id, questionid=question, answer=answer_text)

        return Response({'msg': f'A new answer from {request.user.username} has been added to the database.'}, status=status.HTTP_200_OK)

    except Exception as error:
        print(error)
        return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_answers(request, answerdetail):
    try:
        # Fetch answers for the specific question
        answers = Answer.objects.filter(questionid=answerdetail).select_related('userid').order_by('-answerid')
        
        if not answers.exists():
            # If no answers, return the question title and description
            question = Question.objects.filter(questionid=answerdetail).values('title', 'description').first()
            if question:
                return JsonResponse(question, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'msg': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Prepare response with answers and the users who answered
            response = list(answers.values('answer', 'answerid', 'userid__username'))
            return JsonResponse(response, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['DELETE'])
def delete_specific_answer(request, ID, AnsID):
    try:
        # Get the user ID from the request (assuming it's set in request.user)
        userid = request.user.userid

        # Fetch answers for the specific question and filter by the user
        answers = Answer.objects.filter(questionid=ID, answerid=AnsID)

        if not answers.exists():
            return JsonResponse({'msg': 'Answer not found'}, status=status.HTTP_404_NOT_FOUND)

        answer = answers.first()

        if answer.userid.userid == userid:  # Check if the user is the owner of the answer
            answer.delete()  # Delete the answer
            return JsonResponse({'msg': 'Answer successfully deleted'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'msg': 'You do not have access to delete this answer'}, status=status.HTTP_403_FORBIDDEN)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def update_specific_answer(request, UID):
    try:
        # Get data from the request body
        new_answer = request.data.get('newAnswer')
        AID = request.data.get('AID')
        userid = request.user.userid  # Assuming the user is authenticated

        # Check if the new answer content is provided
        if not new_answer:
            return JsonResponse({'error': 'New answer is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the answer by question ID and answer ID
        answer = Answer.objects.filter(questionid=UID, answerid=AID).first()

        if not answer:
            return JsonResponse({'error': 'Answer not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is the owner of the answer
        if answer.userid.userid == userid:
            answer.answer = new_answer  # Update the answer
            answer.save()  # Save the changes
            return JsonResponse({'msg': 'The answer is updated!'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'msg': 'You do not have access to update this answer'}, status=status.HTTP_403_FORBIDDEN)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)