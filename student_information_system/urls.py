from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from student_information_system import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('student_information_app.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
