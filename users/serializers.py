from rest_framework import serializers
from .models import User, Subject, Course, Question, Option

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, min_length=6)
  class Meta:
    model = User
    fields = ['username', 'password', 'score']

  def create(self, validated_data):
    user = User.objects.create_user(
      username = validated_data["username"],
      password = validated_data["password"],
      score = validated_data.get('score', 0)
    )
    return user

class LoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField(write_only=True)

class OptionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Option
    fields = ("option_id", "question", "option_text", "position")
    read_only_fields = ("option_id",)


class QuestionSerializer(serializers.ModelSerializer):
  options = OptionSerializer(many=True, read_only=True)
  class Meta:
    model = Question
    fields = (
      "question_id",
      "course",
      "question_text",
      "position",
      "correct_option",
      "options",
    )
    read_only_fields = ("question_id",)

  def validate(self, attrs):
    correct_option = attrs.get("correct_option")
    course = attrs.get("course") or getattr(self.instance, "course", None)
    if correct_option is not None:
      q = self.instance or Question(course=course)
      if correct_option.question_id and correct_option.question_id != getattr(q, "question_id", None):
        raise serializers.ValidationError({"correct_option": "Correct option must belong to this question."})
    return attrs


class CourseSerializer(serializers.ModelSerializer):
  questions = QuestionSerializer(many=True, read_only=True)

  class Meta:
    model = Course
    fields = (
      "course_id",
      "subject",
      "code",
      "title",
      "description",
      "difficulty",
      "position",
      "questions",
    )
    read_only_fields = ("course_id",)


class SubjectSerializer(serializers.ModelSerializer):
  courses = CourseSerializer(many=True, read_only=True)

  class Meta:
    model = Subject
    fields = ("subject_id", "name", "description", "courses")
    read_only_fields = ("subject_id",)