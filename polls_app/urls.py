from django.urls import path

from . import views


app_name = 'polls_app'

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:poll_id>/', views.detail, name='poll_detail'),
    path('<int:poll_id>/submit/', views.submit, name='poll_submit'),
    path('<int:poll_id>/<int:total_score>/results/', views.results, name='poll_results'),
]




