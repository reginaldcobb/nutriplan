import csv
import os
from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from django.db import transaction
from foods.models import (
    FoodCategory, Nutrient, Food, FoodNutrient, BrandedFood,
    FoundationFood, SrLegacyFood, SurveyFnddsFood, FoodPortion, MeasureUnit
)


class Command(BaseCommand):
    help = 'Import USDA FoodData Central CSV data'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-dir',
            type=str,
            default='/opt/nutriplan/FoodData_Central_csv_2025-04-24',
            help='Directory containing USDA CSV files'
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Limit number of foods to import (for testing)'
        )
        parser.add_argument(
            '--skip-nutrients',
            action='store_true',
            help='Skip importing food nutrient data (faster)'
        )
        parser.add_argument(
            '--skip-portions',
            action='store_true',
            help='Skip importing food portion data'
        )
    
    def handle(self, *args, **options):
        csv_dir = options['csv_dir']
        limit = options.get('limit')
        skip_nutrients = options.get('skip_nutrients', False)
        skip_portions = options.get('skip_portions', False)
        
        if not os.path.exists(csv_dir):
            self.stdout.write(
                self.style.ERROR(f'CSV directory not found: {csv_dir}')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS('Starting USDA FoodData Central import...')
        )
        
        # Import in order
        self.import_food_categories(csv_dir)
        self.import_nutrients(csv_dir)
        self.import_measure_units(csv_dir)
        self.import_foods(csv_dir, limit)
        
        if not skip_nutrients:
            self.import_food_nutrients(csv_dir, limit)
        
        if not skip_portions:
            self.import_food_portions(csv_dir, limit)
        
        self.import_branded_foods(csv_dir, limit)
        self.import_foundation_foods(csv_dir, limit)
        self.import_sr_legacy_foods(csv_dir, limit)
        self.import_survey_fndds_foods(csv_dir, limit)
        
        # Update search vectors
        if not skip_nutrients:
            self.update_search_vectors()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully imported USDA FoodData Central data!')
        )
    
    def import_food_categories(self, csv_dir):
        """Import food categories"""
        file_path = os.path.join(csv_dir, 'food_category.csv')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING('food_category.csv not found'))
            return
        
        self.stdout.write('Importing food categories...')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            categories = []
            
            for row in reader:
                categories.append(FoodCategory(
                    id=int(row['id']),
                    code=row['code'],
                    description=row['description']
                ))
                
                if len(categories) >= 1000:
                    FoodCategory.objects.bulk_create(categories, ignore_conflicts=True)
                    categories = []
            
            if categories:
                FoodCategory.objects.bulk_create(categories, ignore_conflicts=True)
        
        count = FoodCategory.objects.count()
        self.stdout.write(f'Imported {count} food categories')
    
    def import_nutrients(self, csv_dir):
        """Import nutrients"""
        file_path = os.path.join(csv_dir, 'nutrient.csv')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING('nutrient.csv not found'))
            return
        
        self.stdout.write('Importing nutrients...')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            nutrients = []
            
            for row in reader:
                nutrients.append(Nutrient(
                    id=int(row['id']),
                    name=row['name'],
                    unit_name=row['unit_name'],
                    nutrient_nbr=row.get('nutrient_nbr'),
                    rank=float(row['rank']) if row.get('rank') else None
                ))
                
                if len(nutrients) >= 1000:
                    Nutrient.objects.bulk_create(nutrients, ignore_conflicts=True)
                    nutrients = []
            
            if nutrients:
                Nutrient.objects.bulk_create(nutrients, ignore_conflicts=True)
        
        count = Nutrient.objects.count()
        self.stdout.write(f'Imported {count} nutrients')
    
    def import_measure_units(self, csv_dir):
        """Import measure units"""
        file_path = os.path.join(csv_dir, 'measure_unit.csv')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING('measure_unit.csv not found'))
            return
        
        self.stdout.write('Importing measure units...')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            units = []
            
            for row in reader:
                units.append(MeasureUnit(
                    id=int(row['id']),
                    name=row['name']
                ))
                
                if len(units) >= 1000:
                    MeasureUnit.objects.bulk_create(units, ignore_conflicts=True)
                    units = []
            
            if units:
                MeasureUnit.objects.bulk_create(units, ignore_conflicts=True)
        
        count = MeasureUnit.objects.count()
        self.stdout.write(f'Imported {count} measure units')
    
    def import_foods(self, csv_dir, limit=None):
        """Import main food data"""
        file_path = os.path.join(csv_dir, 'food.csv')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR('food.csv not found'))
            return
        
        self.stdout.write('Importing foods...')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            foods = []
            count = 0
            
            for row in reader:
                if limit and count >= limit:
                    break
                
                # Parse publication date
                pub_date = None
                if row.get('publication_date'):
                    try:
                        pub_date = row['publication_date']
                    except:
                        pass
                
                foods.append(Food(
                    fdc_id=int(row['fdc_id']),
                    data_type=row['data_type'],
                    description=row['description'],
                    food_category_id=int(row['food_category_id']) if row.get('food_category_id') else None,
                    publication_date=pub_date
                ))
                
                count += 1
                
                if len(foods) >= 1000:
                    Food.objects.bulk_create(foods, ignore_conflicts=True)
                    foods = []
                    self.stdout.write(f'Imported {count} foods...')
            
            if foods:
                Food.objects.bulk_create(foods, ignore_conflicts=True)
        
        total_count = Food.objects.count()
        self.stdout.write(f'Imported {total_count} foods total')
    
    def import_food_nutrients(self, csv_dir, limit=None):
        """Import food nutrient data"""
        file_path = os.path.join(csv_dir, 'food_nutrient.csv')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING('food_nutrient.csv not found'))
            return
        
        self.stdout.write('Importing food nutrients...')
        
        # Get list of imported food IDs if limit is set
        imported_food_ids = None
        if limit:
            imported_food_ids = set(Food.objects.values_list('fdc_id', flat=True))
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            nutrients = []
            count = 0
            
            for row in reader:
                fdc_id = int(row['fdc_id'])
                
                # Skip if food not imported (when using limit)
                if imported_food_ids and fdc_id not in imported_food_ids:
                    continue
                
                nutrients.append(FoodNutrient(
                    id=int(row['id']),
                    fdc_id=fdc_id,
                    nutrient_id=int(row['nutrient_id']),
                    amount=float(row['amount']) if row.get('amount') else None,
                    data_points=int(row['data_points']) if row.get('data_points') else None,
                    derivation_id=int(row['derivation_id']) if row.get('derivation_id') else None,
                    min=float(row['min']) if row.get('min') else None,
                    max=float(row['max']) if row.get('max') else None,
                    median=float(row['median']) if row.get('median') else None,
                    loq=row.get('loq'),
                    footnote=row.get('footnote'),
                    min_year_acquired=int(row['min_year_acquired']) if row.get('min_year_acquired') else None,
                    percent_daily_value=float(row['percent_daily_value']) if row.get('percent_daily_value') else None
                ))
                
                count += 1
                
                if len(nutrients) >= 5000:
                    FoodNutrient.objects.bulk_create(nutrients, ignore_conflicts=True)
                    nutrients = []
                    self.stdout.write(f'Imported {count} food nutrients...')
            
            if nutrients:
                FoodNutrient.objects.bulk_create(nutrients, ignore_conflicts=True)
        
        total_count = FoodNutrient.objects.count()
        self.stdout.write(f'Imported {total_count} food nutrients total')
    
    def import_food_portions(self, csv_dir, limit=None):
        """Import food portion data"""
        file_path = os.path.join(csv_dir, 'food_portion.csv')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING('food_portion.csv not found'))
            return
        
        self.stdout.write('Importing food portions...')
        
        # Get list of imported food IDs if limit is set
        imported_food_ids = None
        if limit:
            imported_food_ids = set(Food.objects.values_list('fdc_id', flat=True))
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            portions = []
            count = 0
            
            for row in reader:
                fdc_id = int(row['fdc_id'])
                
                # Skip if food not imported (when using limit)
                if imported_food_ids and fdc_id not in imported_food_ids:
                    continue
                
                portions.append(FoodPortion(
                    id=int(row['id']),
                    fdc_id=fdc_id,
                    seq_num=int(row['seq_num']) if row.get('seq_num') else None,
                    amount=float(row['amount']) if row.get('amount') else None,
                    measure_unit_id=int(row['measure_unit_id']) if row.get('measure_unit_id') else None,
                    portion_description=row.get('portion_description'),
                    modifier=row.get('modifier'),
                    gram_weight=float(row['gram_weight']) if row.get('gram_weight') else None,
                    data_points=int(row['data_points']) if row.get('data_points') else None,
                    footnote=row.get('footnote'),
                    min_year_acquired=int(row['min_year_acquired']) if row.get('min_year_acquired') else None
                ))
                
                count += 1
                
                if len(portions) >= 5000:
                    FoodPortion.objects.bulk_create(portions, ignore_conflicts=True)
                    portions = []
                    self.stdout.write(f'Imported {count} food portions...')
            
            if portions:
                FoodPortion.objects.bulk_create(portions, ignore_conflicts=True)
        
        total_count = FoodPortion.objects.count()
        self.stdout.write(f'Imported {total_count} food portions total')
    
    def truncate_field(self, value, max_length):
        """Truncate field value to max length"""
        if value and len(value) > max_length:
            return value[:max_length-3] + "..."
        return value
    
    def import_branded_foods(self, csv_dir, limit=None):
        """Import branded food data"""
        file_path = os.path.join(csv_dir, 'branded_food.csv')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING('branded_food.csv not found'))
            return
        
        self.stdout.write('Importing branded foods...')
        
        # Get list of imported food IDs if limit is set
        imported_food_ids = None
        if limit:
            imported_food_ids = set(Food.objects.values_list('fdc_id', flat=True))
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            branded_foods = []
            count = 0
            
            for row in reader:
                fdc_id = int(row['fdc_id'])
                
                # Skip if food not imported (when using limit)
                if imported_food_ids and fdc_id not in imported_food_ids:
                    continue
                
                # Parse dates
                modified_date = None
                available_date = None
                discontinued_date = None
                
                try:
                    if row.get('modified_date'):
                        modified_date = row['modified_date']
                    if row.get('available_date'):
                        available_date = row['available_date']
                    if row.get('discontinued_date'):
                        discontinued_date = row['discontinued_date']
                except:
                    pass
                
                branded_foods.append(BrandedFood(
                    fdc_id=fdc_id,
                    brand_owner=self.truncate_field(row.get('brand_owner'), 500),
                    brand_name=self.truncate_field(row.get('brand_name'), 500),
                    subbrand_name=self.truncate_field(row.get('subbrand_name'), 500),
                    gtin_upc=row.get('gtin_upc'),
                    ingredients=row.get('ingredients'),
                    not_a_significant_source_of=row.get('not_a_significant_source_of'),
                    serving_size=float(row['serving_size']) if row.get('serving_size') else None,
                    serving_size_unit=self.truncate_field(row.get('serving_size_unit'), 50),
                    household_serving_fulltext=self.truncate_field(row.get('household_serving_fulltext'), 500),
                    branded_food_category=self.truncate_field(row.get('branded_food_category'), 500),
                    data_source=self.truncate_field(row.get('data_source'), 100),
                    package_weight=self.truncate_field(row.get('package_weight'), 100),
                    modified_date=modified_date,
                    available_date=available_date,
                    market_country=self.truncate_field(row.get('market_country'), 100),
                    discontinued_date=discontinued_date,
                    preparation_state_code=self.truncate_field(row.get('preparation_state_code'), 100),
                    trade_channel=self.truncate_field(row.get('trade_channel'), 200),
                    short_description=self.truncate_field(row.get('short_description'), 500)
                ))
                
                count += 1
                
                if len(branded_foods) >= 1000:
                    BrandedFood.objects.bulk_create(branded_foods, ignore_conflicts=True)
                    branded_foods = []
                    self.stdout.write(f'Imported {count} branded foods...')
            
            if branded_foods:
                BrandedFood.objects.bulk_create(branded_foods, ignore_conflicts=True)
        
        total_count = BrandedFood.objects.count()
        self.stdout.write(f'Imported {total_count} branded foods total')
    
    def import_foundation_foods(self, csv_dir, limit=None):
        """Import foundation food data"""
        file_path = os.path.join(csv_dir, 'foundation_food.csv')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING('foundation_food.csv not found'))
            return
        
        self.stdout.write('Importing foundation foods...')
        
        # Get list of imported food IDs if limit is set
        imported_food_ids = None
        if limit:
            imported_food_ids = set(Food.objects.values_list('fdc_id', flat=True))
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            foundation_foods = []
            
            for row in reader:
                fdc_id = int(row['fdc_id'])
                
                # Skip if food not imported (when using limit)
                if imported_food_ids and fdc_id not in imported_food_ids:
                    continue
                
                foundation_foods.append(FoundationFood(
                    fdc_id=fdc_id,
                    ndb_number=int(row['ndb_number']) if row.get('ndb_number') else None,
                    footnote=row.get('footnote')
                ))
                
                if len(foundation_foods) >= 1000:
                    FoundationFood.objects.bulk_create(foundation_foods, ignore_conflicts=True)
                    foundation_foods = []
            
            if foundation_foods:
                FoundationFood.objects.bulk_create(foundation_foods, ignore_conflicts=True)
        
        count = FoundationFood.objects.count()
        self.stdout.write(f'Imported {count} foundation foods')
    
    def import_sr_legacy_foods(self, csv_dir, limit=None):
        """Import SR legacy food data"""
        file_path = os.path.join(csv_dir, 'sr_legacy_food.csv')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING('sr_legacy_food.csv not found'))
            return
        
        self.stdout.write('Importing SR legacy foods...')
        
        # Get list of imported food IDs if limit is set
        imported_food_ids = None
        if limit:
            imported_food_ids = set(Food.objects.values_list('fdc_id', flat=True))
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            sr_foods = []
            
            for row in reader:
                fdc_id = int(row['fdc_id'])
                
                # Skip if food not imported (when using limit)
                if imported_food_ids and fdc_id not in imported_food_ids:
                    continue
                
                sr_foods.append(SrLegacyFood(
                    fdc_id=fdc_id,
                    ndb_number=int(row['ndb_number']) if row.get('ndb_number') else None
                ))
                
                if len(sr_foods) >= 1000:
                    SrLegacyFood.objects.bulk_create(sr_foods, ignore_conflicts=True)
                    sr_foods = []
            
            if sr_foods:
                SrLegacyFood.objects.bulk_create(sr_foods, ignore_conflicts=True)
        
        count = SrLegacyFood.objects.count()
        self.stdout.write(f'Imported {count} SR legacy foods')
    
    def import_survey_fndds_foods(self, csv_dir, limit=None):
        """Import survey FNDDS food data"""
        file_path = os.path.join(csv_dir, 'survey_fndds_food.csv')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING('survey_fndds_food.csv not found'))
            return
        
        self.stdout.write('Importing survey FNDDS foods...')
        
        # Get list of imported food IDs if limit is set
        imported_food_ids = None
        if limit:
            imported_food_ids = set(Food.objects.values_list('fdc_id', flat=True))
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            survey_foods = []
            
            for row in reader:
                fdc_id = int(row['fdc_id'])
                
                # Skip if food not imported (when using limit)
                if imported_food_ids and fdc_id not in imported_food_ids:
                    continue
                
                # Parse dates
                start_date = None
                end_date = None
                try:
                    if row.get('start_date'):
                        start_date = row['start_date']
                    if row.get('end_date'):
                        end_date = row['end_date']
                except:
                    pass
                
                survey_foods.append(SurveyFnddsFood(
                    fdc_id=fdc_id,
                    food_code=int(row['food_code']) if row.get('food_code') else None,
                    wweia_category_code=int(row['wweia_category_code']) if row.get('wweia_category_code') else None,
                    start_date=start_date,
                    end_date=end_date
                ))
                
                if len(survey_foods) >= 1000:
                    SurveyFnddsFood.objects.bulk_create(survey_foods, ignore_conflicts=True)
                    survey_foods = []
            
            if survey_foods:
                SurveyFnddsFood.objects.bulk_create(survey_foods, ignore_conflicts=True)
        
        count = SurveyFnddsFood.objects.count()
        self.stdout.write(f'Imported {count} survey FNDDS foods')
    
    def update_search_vectors(self):
        """Update search vectors for full-text search"""
        self.stdout.write('Updating search vectors...')
        
        try:
            with transaction.atomic():
                Food.objects.update(
                    search_vector=SearchVector('description')
                )
            self.stdout.write('Search vectors updated successfully')
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not update search vectors: {e}')
            )

