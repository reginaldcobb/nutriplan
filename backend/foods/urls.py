from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.FoodCategoryViewSet)
router.register(r'nutrients', views.NutrientViewSet)
router.register(r'foods', views.FoodViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/', views.FoodSearchView.as_view(), name='food-search'),
    path('stats/', views.FoodStatsView.as_view(), name='food-stats'),
    path('autocomplete/', views.FoodAutocompleteView.as_view(), name='food-autocomplete'),
    path('barcode/', views.BarcodeSearchView.as_view(), name='barcode-search'),
]

