from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, LoginSerializer, SubjectSerializer, CourseSerializer, QuestionSerializer, OptionSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import Subject, Course, Question, Option

class RegisterView(APIView):
  permission_classes = [AllowAny]

  def post(self, request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      return Response({
        'user': {
          'id': user.id,
          'username': user.username,
          'score': user.score
        }
      }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
  permission_classes = [AllowAny]

  def post(self, request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    from django.contrib.auth import authenticate
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': {
          'id': user.id,
          'username': user.username,
          'score': user.score
        }
      })
    return Response({'error': 'wrong username or password'}, status=status.HTTP_401_UNAUTHORIZED)
# Create your views here.

# Subjects
class SubjectListCreate(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = Subject.objects.all().order_by("name")
        return Response(SubjectSerializer(qs, many=True).data)

    def post(self, request):
        s = SubjectSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

class SubjectDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        obj = get_object_or_404(Subject, pk=pk)
        return Response(SubjectSerializer(obj).data)

    def patch(self, request, pk):
        obj = get_object_or_404(Subject, pk=pk)
        s = SubjectSerializer(obj, data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(Subject, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Courses
class CourseListCreate(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = Course.objects.select_related("subject").all().order_by("subject_id", "position", "course_id")
        subject_id = request.query_params.get("subject")
        if subject_id:
            qs = qs.filter(subject_id=subject_id)
        return Response(CourseSerializer(qs, many=True).data)

    def post(self, request):
        s = CourseSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        obj = get_object_or_404(Course.objects.select_related("subject"), pk=pk)
        return Response(CourseSerializer(obj).data)

    def patch(self, request, pk):
        obj = get_object_or_404(Course, pk=pk)
        s = CourseSerializer(obj, data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(Course, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Questions
class QuestionListCreate(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = (
            Question.objects
            .select_related("course", "correct_option")
            .prefetch_related("options")
            .all()
            .order_by("course_id", "position", "question_id")
        )
        course_id = request.query_params.get("course")
        if course_id:
            qs = qs.filter(course_id=course_id)
        return Response(QuestionSerializer(qs, many=True).data)

    def post(self, request):
        s = QuestionSerializer(data=request.data)
        if s.is_valid():
            try:
                obj = s.save()
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(QuestionSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        obj = get_object_or_404(
            Question.objects.select_related("course", "correct_option").prefetch_related("options"),
            pk=pk,
        )
        return Response(QuestionSerializer(obj).data)

    def patch(self, request, pk):
        obj = get_object_or_404(Question, pk=pk)
        s = QuestionSerializer(obj, data=request.data, partial=True)
        if s.is_valid():
            try:
                s.save()
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(Question, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Options
class OptionListCreate(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = Option.objects.select_related("question").all().order_by("question_id", "position", "option_id")
        question_id = request.query_params.get("question")
        if question_id:
            qs = qs.filter(question_id=question_id)
        return Response(OptionSerializer(qs, many=True).data)

    def post(self, request):
        s = OptionSerializer(data=request.data)
        if s.is_valid():
            try:
                obj = s.save()
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(OptionSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

class OptionDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        obj = get_object_or_404(Option.objects.select_related("question"), pk=pk)
        return Response(OptionSerializer(obj).data)

    def patch(self, request, pk):
        obj = get_object_or_404(Option, pk=pk)
        s = OptionSerializer(obj, data=request.data, partial=True)
        if s.is_valid():
            try:
                s.save()
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(Option, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
