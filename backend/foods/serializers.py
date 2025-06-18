from rest_framework import serializers
from .models import (
    FoodCategory, Nutrient, Food, FoodNutrient, BrandedFood,
    FoundationFood, SrLegacyFood, SurveyFnddsFood, FoodPortion,
    MeasureUnit, NutrientLookup
)


class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ['id', 'code', 'description']


class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrient
        fields = ['id', 'name', 'unit_name', 'nutrient_nbr', 'rank']


class FoodSerializer(serializers.ModelSerializer):
    food_category = serializers.CharField(read_only=True)
    
    class Meta:
        model = Food
        fields = ['fdc_id', 'data_type', 'description', 'food_category_id', 'food_category', 'publication_date']


class FoodSearchSerializer(serializers.ModelSerializer):
    """Serializer for food search results with nutrition preview"""
    food_category = serializers.CharField(read_only=True)
    calories = serializers.SerializerMethodField()
    protein = serializers.SerializerMethodField()
    fat = serializers.SerializerMethodField()
    carbs = serializers.SerializerMethodField()
    
    class Meta:
        model = Food
        fields = ['fdc_id', 'data_type', 'description', 'food_category', 'calories', 'protein', 'fat', 'carbs']
    
    def get_calories(self, obj):
        return NutrientLookup.get_nutrient_value(obj.fdc_id, NutrientLookup.ENERGY_KCAL)
    
    def get_protein(self, obj):
        return NutrientLookup.get_nutrient_value(obj.fdc_id, NutrientLookup.PROTEIN)
    
    def get_fat(self, obj):
        return NutrientLookup.get_nutrient_value(obj.fdc_id, NutrientLookup.TOTAL_FAT)
    
    def get_carbs(self, obj):
        return NutrientLookup.get_nutrient_value(obj.fdc_id, NutrientLookup.CARBS)


class FoodNutrientSerializer(serializers.ModelSerializer):
    nutrient_name = serializers.CharField(source='nutrient.name', read_only=True)
    nutrient_unit = serializers.CharField(source='nutrient.unit_name', read_only=True)
    
    class Meta:
        model = FoodNutrient
        fields = ['id', 'fdc_id', 'nutrient_id', 'nutrient_name', 'nutrient_unit', 'amount', 'percent_daily_value']


class BrandedFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandedFood
        fields = [
            'fdc_id', 'brand_owner', 'brand_name', 'subbrand_name', 'gtin_upc',
            'ingredients', 'serving_size', 'serving_size_unit', 'household_serving_fulltext',
            'branded_food_category', 'data_source', 'package_weight'
        ]


class FoodPortionSerializer(serializers.ModelSerializer):
    measure_unit_name = serializers.CharField(source='measure_unit.name', read_only=True)
    
    class Meta:
        model = FoodPortion
        fields = [
            'id', 'fdc_id', 'seq_num', 'amount', 'measure_unit_id', 'measure_unit_name',
            'portion_description', 'modifier', 'gram_weight'
        ]

# from rest_framework import serializers
from .models import (
    CNFoodCategory, CNNutrient, CNGPCName, CNFood, 
    CNNutrientValue, CNWeight, CNNutrientLookup
)


class CNFoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CNFoodCategory
        fields = ['code', 'description', 'date_added', 'last_modified']


class CNNutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = CNNutrient
        fields = ['code', 'description', 'description_abbrev', 'unit', 'date_added', 'last_modified']


class CNNutrientValueSerializer(serializers.ModelSerializer):
    nutrient_name = serializers.CharField(source='nutrient.description', read_only=True)
    nutrient_unit = serializers.CharField(source='nutrient.unit', read_only=True)
    nutrient_abbrev = serializers.CharField(source='nutrient.description_abbrev', read_only=True)
    
    class Meta:
        model = CNNutrientValue
        fields = [
            'nutrient_value', 'per_unit', 'nutrient_name', 
            'nutrient_unit', 'nutrient_abbrev'
        ]


class CNWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = CNWeight
        fields = [
            'sequence_num', 'amount', 'measure_description', 
            'unit_amount', 'type_of_unit'
        ]


class CNFoodListSerializer(serializers.ModelSerializer):
    """Serializer for CN food list views (minimal data)"""
    food_category_name = serializers.CharField(source='food_category.description', read_only=True)
    
    # Basic nutrition info
    calories = serializers.SerializerMethodField()
    protein = serializers.SerializerMethodField()
    fat = serializers.SerializerMethodField()
    carbs = serializers.SerializerMethodField()
    
    class Meta:
        model = CNFood
        fields = [
            'cn_code', 'descriptor', 'abbreviated_descriptor',
            'food_category_name', 'brand_name', 'brand_owner_name',
            'calories', 'protein', 'fat', 'carbs'
        ]
    
    def get_calories(self, obj):
        return CNNutrientLookup.get_nutrient_value(obj.cn_code, CNNutrientLookup.ENERGY_KCAL)
    
    def get_protein(self, obj):
        return CNNutrientLookup.get_nutrient_value(obj.cn_code, CNNutrientLookup.PROTEIN)
    
    def get_fat(self, obj):
        return CNNutrientLookup.get_nutrient_value(obj.cn_code, CNNutrientLookup.TOTAL_FAT)
    
    def get_carbs(self, obj):
        return CNNutrientLookup.get_nutrient_value(obj.cn_code, CNNutrientLookup.CARBS)


class CNFoodDetailSerializer(serializers.ModelSerializer):
    """Serializer for CN food detail views (complete data)"""
    food_category_name = serializers.CharField(source='food_category.description', read_only=True)
    nutrient_values = CNNutrientValueSerializer(many=True, read_only=True)
    weights = CNWeightSerializer(many=True, read_only=True)
    
    # Macronutrients
    macros = serializers.SerializerMethodField()
    vitamins_minerals = serializers.SerializerMethodField()
    
    class Meta:
        model = CNFood
        fields = [
            'cn_code', 'descriptor', 'abbreviated_descriptor',
            'food_category_name', 'gtin', 'product_code',
            'brand_owner_name', 'brand_name', 'fns_material_number',
            'form_of_food', 'fdc_id', 'date_added', 'last_modified',
            'nutrient_values', 'weights', 'macros', 'vitamins_minerals'
        ]
    
    def get_macros(self, obj):
        return CNNutrientLookup.get_macros(obj.cn_code)
    
    def get_vitamins_minerals(self, obj):
        return CNNutrientLookup.get_vitamins_minerals(obj.cn_code)

