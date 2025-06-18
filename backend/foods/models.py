from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex


class FoodCategory(models.Model):
    """USDA Food Categories"""
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'food_category'
        verbose_name_plural = 'Food Categories'
    
    def __str__(self):
        return f"{self.code} - {self.description}"


class Nutrient(models.Model):
    """USDA Nutrients"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    unit_name = models.CharField(max_length=20)
    nutrient_nbr = models.CharField(max_length=10, null=True, blank=True)
    rank = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'nutrient'
        ordering = ['rank', 'name']
        indexes = [
            models.Index(fields=['rank', 'name']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.unit_name})"


class MeasureUnit(models.Model):
    """Measurement Units"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'measure_unit'
    
    def __str__(self):
        return self.name


class Food(models.Model):
    """Main USDA Food Data"""
    fdc_id = models.IntegerField(primary_key=True)
    data_type = models.CharField(max_length=50)
    description = models.TextField()
    food_category_id = models.IntegerField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    search_vector = SearchVectorField(null=True, blank=True)
    
    class Meta:
        db_table = 'food'
        indexes = [
            models.Index(fields=['data_type']),
            models.Index(fields=['food_category_id']),
            GinIndex(fields=['search_vector']),
        ]
    
    @property
    def food_category(self):
        """Get food category description"""
        if self.food_category_id:
            try:
                category = FoodCategory.objects.get(id=self.food_category_id)
                return category.description
            except FoodCategory.DoesNotExist:
                pass
        return None
    
    def __str__(self):
        return f"{self.fdc_id} - {self.description[:50]}"


class FoodNutrient(models.Model):
    """Food Nutrient Data"""
    id = models.BigIntegerField(primary_key=True)
    fdc_id = models.IntegerField()
    nutrient_id = models.IntegerField()
    amount = models.FloatField(null=True, blank=True)
    data_points = models.IntegerField(null=True, blank=True)
    derivation_id = models.IntegerField(null=True, blank=True)
    min = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)
    median = models.FloatField(null=True, blank=True)
    loq = models.CharField(max_length=10, null=True, blank=True)
    footnote = models.TextField(null=True, blank=True)
    min_year_acquired = models.IntegerField(null=True, blank=True)
    percent_daily_value = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'food_nutrient'
        indexes = [
            models.Index(fields=['fdc_id']),
            models.Index(fields=['nutrient_id']),
            models.Index(fields=['fdc_id', 'nutrient_id']),
        ]
    
    @property
    def nutrient(self):
        """Get nutrient object"""
        try:
            return Nutrient.objects.get(id=self.nutrient_id)
        except Nutrient.DoesNotExist:
            return None
    
    def __str__(self):
        return f"Food {self.fdc_id} - Nutrient {self.nutrient_id}: {self.amount}"


class BrandedFood(models.Model):
    """Branded Food Data - Updated with larger field sizes"""
    fdc_id = models.IntegerField(primary_key=True)
    brand_owner = models.CharField(max_length=500, null=True, blank=True)
    brand_name = models.CharField(max_length=500, null=True, blank=True)
    subbrand_name = models.CharField(max_length=500, null=True, blank=True)
    gtin_upc = models.CharField(max_length=50, null=True, blank=True)
    ingredients = models.TextField(null=True, blank=True)
    not_a_significant_source_of = models.TextField(null=True, blank=True)
    serving_size = models.FloatField(null=True, blank=True)
    serving_size_unit = models.CharField(max_length=50, null=True, blank=True)
    household_serving_fulltext = models.CharField(max_length=500, null=True, blank=True)
    branded_food_category = models.CharField(max_length=500, null=True, blank=True)
    data_source = models.CharField(max_length=100, null=True, blank=True)
    package_weight = models.CharField(max_length=100, null=True, blank=True)
    modified_date = models.DateField(null=True, blank=True)
    available_date = models.DateField(null=True, blank=True)
    market_country = models.CharField(max_length=100, null=True, blank=True)
    discontinued_date = models.DateField(null=True, blank=True)
    preparation_state_code = models.CharField(max_length=100, null=True, blank=True)
    trade_channel = models.CharField(max_length=200, null=True, blank=True)
    short_description = models.CharField(max_length=500, null=True, blank=True)
    
    class Meta:
        db_table = 'branded_food'
        indexes = [
            models.Index(fields=['gtin_upc']),
            models.Index(fields=['brand_owner']),
            models.Index(fields=['branded_food_category']),
        ]
    
    def __str__(self):
        return f"{self.brand_name} - {self.fdc_id}"


class FoundationFood(models.Model):
    """Foundation Food Data"""
    fdc_id = models.IntegerField(primary_key=True)
    ndb_number = models.IntegerField(null=True, blank=True)
    footnote = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'foundation_food'
    
    def __str__(self):
        return f"Foundation Food {self.fdc_id}"


class SrLegacyFood(models.Model):
    """SR Legacy Food Data"""
    fdc_id = models.IntegerField(primary_key=True)
    ndb_number = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'sr_legacy_food'
    
    def __str__(self):
        return f"SR Legacy Food {self.fdc_id}"


class SurveyFnddsFood(models.Model):
    """Survey FNDDS Food Data"""
    fdc_id = models.IntegerField(primary_key=True)
    food_code = models.IntegerField(null=True, blank=True)
    wweia_category_code = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'survey_fndds_food'
    
    def __str__(self):
        return f"Survey FNDDS Food {self.fdc_id}"


class FoodPortion(models.Model):
    """Food Portion Data"""
    id = models.IntegerField(primary_key=True)
    fdc_id = models.IntegerField()
    seq_num = models.IntegerField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    measure_unit_id = models.IntegerField(null=True, blank=True)
    portion_description = models.CharField(max_length=200, null=True, blank=True)
    modifier = models.CharField(max_length=200, null=True, blank=True)
    gram_weight = models.FloatField(null=True, blank=True)
    data_points = models.IntegerField(null=True, blank=True)
    footnote = models.TextField(null=True, blank=True)
    min_year_acquired = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'food_portion'
        indexes = [
            models.Index(fields=['fdc_id']),
        ]
    
    @property
    def measure_unit(self):
        """Get measure unit object"""
        if self.measure_unit_id:
            try:
                return MeasureUnit.objects.get(id=self.measure_unit_id)
            except MeasureUnit.DoesNotExist:
                pass
        return None
    
    def __str__(self):
        return f"Portion {self.id} for Food {self.fdc_id}"


class NutrientLookup:
    """Helper class for common nutrient lookups"""
    
    # Common nutrient IDs from USDA database
    ENERGY_KCAL = 1008  # Energy (kcal)
    PROTEIN = 1003      # Protein
    TOTAL_FAT = 1004    # Total lipid (fat)
    CARBS = 1005        # Carbohydrate, by difference
    FIBER = 1079        # Fiber, total dietary
    SUGARS = 2000       # Sugars, total including NLEA
    SODIUM = 1093       # Sodium, Na
    CALCIUM = 1087      # Calcium, Ca
    IRON = 1089         # Iron, Fe
    VITAMIN_C = 1162    # Vitamin C, total ascorbic acid
    
    @classmethod
    def get_nutrient_value(cls, fdc_id, nutrient_id):
        """Get nutrient value for a specific food"""
        try:
            food_nutrient = FoodNutrient.objects.get(
                fdc_id=fdc_id, 
                nutrient_id=nutrient_id
            )
            return food_nutrient.amount
        except FoodNutrient.DoesNotExist:
            return None
    
    @classmethod
    def get_macros(cls, fdc_id):
        """Get macronutrients for a food"""
        return {
            'calories': cls.get_nutrient_value(fdc_id, cls.ENERGY_KCAL),
            'protein': cls.get_nutrient_value(fdc_id, cls.PROTEIN),
            'fat': cls.get_nutrient_value(fdc_id, cls.TOTAL_FAT),
            'carbs': cls.get_nutrient_value(fdc_id, cls.CARBS),
            'fiber': cls.get_nutrient_value(fdc_id, cls.FIBER),
            'sugars': cls.get_nutrient_value(fdc_id, cls.SUGARS),
        }
    
    @classmethod
    def get_vitamins_minerals(cls, fdc_id):
        """Get key vitamins and minerals for a food"""
        return {
            'sodium': cls.get_nutrient_value(fdc_id, cls.SODIUM),
            'calcium': cls.get_nutrient_value(fdc_id, cls.CALCIUM),
            'iron': cls.get_nutrient_value(fdc_id, cls.IRON),
            'vitamin_c': cls.get_nutrient_value(fdc_id, cls.VITAMIN_C),
        }


class CNFoodCategory(models.Model):
    """Child Nutrition Food Categories"""
    code = models.IntegerField(primary_key=True, help_text="Food category code")
    description = models.CharField(max_length=200, help_text="Category description")
    date_added = models.DateField(null=True, blank=True)
    last_modified = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'cn_food_category'
        verbose_name = 'CN Food Category'
        verbose_name_plural = 'CN Food Categories'
    
    def __str__(self):
        return f"{self.code}: {self.description}"


class CNNutrient(models.Model):
    """Child Nutrition Nutrient Definitions"""
    code = models.IntegerField(primary_key=True, help_text="Nutrient code")
    description = models.CharField(max_length=200, help_text="Nutrient description")
    description_abbrev = models.CharField(max_length=50, help_text="Abbreviated description")
    unit = models.CharField(max_length=20, help_text="Nutrient unit")
    date_added = models.DateField(null=True, blank=True)
    last_modified = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'cn_nutrient'
        verbose_name = 'CN Nutrient'
        verbose_name_plural = 'CN Nutrients'
    
    def __str__(self):
        return f"{self.code}: {self.description} ({self.unit})"


class CNGPCName(models.Model):
    """Child Nutrition GPC (Global Product Classification) Names"""
    gpc_code = models.CharField(max_length=20, primary_key=True)
    gpc_description = models.CharField(max_length=500)
    date_added = models.DateField(null=True, blank=True)
    last_modified = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'cn_gpc_name'
        verbose_name = 'CN GPC Name'
        verbose_name_plural = 'CN GPC Names'
    
    def __str__(self):
        return f"{self.gpc_code}: {self.gpc_description}"


class CNFood(models.Model):
    """Child Nutrition Food Descriptions"""
    cn_code = models.IntegerField(primary_key=True, help_text="Child Nutrition code")
    # food_category = models.ForeignKey(CNFoodCategory, on_delete=models.CASCADE, help_text="Food category")
    # food_category = models.ForeignKey(CNFoodCategory, on_delete=models.CASCADE, null=True, blank=True)
    food_category = models.ForeignKey(CNFoodCategory, on_delete=models.CASCADE, null=True, blank=True, help_text="Food category")
    descriptor = models.TextField(help_text="Full food description")
    abbreviated_descriptor = models.CharField(max_length=200, help_text="Abbreviated description")
    gtin = models.CharField(max_length=20, null=True, blank=True, help_text="Global Trade Item Number")
    product_code = models.CharField(max_length=50, null=True, blank=True)
    brand_owner_name = models.CharField(max_length=200, null=True, blank=True)
    brand_name = models.CharField(max_length=200, null=True, blank=True)
    fns_material_number = models.CharField(max_length=50, null=True, blank=True)
    source_code = models.IntegerField(null=True, blank=True)
    date_added = models.DateField(null=True, blank=True)
    last_modified = models.DateField(null=True, blank=True)
    discontinued_date = models.DateField(null=True, blank=True)
    form_of_food = models.CharField(max_length=100, null=True, blank=True)
    fdc_id = models.IntegerField(null=True, blank=True, help_text="FoodData Central ID")
    gpc_product_code = models.ForeignKey(CNGPCName, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Search functionality
    search_vector = SearchVectorField(null=True, blank=True)
    
    class Meta:
        db_table = 'cn_food'
        verbose_name = 'CN Food'
        verbose_name_plural = 'CN Foods'
        indexes = [
            GinIndex(fields=['search_vector']),
            models.Index(fields=['food_category']),
            models.Index(fields=['gtin']),
            models.Index(fields=['fdc_id']),
        ]
    
    def __str__(self):
        return f"{self.cn_code}: {self.descriptor}"
    
    @property
    def food_category_name(self):
        return self.food_category.description if self.food_category else None


class CNNutrientValue(models.Model):
    """Child Nutrition Nutrient Values"""
    cn_food = models.ForeignKey(CNFood, on_delete=models.CASCADE, related_name='nutrient_values')
    nutrient = models.ForeignKey(CNNutrient, on_delete=models.CASCADE)
    nutrient_value = models.FloatField(help_text="Nutrient value")
    per_unit = models.CharField(max_length=20, default='100g', help_text="Per unit (e.g., 100g)")
    value_type_code = models.IntegerField(null=True, blank=True)
    source_code = models.IntegerField(null=True, blank=True)
    date_added = models.DateField(null=True, blank=True)
    last_modified = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'cn_nutrient_value'
        verbose_name = 'CN Nutrient Value'
        verbose_name_plural = 'CN Nutrient Values'
        unique_together = ['cn_food', 'nutrient']
        indexes = [
            models.Index(fields=['cn_food', 'nutrient']),
            models.Index(fields=['nutrient']),
        ]
    
    def __str__(self):
        return f"{self.cn_food.cn_code} - {self.nutrient.description}: {self.nutrient_value} {self.nutrient.unit}"


class CNWeight(models.Model):
    """Child Nutrition Weights/Portions"""
    cn_food = models.ForeignKey(CNFood, on_delete=models.CASCADE, related_name='weights')
    sequence_num = models.IntegerField(help_text="Sequence number")
    amount = models.FloatField(help_text="Amount")
    measure_description = models.CharField(max_length=200, help_text="Measure description")
    unit_amount = models.FloatField(help_text="Unit amount")
    type_of_unit = models.CharField(max_length=20, help_text="Type of unit (e.g., g, ml)")
    source_code = models.IntegerField(null=True, blank=True)
    date_added = models.DateField(null=True, blank=True)
    last_modified = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'cn_weight'
        verbose_name = 'CN Weight'
        verbose_name_plural = 'CN Weights'
        unique_together = ['cn_food', 'sequence_num']
        indexes = [
            models.Index(fields=['cn_food']),
        ]
    
    def __str__(self):
        return f"{self.cn_food.cn_code} - {self.amount} {self.measure_description}"


class CNNutrientLookup:
    """Helper class for common Child Nutrition nutrient lookups"""
    
    # Common nutrient codes in Child Nutrition database
    ENERGY_KCAL = 208  # Energy (kcal)
    PROTEIN = 203      # Protein
    TOTAL_FAT = 204    # Total Fat
    CARBS = 205        # Carbohydrate
    FIBER = 291        # Fiber, total dietary
    SUGARS = 269       # Sugars, total
    CALCIUM = 301      # Calcium
    IRON = 303         # Iron
    SODIUM = 307       # Sodium
    VITAMIN_C = 401    # Vitamin C
    VITAMIN_A = 320    # Vitamin A, RAE
    
    @classmethod
    def get_nutrient_value(cls, cn_code, nutrient_code):
        """Get a specific nutrient value for a CN food"""
        try:
            nutrient_value = CNNutrientValue.objects.get(
                cn_food__cn_code=cn_code,
                nutrient__code=nutrient_code
            )
            return nutrient_value.nutrient_value
        except CNNutrientValue.DoesNotExist:
            return None
    
    @classmethod
    def get_macros(cls, cn_code):
        """Get macronutrients for a CN food"""
        return {
            'calories': cls.get_nutrient_value(cn_code, cls.ENERGY_KCAL),
            'protein': cls.get_nutrient_value(cn_code, cls.PROTEIN),
            'fat': cls.get_nutrient_value(cn_code, cls.TOTAL_FAT),
            'carbs': cls.get_nutrient_value(cn_code, cls.CARBS),
            'fiber': cls.get_nutrient_value(cn_code, cls.FIBER),
            'sugars': cls.get_nutrient_value(cn_code, cls.SUGARS),
        }
    
    @classmethod
    def get_vitamins_minerals(cls, cn_code):
        """Get key vitamins and minerals for a CN food"""
        return {
            'calcium': cls.get_nutrient_value(cn_code, cls.CALCIUM),
            'iron': cls.get_nutrient_value(cn_code, cls.IRON),
            'sodium': cls.get_nutrient_value(cn_code, cls.SODIUM),
            'vitamin_c': cls.get_nutrient_value(cn_code, cls.VITAMIN_C),
            'vitamin_a': cls.get_nutrient_value(cn_code, cls.VITAMIN_A),
        }