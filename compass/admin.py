from django.contrib import admin
from .models import Results, Question, Answer, UserDetails, Quiz, Question_choice, Business_Priority

class QuestionChoiceInline(admin.TabularInline):
    model = Question_choice

class BusinessPriorityInline(admin.TabularInline):
    model = Business_Priority


class ResultsAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'date', 'user_email')
    inlines = [
        QuestionChoiceInline,BusinessPriorityInline,
    ]

    def user_email(self, obj):
        return obj.userdetails.email


class QuizAdmin(admin.ModelAdmin):
    list_display = ('id','name')

admin.site.register(Business_Priority)
admin.site.register(Question_choice)
admin.site.register(UserDetails)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Answer)
admin.site.register(Results, ResultsAdmin)
admin.site.register(Question)