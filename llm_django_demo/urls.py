from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from core.views import APIRootView, AllConversationsView, VegetarianConversationsView

def home(request):
    return HttpResponse("Hello! Django is working with PostgreSQL!")

def health(request):
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return HttpResponse("Database connection: OK")
    except Exception as e:
        return HttpResponse(f"Database connection failed: {e}")

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Basic pages
    path('', APIRootView.as_view(), name='api_root'),  # API root at the main URL
    path('home/', home, name='home'),
    path('health/', health, name='health'),
    
    # API endpoints
    path('api/', APIRootView.as_view(), name='api_root_alt'),  # Alternative API root
    path('api/conversations/', AllConversationsView.as_view(), name='all_conversations'),
    path('api/vegetarian_conversations/', VegetarianConversationsView.as_view(), name='vegetarian_conversations'),
]