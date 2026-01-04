"""
URL configuration for End_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


"""
URL configuration for End_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
"""
URL configuration for End_Project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    html = """
    <h1>Rentals API</h1>
    <p>Доступные эндпоинты:</p>
    <ul>
        <li><a href="/api/v1/register/">Регистрация</a></li>
        <li><a href="/api/v1/listings/">Объявления</a></li>
        <li><a href="/api/v1/bookings/">Бронирования</a></li>
        <li><a href="/admin/">Админка</a></li>
    </ul>
    """
    return HttpResponse(html)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('api/v1/', include('rentals.urls'))
]