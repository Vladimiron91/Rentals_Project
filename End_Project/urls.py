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
        <li><a href="/api/v1/login/">Вход</a> (POST с username и password)</li>
        <li><a href="/api/v1/logout/">Выход</a> (требуется аутентификация)</li>
        <li><a href="/api/v1/current-user/">Текущий пользователь</a></li>
        <li><a href="/api/v1/listings/">Объявления</a></li>
        <li><a href="/api/v1/bookings/">Бронирования</a></li>
        <li><a href="/api/v1/listings/search/?q=berlin">Поиск объявлений</a></li>
        <li><a href="/admin/">Админка</a></li>
    </ul>
    
    
    
    
    

    <h3>
    Это поле только для меня кожаного, чтобы знать как правильно работать с Логином и Токенами
    Пример входа через cURL:</h3>
    
    
    <pre>
    curl -X POST http://localhost:8000/api/v1/login/ \\
      -H "Content-Type: application/json" \\
      -d '{"username": "testuser", "password": "test123"}'
    </pre>

    <h3>Пример использования токена:</h3>
    <pre>
    curl -X GET http://localhost:8000/api/v1/current-user/ \\
      -H "Authorization: Token YOUR_TOKEN_HERE"
    </pre>
    """
    return HttpResponse(html)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('api/v1/', include('rentals.urls'))
]