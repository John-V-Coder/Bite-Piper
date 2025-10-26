"""
URL configuration for funding app
"""

from django.urls import path
from . import views

app_name = 'funding'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('dashboard/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('agent/', views.agent_dashboard, name='agent_dashboard'),
    
    # HTMX endpoints
    path('calculate/', views.calculate_allocation, name='calculate'),
    path('recalculate-custom/', views.recalculate_custom, name='recalculate_custom'),
    path('priority/<str:region_name>/', views.calculate_priority, name='priority'),
    
    # Agent integration endpoints
    path('agent/analyze/', views.agent_analyze_allocation, name='agent_analyze'),
    path('agent/analyze/<str:region_name>/', views.agent_analyze_single, name='agent_analyze_single'),
    
    # API endpoints
    path('api/health/', views.api_health, name='api_health'),
    path('api/regions/', views.get_regions, name='api_regions'),
    path('api/agent/health/', views.agent_health, name='agent_health'),
]
