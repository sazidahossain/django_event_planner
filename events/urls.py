from django.urls import path
from .views import Login, Logout, Signup, home
from events import views
urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('events/create/',views.event_create ,name='event-create'),
    path('events/list/',views.event_list ,name='event-list'),
    path('events/<int:event_id>/detail/',views.event_detail ,name='event-detail'),
    path('no-access/',views.no_access ,name='no-access'),
    path('events/<int:event_id>/update/',views.event_update ,name='event-update'),
]