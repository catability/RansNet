from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from users.serializers import UserSerializer
from users.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import jwt

SECRET = settings.SECRET_KEY


# @csrf_exempt
@api_view(["GET", "POST"])
def user_login(request):
    if request.method == "GET":
        data = {"message": "This is login page"}
        return JsonResponse(data)

    elif request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user and check_password(password, user.password):
            token, created = Token.objects.get_or_create(user=user)

            access_token = jwt.encode({"id": user.pk}, SECRET, algorithm="HS256")
            header = jwt.decode(access_token, SECRET, algorithms="HS256")
            return Response(
                {"token": token.key, "access_token": access_token, "header": header}
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


@csrf_exempt
@api_view(["GET", "POST"])
def user_sign(request):
    # username = request.GET.get("username")

    # if username:
    #     return check_username(request)

    if request.method == "GET":
        data = {"message": "This is signup page"}
        return JsonResponse(data)

    elif request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get("password")
            encrypted_password = make_password(password)
            serializer.validated_data["password"] = encrypted_password
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def check_username(request):
    username = request.GET.get("username")

    if not username:
        return Response(
            {"error": "Please provide a username."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.get(username=username)
        return Response(
            {"message": "Username is already taken."},
            status=status.HTTP_200_OK,
        )
    except User.DoesNotExist:
        return Response(
            {"message": "Username is available."},
            status=status.HTTP_200_OK,
        )


@api_view(["GET", "PUT"])
# @permission_classes([IsAuthenticated])
def mypage(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    if auth_header and auth_header.startswith("Token "):
        token = auth_header.split(" ")[1]
        try:
            decoded_token = jwt.decode(token, SECRET, algorithms=["HS256"])
            user_id = decoded_token.get("id")
            # 여기서 user_id를 활용하여 사용자 정보를 가져오거나 처리할 수 있습니다.
            user = User.objects.get(id=user_id)
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Token expired"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.DecodeError:
            return Response(
                {"error": "Token decode error"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(
            {"error": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # elif request.method == "DELETE":
    #     # Check if the user has related data (e.g., reports) before deleting
    #     if user.reports.exists():
    #         return Response(
    #             {"error": "Cannot delete user with related data."},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
    #     user.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
