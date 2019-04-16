from django.contrib import admin
from .models import Results, Question, Answer, UserDetails, Quiz


class ResultsAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'answer_list', 'date', 'user_email')
    # readonly_fields = ('userdetails',)

    def user_email(self, obj):
        return obj.userdetails.email


class QuizAdmin(admin.ModelAdmin):
    list_display = ('id','name')


admin.site.register(UserDetails)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Answer)
admin.site.register(Results, ResultsAdmin)
admin.site.register(Question)