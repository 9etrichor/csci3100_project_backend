from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class UserManager(BaseUserManager):
  def create_user(self, username, password=None, **extra_fields):
    if not username:
      raise ValueError("No username")
    user = self.model(username=username, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self, username, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault("is_superuser", True)
    return self.create_user(username, password,**extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(max_length=50, unique=True)
  score = models.IntegerField(default=0)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  objects = UserManager()

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = []
  def __str__(self):
    return self.username

# subject
class Subject(models.Model):
  subject_id = models.BigAutoField(primary_key=True)
  name = models.CharField(max_length=120, unique=True)
  description = models.TextField(blank=True, null=True)

  class Meta:
    db_table = "subject"
    ordering = ["name"]

  def __str__(self):
    return self.name


class Course(models.Model):
  course_id = models.BigAutoField(primary_key=True)
  subject = models.ForeignKey(
    Subject,
    on_delete=models.PROTECT,   # prevent deleting a subject that has courses
    related_name="courses",
  )
  code = models.CharField(max_length=32, unique=True)  # e.g., GIT101
  title = models.CharField(max_length=200)
  description = models.TextField(blank=True, null=True)
  difficulty = models.CharField(max_length=50, blank=True, null=True)
  position = models.PositiveIntegerField(blank=True, null=True)  # order within subject

  class Meta:
    db_table = "course"
    ordering = ["subject_id", "position", "course_id"]
    
    constraints = [
      models.UniqueConstraint(fields=["subject", "position"], name="uq_course_subject_position"),
    ]

  def __str__(self):
    return f"{self.code} - {self.title}" if self.code else self.title


class Question(models.Model):
  question_id = models.BigAutoField(primary_key=True)
  course = models.ForeignKey(
    Course,
    on_delete=models.CASCADE,   # deleting a course deletes its questions
    related_name="questions",
  )
  question_text = models.TextField()
  position = models.PositiveIntegerField()  # order within course

  # One correct option per question (nullable until set).
  correct_option = models.ForeignKey(
    "Option",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="correct_for_questions",
  )

  class Meta:
    db_table = "question"
    ordering = ["course_id", "position", "question_id"]
    constraints = [
      models.UniqueConstraint(fields=["course", "position"], name="uq_question_course_position"),
    ]

  def __str__(self):
    return f"Q{self.position} ({self.course.code or self.course_id})"

  def clean(self):
    super().clean()
    # Enforce that correct_option belongs to this question (when set).
    if self.correct_option_id and self.correct_option.question_id != self.question_id:
      from django.core.exceptions import ValidationError
      raise ValidationError({"correct_option": "Correct option must belong to this question."})


class Option(models.Model):
  option_id = models.BigAutoField(primary_key=True)
  question = models.ForeignKey(
    Question,
    on_delete=models.CASCADE,   # deleting a question deletes its options
    related_name="options",
  )
  option_text = models.TextField()
  position = models.PositiveIntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(4)]
  )  # 1–4 unique within question

  class Meta:
    db_table = "option"
    ordering = ["question_id", "position", "option_id"]
    constraints = [
      models.UniqueConstraint(fields=["question", "position"], name="uq_option_question_position"),
    ]

  def __str__(self):
    return f"Option {self.position} of Q{self.question_id}"