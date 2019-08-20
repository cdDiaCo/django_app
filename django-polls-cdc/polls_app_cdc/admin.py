from django.contrib import admin
from .models import Poll, Question, Answer, Results


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer_text', 'answer_score', 'question')
    list_per_page = 12


admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Results)


