import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from django.db import transaction
from foods.models import (
    CNFoodCategory, CNNutrient, CNGPCName, CNFood, 
    CNNutrientValue, CNWeight
)


class Command(BaseCommand):
    help = 'Import Child Nutrition database CSV data'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-dir',
            type=str,
            default='/opt/nutriplan',
            help='Directory containing Child Nutrition CSV files'
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Limit number of foods to import (for testing)'
        )
        parser.add_argument(
            '--skip-nutrients',
            action='store_true',
            help='Skip importing nutrient values (faster)'
        )
        parser.add_argument(
            '--skip-weights',
            action='store_true',
            help='Skip importing weight/portion data'
        )
    
    def handle(self, *args, **options):
        csv_dir = options['csv_dir']
        limit = options.get('limit')
        skip_nutrients = options.get('skip_nutrients', False)
        skip_weights = options.get('skip_weights', False)
        
        # Look for CN CSV files
        cn_files = [
            'CN.2025.05_CTGNME.csv',
            'CN.2025.05_NUTDES.csv', 
            'CN.2025.05_GPCNME.csv',
            'CN.2025.05_FDES.csv',
            'CN.2025.05_NUTVAL.csv',
            'CN.2025.05_WGHT.csv'
        ]
        
        # Check if files exist
        missing_files = []
        for file in cn_files:
            if not os.path.exists(os.path.join(csv_dir, file)):
                missing_files.append(file)
        
        if missing_files:
            self.stdout.write(
                self.style.ERROR(f'Missing CN CSV files: {", ".join(missing_files)}')
            )
            self.stdout.write(f'Looking in directory: {csv_dir}')
            return
        
        self.stdout.write(
            self.style.SUCCESS('Starting Child Nutrition database import...')
        )
        
        # Import in order
        self.import_food_categories(csv_dir)
        self.import_nutrients(csv_dir)
        self.import_gpc_names(csv_dir)
        self.import_foods(csv_dir, limit)
        
        if not skip_nutrients:
            self.import_nutrient_values(csv_dir, limit)
        
        if not skip_weights:
            self.import_weights(csv_dir, limit)
        
        # Update search vectors
        self.update_search_vectors()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully imported Child Nutrition database!')
        )
    
    def parse_date(self, date_str):
        """Parse date string in MM/DD/YYYY format"""
        if not date_str or date_str.strip() == '':
            return None
        try:
            return datetime.strptime(date_str.strip(), '%m/%d/%Y').date()
        except ValueError:
            try:
                return datetime.strptime(date_str.strip(), '%m/%d/%y').date()
            except ValueError:
                return None
    
    def import_food_categories(self, csv_dir):
        """Import CN food categories"""
        file_path = os.path.join(csv_dir, 'CN.2025.05_CTGNME.csv')
        self.stdout.write('Importing CN food categories...')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            categories = []
            
            for row in reader:
                categories.append(CNFoodCategory(
                    code=int(row['Food category code']),
                    description=row['Category description'],
                    date_added=self.parse_date(row.get('Date added')),
                    last_modified=self.parse_date(row.get('Last modified'))
                ))
                
                if len(categories) >= 100:
                    CNFoodCategory.objects.bulk_create(categories, ignore_conflicts=True)
                    categories = []
            
            if categories:
                CNFoodCategory.objects.bulk_create(categories, ignore_conflicts=True)
        
        count = CNFoodCategory.objects.count()
        self.stdout.write(f'Imported {count} CN food categories')
    
    def import_nutrients(self, csv_dir):
        """Import CN nutrients"""
        file_path = os.path.join(csv_dir, 'CN.2025.05_NUTDES.csv')
        self.stdout.write('Importing CN nutrients...')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            nutrients = []
            
            for row in reader:
                nutrients.append(CNNutrient(
                    code=int(row['Nutrient code']),
                    description=row['Nutrient description'],
                    description_abbrev=row['Nutrient description abbrev'],
                    unit=row['Nutrient unit'],
                    date_added=self.parse_date(row.get('Date added')),
                    last_modified=self.parse_date(row.get('Last modified'))
                ))
                
                if len(nutrients) >= 100:
                    CNNutrient.objects.bulk_create(nutrients, ignore_conflicts=True)
                    nutrients = []
            
            if nutrients:
                CNNutrient.objects.bulk_create(nutrients, ignore_conflicts=True)
        
        count = CNNutrient.objects.count()
        self.stdout.write(f'Imported {count} CN nutrients')
    
    def import_gpc_names(self, csv_dir):
        """Import CN GPC names"""
        file_path = os.path.join(csv_dir, 'CN.2025.05_GPCNME.csv')
        self.stdout.write('Importing CN GPC names...')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            gpc_names = []
            
            for row in reader:
                gpc_names.append(CNGPCName(
                    gpc_code=row['Gpc code'],
                    gpc_description=row['Gpc description'],
                    date_added=self.parse_date(row.get('Date added')),
                    last_modified=self.parse_date(row.get('Last modified'))
                ))
                
                if len(gpc_names) >= 100:
                    CNGPCName.objects.bulk_create(gpc_names, ignore_conflicts=True)
                    gpc_names = []
            
            if gpc_names:
                CNGPCName.objects.bulk_create(gpc_names, ignore_conflicts=True)
        
        count = CNGPCName.objects.count()
        self.stdout.write(f'Imported {count} CN GPC names')
    
    def import_foods(self, csv_dir, limit=None):
        """Import CN foods"""
        file_path = os.path.join(csv_dir, 'CN.2025.05_FDES.csv')
        self.stdout.write('Importing CN foods...')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            foods = []
            count = 0
            
            for row in reader:
                if limit and count >= limit:
                    break
                
                # Get foreign key references
                food_category = None
                try:
                    food_category = CNFoodCategory.objects.get(code=int(row['Food category code']))
                except (CNFoodCategory.DoesNotExist, ValueError):
                    pass
                
                gpc_product = None
                if row.get('Gpc product code'):
                    try:
                        gpc_product = CNGPCName.objects.get(gpc_code=row['Gpc product code'])
                    except CNGPCName.DoesNotExist:
                        pass
                
                foods.append(CNFood(
                    cn_code=int(row['Cn code']),
                    food_category=food_category,
                    descriptor=row['Descriptor'],
                    abbreviated_descriptor=row['Abbreviated descriptor'],
                    gtin=row.get('Gtin') if row.get('Gtin') else None,
                    product_code=row.get('Product code') if row.get('Product code') else None,
                    brand_owner_name=row.get('Brand owner name') if row.get('Brand owner name') else None,
                    brand_name=row.get('Brand name') if row.get('Brand name') else None,
                    fns_material_number=row.get('FNS Material Number') if row.get('FNS Material Number') else None,
                    source_code=int(row['Source code']) if row.get('Source code') else None,
                    date_added=self.parse_date(row.get('Date added')),
                    last_modified=self.parse_date(row.get('Last modified')),
                    discontinued_date=self.parse_date(row.get('Discontinued date')),
                    form_of_food=row.get('Form of food') if row.get('Form of food') else None,
                    fdc_id=int(row['Fdc id']) if row.get('Fdc id') else None,
                    gpc_product_code=gpc_product
                ))
                
                count += 1
                
                if len(foods) >= 1000:
                    CNFood.objects.bulk_create(foods, ignore_conflicts=True)
                    foods = []
                    self.stdout.write(f'Imported {count} CN foods...')
            
            if foods:
                CNFood.objects.bulk_create(foods, ignore_conflicts=True)
        
        total_count = CNFood.objects.count()
        self.stdout.write(f'Imported {total_count} CN foods total')
    
    def import_nutrient_values(self, csv_dir, limit=None):
        """Import CN nutrient values"""
        file_path = os.path.join(csv_dir, 'CN.2025.05_NUTVAL.csv')
        self.stdout.write('Importing CN nutrient values...')
        
        # Get list of imported food codes if limit is set
        imported_food_codes = None
        if limit:
            imported_food_codes = set(CNFood.objects.values_list('cn_code', flat=True))
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            nutrient_values = []
            count = 0
            
            for row in reader:
                cn_code = int(row['Cn Code'])
                
                # Skip if food not imported (when using limit)
                if imported_food_codes and cn_code not in imported_food_codes:
                    continue
                
                # Get foreign key references
                try:
                    cn_food = CNFood.objects.get(cn_code=cn_code)
                    nutrient = CNNutrient.objects.get(code=int(row['Nutrient code']))
                except (CNFood.DoesNotExist, CNNutrient.DoesNotExist):
                    continue
                
                nutrient_values.append(CNNutrientValue(
                    cn_food=cn_food,
                    nutrient=nutrient,
                    nutrient_value=float(row['Nutrient value']),
                    per_unit=row.get('Per unit', '100g'),
                    value_type_code=int(row['Value type code']) if row.get('Value type code') else None,
                    source_code=int(row['Source code']) if row.get('Source code') else None,
                    date_added=self.parse_date(row.get('Date added')),
                    last_modified=self.parse_date(row.get('Last modified'))
                ))
                
                count += 1
                
                if len(nutrient_values) >= 5000:
                    CNNutrientValue.objects.bulk_create(nutrient_values, ignore_conflicts=True)
                    nutrient_values = []
                    self.stdout.write(f'Imported {count} CN nutrient values...')
            
            if nutrient_values:
                CNNutrientValue.objects.bulk_create(nutrient_values, ignore_conflicts=True)
        
        total_count = CNNutrientValue.objects.count()
        self.stdout.write(f'Imported {total_count} CN nutrient values total')
    
    def import_weights(self, csv_dir, limit=None):
        """Import CN weights/portions"""
        file_path = os.path.join(csv_dir, 'CN.2025.05_WGHT.csv')
        self.stdout.write('Importing CN weights...')
        
        # Get list of imported food codes if limit is set
        imported_food_codes = None
        if limit:
            imported_food_codes = set(CNFood.objects.values_list('cn_code', flat=True))
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            weights = []
            count = 0
            
            for row in reader:
                cn_code = int(row['Cn code'])
                
                # Skip if food not imported (when using limit)
                if imported_food_codes and cn_code not in imported_food_codes:
                    continue
                
                # Get foreign key reference
                try:
                    cn_food = CNFood.objects.get(cn_code=cn_code)
                except CNFood.DoesNotExist:
                    continue
                
                weights.append(CNWeight(
                    cn_food=cn_food,
                    sequence_num=int(row['Sequence num']),
                    amount=float(row['Amount']),
                    measure_description=row['Measure description'],
                    unit_amount=float(row['Unit amount']),
                    type_of_unit=row['Type of unit'],
                    source_code=int(row['Source code']) if row.get('Source code') else None,
                    date_added=self.parse_date(row.get('Date added')),
                    last_modified=self.parse_date(row.get('Last modified'))
                ))
                
                count += 1
                
                if len(weights) >= 5000:
                    CNWeight.objects.bulk_create(weights, ignore_conflicts=True)
                    weights = []
                    self.stdout.write(f'Imported {count} CN weights...')
            
            if weights:
                CNWeight.objects.bulk_create(weights, ignore_conflicts=True)
        
        total_count = CNWeight.objects.count()
        self.stdout.write(f'Imported {total_count} CN weights total')
    
    def update_search_vectors(self):
        """Update search vectors for full-text search"""
        self.stdout.write('Updating CN search vectors...')
        
        try:
            with transaction.atomic():
                CNFood.objects.update(
                    search_vector=SearchVector('descriptor', 'abbreviated_descriptor')
                )
            self.stdout.write('CN search vectors updated successfully')
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not update CN search vectors: {e}')
            )