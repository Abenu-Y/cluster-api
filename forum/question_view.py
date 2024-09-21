from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .models import Question,User,Answer
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
import secrets
from django.shortcuts import render
from django.db import models 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

def generate_unique_id(length=4):
    return ''.join(secrets.choice('0123456789') for _ in range(length))


@api_view(['POST'])
def addnewquestion(request):
    data = request.data
    userid = request.user.userid
    print(request.user.userid)
    user = get_object_or_404(User, userid=userid)
    
    # Basic validation (you can expand this with more checks)
    if not all(k in data for k in ("title", "description", "tag")):
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)



    # Create the user
    question = Question(
        questionid = generate_unique_id(),
        userid=user,
        title=data['title'],
        description=data['description'],
        tag=data['tag'],
    )
    question.save()

    return Response({"message": f"A new question asked by {request.user.username} is added to the database.."}, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def get_all_questions(request, offset=0, limit=10):
    offset = int(offset)
    limit = int(limit)

    # Using Django ORM to fetch questions with user and answer counts
    questions = (
    Question.objects
    .select_related('userid')  # Assuming `userid` is the ForeignKey to User
    .annotate(num_answers=models.Count('answer'))  # Count the answers related to each question
    .values('userid__username', 'title', 'questionid', 'num_answers')  # Select specific fields
   )[offset:offset + limit]
    
    return Response(list(questions), status=status.HTTP_200_OK)



@api_view(['DELETE'])
def delete_question(request, QID):
    # Get the user ID from the request (assuming it's set in request.user)
    userid = request.user.userid

    # Get the question and check if the user is the owner
    question = get_object_or_404(Question, questionid=QID)
    print(question.userid_id,"yuu")

    if question.userid_id == userid:  # Assuming userid is a ForeignKey to User
        # Delete all answers associated with the question
        Answer.objects.filter(questionid=QID).delete()
        # Delete the question
        question.delete()

        return Response({'msg': 'Question successfully deleted'}, status=status.HTTP_200_OK)
    else:
        return Response({'msg': 'You do not have access to delete this question'}, status=status.HTTP_403_FORBIDDEN)
    


@api_view(['GET'])
def get_question_title_and_description(request, QuestID):
    try:
        # Get the question with its title, description, tag, and associated username
        question = get_object_or_404(Question, questionid=QuestID)
        print("ab",question.title)

        # Assuming 'userid' is a ForeignKey to the User model in Question
        response_data = {
            'title': question.title,
            'description': question.description,
            'tag': question.tag,
            # 'username': question.userid.username  # Accessing the related User's username
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as error:
        print(error)
        return Response({'msg': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def total_question(request):
    try:
        num_questions = Question.objects.count()  # Get the total number of questions
        return Response({'num': num_questions}, status=status.HTTP_200_OK)

    except Exception as error:
        print(error)
        return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['PUT'])
@permission_classes([IsAuthenticated])  # Assuming you want to restrict access to authenticated users
def update_question(request, QID):
    userid = request.user.userid  # Get user ID from the request
    title = request.data.get('title')
    description = request.data.get('description')
    tag = request.data.get('tag')

    # Check if all required fields are provided
    if not title or not description or not tag:
        return Response({'msg': 'Please provide all requirements to update a question'}, status=status.HTTP_400_BAD_REQUEST)

    # Get the question object
    question = get_object_or_404(Question, questionid=QID)

    # Check if the user is the owner of the question
    if question.userid.userid == userid:  # Assuming userid is a ForeignKey to User
        # Update the question fields
        question.title = title
        question.description = description
        question.tag = tag
        question.save()  # Save the updated question

        return Response({'msg': 'Successfully updated!'}, status=status.HTTP_200_OK)
    else:
        return Response({'msg': 'You do not have access to update this question'}, status=status.HTTP_403_FORBIDDEN)    
    

@api_view(['POST'])
def searched_questions(request):
    try:
        search_word = request.data.get('searchWord', '')  # Get the search word from the request

        # Perform the search using Django ORM
        searched_questions = (
            Question.objects
            .filter(title__icontains=search_word)  # Case-insensitive search
            .select_related('userid')  # Assuming userid is a ForeignKey to User
            .annotate(num_answers=Count('answer'))  # Count related answers
            .values('title', 'questionid', 'userid__username', 'num_answers')  # Select specific fields
        )

        return Response(list(searched_questions), status=status.HTTP_200_OK)

    except Exception as error:
        print(error)
        return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)