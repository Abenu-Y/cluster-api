from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate
import jwt
from django.conf import settings

@api_view(['POST'])
def registerUser(request):
    data = request.data
    
    # Basic validation (you can expand this with more checks)
    if not all(k in data for k in ("username", "password", "firstname", "lastname", "email")):
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the username or email already exists
    if User.objects.filter(username=data['username']).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=data['email']).exists():
        return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user
    user = User(
        username=data['username'],
        firstname=data['firstname'],
        lastname=data['lastname'],
        email=data['email'],
    )
    user.set_password(data['password'])  # Hash the password
    user.save()

    return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)



User = get_user_model()
@csrf_exempt
@api_view(['POST'])
def loginUser(request):
    data = request.data
    try:
        user = User.objects.get(username=data['username'])  # Get the user by username
        print(user)
        if check_password(data['password'], user.password):  # Check if password matches
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)  # Generate access token

            return Response({
                'msg': 'User successfully logged in',
                'refresh': str(refresh),
                'token': access_token,
                'username': user.username  # Include username in the response
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    # data = request.data
    # user = authenticate(username=data['username'], password=data['password'])
    # print(user.username, user.userid)

    # if user is not None:
    #     # Create token
    #     token = jwt.encode(
    #         {'username': user.username, 'user_id': user.userid},
    #         settings.SECRET_KEY,
    #         algorithm='HS256'
    #     )
    #     return Response({'msg': 'User successfully logged in', 'token': token, 'username': user.username}, status=status.HTTP_200_OK)
    # else:
    #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def question(request):
    return Response({"msg":"Abenezer"})




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checkUser(request):
    return Response({"message": f"Hello, {request.user.username}!"})