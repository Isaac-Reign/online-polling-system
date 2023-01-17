from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', views.vote_home, name='poll_board'),
	path('poll/messages/', views.messages_section, name='messages'),
	path('please_login/', views.please_login, name='please_login'),
	path('create_poll/', views.create_poll, name='create_poll'),
	path('vote/', views.vote, name='vote'),
	path('submit_vote/<poll_id>/', views.submit_vote, name='submit_vote'),
	path('poll_results/', views.result_home, name='poll_results'),
	path('delete_poll/', views.delete_poll, name='delete_poll'),
	path('results/', views.results, name='results'),
	path('about/', views.about, name='about'),
	path('voters/', views.voters, name='voters'),
	path('can_vote/<person_id>/', views.can_vote, name='can_vote'),



	path('login_user/', views.login_user, name='login_user'),
	path('register_user/', views.register_user, name='register_user'),
	path('complete_registration/', views.complete_registration, name='complete_registration'),
	path('logout_user/', views.logout_user, name='logout_user'),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
