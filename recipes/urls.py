# recipes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_index, name='recipe_index'),
    path('<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
]