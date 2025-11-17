from django.contrib import admin
from .models import Subject, Course, Question, Option

# Register your models here.
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
  list_display = ("subject_id", "name")
  search_fields = ("name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  list_display = ("course_id", "code", "title", "subject", "position")
  list_filter = ("subject",)
  search_fields = ("code", "title")
  autocomplete_fields = ("subject",)
  ordering = ("subject", "position", "course_id")


class OptionInline(admin.TabularInline):
  model = Option
  extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
  list_display = ("question_id", "course", "position", "correct_option")
  list_filter = ("course__subject", "course")
  search_fields = ("question_text",)
  autocomplete_fields = ("course", "correct_option")
  inlines = [OptionInline]
  ordering = ("course", "position", "question_id")


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
  list_display = ("option_id", "question", "position")
  list_filter = ("question__course__subject", "question__course")
  search_fields = ("option_text",)
  autocomplete_fields = ("question",)
  ordering = ("question", "position", "option_id")