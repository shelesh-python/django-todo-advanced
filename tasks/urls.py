from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view),
    path('logout/', views.logout_view),

    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('add/', views.add_task),
    path('toggle/<int:id>/', views.toggle_task),
    path('delete/<int:id>/', views.delete_task),

    path('api/tasks/', views.task_api),
    path('api/admin/tasks/', views.admin_task_api),
]
