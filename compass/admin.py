""" The admin file to edit what to display and how on admin page. """
from django.contrib import admin
from .models import Results, Question, Answer,\
    UserDetails, Quiz, Question_choice, Business_Priority, Category

class QuestionChoiceInline(admin.TabularInline):
    """ Display the model QuestionChoice inline for results. """
    model = Question_choice

class BusinessPriorityInline(admin.TabularInline):
    """ Display the model BusinessPriority inline for results. """
    model = Business_Priority


class ResultsAdmin(admin.ModelAdmin):
    """ List of what to display in Results, adding email and classes above. """
    list_display = ('id', 'quiz', 'date', 'user_email')
    inlines = [
        QuestionChoiceInline, BusinessPriorityInline,
    ]

    @staticmethod
    def user_email(self, obj):
        """ Return the userdetails email for viewing in admin. """
        return obj.userdetails.email


class QuizAdmin(admin.ModelAdmin):
    """ List of what to display in Quiz. """
    list_display = ('id', 'name')


admin.site.register(Business_Priority)
admin.site.register(Question_choice)
admin.site.register(UserDetails)
admin.site.register(Category)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Answer)
admin.site.register(Results, ResultsAdmin)
admin.site.register(Question)
