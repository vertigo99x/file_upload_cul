from django.urls import path


from . import views


urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('students', views.students, name='students'),
    path('history', views.history, name='history'),
    path('notifications', views.notifications, name='notifications'),
    path('file/upload', views.upload_file, name='upload_file'),
    path('folder/create', views.createFolder, name='create_folder'),
    path('folder/<str:folder_id>', views.folderSort, name='folder_sort'),
    path('file/approve/<str:pk>', views.approve, name='approve'),
    path('file/reject/<str:pk>', views.reject, name='reject'),
    
]
