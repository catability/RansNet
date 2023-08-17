from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from reports.models import Report
from reports.serializers import ReportSerializer
import jwt
from django.conf import settings
from users.models import User

SECRET = settings.SECRET_KEY


@csrf_exempt
@api_view(["GET", "POST"])
def report_register(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    if auth_header and auth_header.startswith("Token "):
        token = auth_header.split(" ")[1]
        try:
            decoded_token = jwt.decode(token, SECRET, algorithms=["HS256"])
            user_id = decoded_token.get("id")
            user = User.objects.get(id=user_id)  # 사용자 정보 가져오기
        except jwt.ExpiredSignatureError:
            return JsonResponse(
                {"error": "Token expired"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.DecodeError:
            return JsonResponse(
                {"error": "Token decode error"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
    else:
        return JsonResponse(
            {"error": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if request.method == "GET":
        data = {"message": "This is report page"}
        return JsonResponse(data)
    elif request.method == "POST":
        # data = JSONParser().parse(request)
        data = request.data
        data["report_account"] = user.id  # 현재 사용자를 신고 계정으로 설정
        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# # @api_view(["GET", "POST"])
# def report_register(request):
#     if request.method == "GET":
#         data = {"message": "This is report page"}
#         return JsonResponse(data)

#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = ReportSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET", "POST"])
# def report_register(request):
#     if request.method == "GET":
#         data = {"message": "This is report page"}
#         return Response(data, content_type="application/json")


# @csrf_exempt
def report_list(request):
    if request.method == "GET":
        reports = Report.objects.filter(is_deleted=False)
        serializer = ReportSerializer(reports, many=True)
        return JsonResponse(serializer.data, safe=False)


# @api_view(["GET"])
# def report_list(request):
#     if request.method == "GET":
#         reports = Report.objects.filter(is_deleted=False)
#         serializer = ReportSerializer(reports, many=True)
#         return Response(serializer.data)


@csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
def report_detail(request, pk):
    try:
        report = Report.objects.get(pk=pk, is_deleted=False)
    except Report.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ReportSerializer(report)
        return JsonResponse(serializer.data)

    else:
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header and auth_header.startswith("Token"):
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

        if request.method == "PUT":
            # Check if the user is the author of the report
            if report.report_account.id != user_id:
                return Response(
                    {"error": "You do not have permission to update this report."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            data = JSONParser().parse(request)
            serializer = ReportSerializer(report, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "DELETE":
            # Check if the user is the author of the report
            if report.report_account.id != user_id:
                return Response(
                    {"error": "You do not have permission to delete this report."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            report.is_deleted = True
            report.save()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
