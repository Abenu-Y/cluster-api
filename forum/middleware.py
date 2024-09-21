from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from jwt import ExpiredSignatureError, InvalidTokenError


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        

    def __call__(self, request):
        # Define the paths that require JWT authentication
        protected_paths = ['/api/questions/', '/api/answers/', '/api/users/check/']
        # Only apply the middleware if the request path starts with one of the protected paths
        if any(request.path.startswith(path) for path in protected_paths):
            auth_header = request.headers.get('Authorization')

            if not auth_header or not auth_header.startswith('Bearer'):
                return JsonResponse({'msg': 'NO AUTHORIZATION'}, status=401)
            
            token = auth_header.split(' ')[1] if ' ' in auth_header else None

            if token == 'null':
                return JsonResponse({'msg': 'NULL AUTHORIZATION'}, status=401)
            
            try:
                # Initialize JWTAuthentication instance
                jwt_auth = JWTAuthentication()

                # Validate the token (this decodes the JWT)
                validated_token = jwt_auth.get_validated_token(token)

                # Get the user associated with the token
                user = jwt_auth.get_user(validated_token=validated_token)

                # Attach the user to the request
                request.user = user
            except (AuthenticationFailed, ExpiredSignatureError, InvalidTokenError):
                return JsonResponse({'msg': 'INVALID TOKEN'}, status=401)
            
            

        # Continue processing the request
        # print("continue..")
        response = self.get_response(request)
        # print(response)
        # print("upto this ...")
        return response