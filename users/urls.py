from django.urls import path
from .views import RegisterView, LoginView, SubjectListCreate, SubjectDetail, CourseListCreate, CourseDetail, QuestionListCreate, QuestionDetail, OptionListCreate, OptionDetail

urlpatterns = [
  path('register/', RegisterView.as_view(), name='register'),
  path('login/', LoginView.as_view(), name='login'),

  # your existing auth endpoints
  path("auth/register/", RegisterView.as_view(), name="register"),
  path("auth/login/", LoginView.as_view(), name="login"),

  # new endpoints
  path("subjects/", SubjectListCreate.as_view(), name="subject-list"),
  path("subjects/<int:pk>/", SubjectDetail.as_view(), name="subject-detail"),

  path("courses/", CourseListCreate.as_view(), name="course-list"),
  path("courses/<int:pk>/", CourseDetail.as_view(), name="course-detail"),

  path("questions/", QuestionListCreate.as_view(), name="question-list"),
  path("questions/<int:pk>/", QuestionDetail.as_view(), name="question-detail"),

  path("options/", OptionListCreate.as_view(), name="option-list"),
  path("options/<int:pk>/", OptionDetail.as_view(), name="option-detail")
]