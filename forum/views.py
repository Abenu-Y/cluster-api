from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model



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
        print(user , check_password(data['password'],user.password))
        if check_password(data['password'], user.password):  # Check if password matches
            refresh = RefreshToken.for_user(user)  # Generate tokens
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)