from .redis.async_redis_utils import create_game_in_redis, get_lobbies
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the token to log out the user
        request.auth.delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')  # Optional

        # Validate required fields
        if not username or not password:
            return Response({"message": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return Response({"message": "Username is already taken try again."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user:
            # Create or retrieve the user's token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful",
                "token": token.key,
                "username": user.username
            }, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# async def join(request):
#     asd = json.loads(request.body)
#     return JsonResponse({"message": "ok"})

@ensure_csrf_cookie
def csrf_init(request): # We use this endpoint in order to set a csrf cookie for the frontend
    return JsonResponse({"detail": "CSRF cookie set"})

async def lobbies(request):
    lobbies = await get_lobbies()
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        "games_broadcast",
            {
                "type": "new.game",
                "game_data": lobbies
    })
    return JsonResponse({"message": "ok"})
async def send(request): # NOT USED RIGHT?
    print(request)
    return JsonResponse({"message": "ok"})

async def start(request): # NOT USED RIGHT?
    print(request)
    return JsonResponse({"message": "ok"})

async def create(request):
    game_id = await create_game_in_redis()
    print("Game Created!")
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        "games_broadcast",
            {
                "type": "new.game",
                "game_data": [{"game_id": str(game_id), "players":[], "state":"open"}]
            })
    return JsonResponse({"message": "ok"})
