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
    path('events/dashboard/',views.organizer_dashboard ,name='dashboard'),
    path('events/<int:event_id>/book/',views.event_book ,name='event-book'),
    path('events/<int:event_id>/delete/',views.event_delete ,name='event-delete'),
    path('events/deletex/<int:book_id>',views.book_delete ,name='book-delete'),
    path('events/update/<int:user_id>/',views.user_update ,name='user-update'),
]