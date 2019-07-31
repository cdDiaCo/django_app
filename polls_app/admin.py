from django.contrib import admin

# Register your models here.

from .models import Poll, Question, Answer, Results


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer_text', 'answer_score', 'question')
    #search_fields = ('answer_text', 'question')
    list_per_page = 12


admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Results)


