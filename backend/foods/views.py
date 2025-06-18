from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import (
    FoodCategory, Nutrient, Food, FoodNutrient, BrandedFood,
    FoundationFood, SrLegacyFood, SurveyFnddsFood, FoodPortion,
    MeasureUnit, NutrientLookup
)
from .serializers import (
    FoodCategorySerializer, NutrientSerializer, FoodSerializer, FoodSearchSerializer,
    BrandedFoodSerializer, FoodNutrientSerializer, FoodPortionSerializer
)


class FoodCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for USDA Food Categories"""
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer


class NutrientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for USDA Nutrients"""
    queryset = Nutrient.objects.all().order_by('rank', 'name')
    serializer_class = NutrientSerializer


class FoodViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for USDA Foods"""
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    
    def get_queryset(self):
        queryset = Food.objects.all()
        
        # Filter by data type
        data_type = self.request.query_params.get('data_type')
        if data_type:
            queryset = queryset.filter(data_type=data_type)
        
        # Filter by food category
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(food_category_id=category_id)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def nutrients(self, request, pk=None):
        """Get all nutrients for a specific food"""
        food = self.get_object()
        nutrients = FoodNutrient.objects.filter(fdc_id=food.fdc_id).select_related()
        
        # Group nutrients by type for better organization
        nutrient_data = {}
        for fn in nutrients:
            try:
                nutrient = Nutrient.objects.get(id=fn.nutrient_id)
                nutrient_data[nutrient.name] = {
                    'amount': fn.amount,
                    'unit': nutrient.unit_name,
                    'nutrient_id': nutrient.id,
                    'percent_daily_value': fn.percent_daily_value
                }
            except Nutrient.DoesNotExist:
                continue
        
        return Response(nutrient_data)
    
    @action(detail=True, methods=['get'])
    def macros(self, request, pk=None):
        """Get macronutrients for a specific food"""
        food = self.get_object()
        macros = NutrientLookup.get_macros(food.fdc_id)
        return Response(macros)
    
    @action(detail=True, methods=['get'])
    def portions(self, request, pk=None):
        """Get portion information for a specific food"""
        food = self.get_object()
        portions = FoodPortion.objects.filter(fdc_id=food.fdc_id)
        serializer = FoodPortionSerializer(portions, many=True)
        return Response(serializer.data)


class FoodSearchView(APIView):
    """Advanced food search with full-text search and filtering"""
    
    def get(self, request):
        query = request.GET.get('q', '').strip()
        data_type = request.GET.get('data_type', '')
        category_id = request.GET.get('category_id', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        
        if not query:
            return Response({
                'results': [],
                'total_count': 0,
                'page': page,
                'page_size': page_size,
                'total_pages': 0
            })
        
        # Start with base queryset
        foods = Food.objects.all()
        
        # Apply filters
        if data_type:
            foods = foods.filter(data_type=data_type)
        
        if category_id:
            foods = foods.filter(food_category_id=category_id)
        
        # Full-text search
        if len(query) > 2:
            try:
                search_query = SearchQuery(query)
                foods = foods.filter(search_vector=search_query)
                foods = foods.annotate(
                    rank=SearchRank('search_vector', search_query)
                ).order_by('-rank')
            except:
                # Fallback to simple text search if search_vector not available
                foods = foods.filter(
                    Q(description__icontains=query)
                ).order_by('description')
        else:
            # Fallback to simple text search for short queries
            foods = foods.filter(
                Q(description__icontains=query)
            ).order_by('description')
        
        # Pagination
        paginator = Paginator(foods, page_size)
        page_obj = paginator.get_page(page)
        
        # Serialize results
        serializer = FoodSearchSerializer(page_obj.object_list, many=True)
        
        return Response({
            'results': serializer.data,
            'total_count': paginator.count,
            'page': page,
            'page_size': page_size,
            'total_pages': paginator.num_pages
        })


class FoodStatsView(APIView):
    """Get database statistics - Clean version without legacy models"""
    
    def get(self, request):
        try:
            stats = {
                'total_foods': Food.objects.count(),
                'branded_foods': BrandedFood.objects.count(),
                'foundation_foods': FoundationFood.objects.count(),
                'sr_legacy_foods': SrLegacyFood.objects.count(),
                'survey_fndds_foods': SurveyFnddsFood.objects.count(),
                'total_nutrients': Nutrient.objects.count(),
                'total_food_nutrients': FoodNutrient.objects.count(),
                'total_categories': FoodCategory.objects.count(),
                'status': 'ok'
            }
            
            # Top food categories (safe version)
            try:
                top_categories = Food.objects.values('food_category_id').annotate(
                    count=Count('fdc_id')
                ).order_by('-count')[:10]
                
                category_stats = []
                for cat in top_categories:
                    if cat['food_category_id']:
                        try:
                            category = FoodCategory.objects.get(id=cat['food_category_id'])
                            category_stats.append({
                                'id': category.id,
                                'name': category.description,
                                'count': cat['count']
                            })
                        except FoodCategory.DoesNotExist:
                            pass
                
                stats['top_categories'] = category_stats
            except:
                stats['top_categories'] = []
            
            return Response(stats)
            
        except Exception as e:
            # Return basic stats if there's an error
            return Response({
                'total_foods': 0,
                'branded_foods': 0,
                'foundation_foods': 0,
                'sr_legacy_foods': 0,
                'survey_fndds_foods': 0,
                'total_nutrients': 0,
                'total_food_nutrients': 0,
                'total_categories': 0,
                'top_categories': [],
                'status': 'error',
                'error': str(e)
            })


class FoodAutocompleteView(APIView):
    """Autocomplete suggestions for food search"""
    
    def get(self, request):
        query = request.GET.get('q', '').strip()
        limit = int(request.GET.get('limit', 10))
        
        if len(query) < 2:
            return Response([])
        
        # Get suggestions from food descriptions
        suggestions = Food.objects.filter(
            description__icontains=query
        ).values_list('description', flat=True).distinct()[:limit]
        
        return Response(list(suggestions))


class BarcodeSearchView(APIView):
    """Search foods by barcode (UPC/GTIN)"""
    
    def get(self, request):
        barcode = request.GET.get('barcode', '').strip()
        
        if not barcode:
            return Response({
                'error': 'Barcode parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Search in branded foods
        try:
            branded_food = BrandedFood.objects.get(gtin_upc=barcode)
            food = Food.objects.get(fdc_id=branded_food.fdc_id)
            
            # Get nutrition info
            macros = NutrientLookup.get_macros(food.fdc_id)
            
            result = {
                'fdc_id': food.fdc_id,
                'description': food.description,
                'brand_owner': branded_food.brand_owner,
                'brand_name': branded_food.brand_name,
                'ingredients': branded_food.ingredients,
                'serving_size': branded_food.serving_size,
                'serving_size_unit': branded_food.serving_size_unit,
                'gtin_upc': branded_food.gtin_upc,
                'nutrition': macros
            }
            
            return Response(result)
            
        except (BrandedFood.DoesNotExist, Food.DoesNotExist):
            return Response({
                'error': 'Food not found for this barcode'
            }, status=status.HTTP_404_NOT_FOUND)

