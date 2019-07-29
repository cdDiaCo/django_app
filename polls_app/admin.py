from django.contrib import admin

# Register your models here.

from .models import Poll, Question, Answer, Results

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Results)


