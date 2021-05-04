from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard/create_trip', views.create_trip),
    path('dashboard/new_trip', views.new_trip),
    path('dashboard/add_trip/<int:id>', views.add_trip),
    path('dashboard/delete/<int:id>', views.delete),
    path('dashboard/edit/<int:id>', views.edit),
    path('dashboard/update_trip/<int:id>', views.update_trip),
    path('dashboard/show_trip/<int:id>', views.show_trip),
    path('dashboard/join/<int:id>', views.join),
    path('dashboard/cancel/<int:id>', views.cancel),

]