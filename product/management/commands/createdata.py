from django.core.management.base import BaseCommand
from faker import Faker
import random
from product.models import Unit, Category, Subcategory, SubofSub, Product

class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Generate Units
        for _ in range(5):  # Adjust the range for more or fewer units
            Unit.objects.create(
                name=fake.word(),
                description=fake.text()
            )

        # Generate Categories
        categories = []
        for _ in range(5):  # Adjust the range for more or fewer categories
            category = Category.objects.create(
                name=fake.word(),
                description=fake.text(),
                image=None  # Set to None or use a default image path
            )
            categories.append(category)

        # Generate Subcategories
        subcategories = []
        for _ in range(10):  # Adjust the range for more or fewer subcategories
            subcategory = Subcategory.objects.create(
                name=fake.word(),
                description=fake.text(),
                image=None,
                category=random.choice(categories)
            )
            subcategories.append(subcategory)

        # Generate SubofSubcategories
        for _ in range(15):  # Adjust the range for more or fewer sub-subcategories
            SubofSub.objects.create(
                name=fake.word(),
                description=fake.text(),
                image=None,
                sub_category=random.choice(subcategories)
            )

        # Generate Products
        units = list(Unit.objects.all())
        for _ in range(20):  # Adjust the range for more or fewer products
            Product.objects.create(
                name=fake.word(),
                description=fake.text(),
                price=round(random.uniform(10.0, 1000.0), 2),
                unit=random.choice(units),
                qty=random.randint(1, 100),
                image_one=None,
                image_two=None,
                image_three=None,
                image_four=None,
                image_five=None,
                status=True,
                category=random.choice(categories),
                sold_by=fake.company(),
                material=fake.word(),
                brand=fake.word(),
                color=fake.color_name(),
                size=fake.word(),
                warranty=random.randint(1, 10),
                number_of_box=random.randint(1, 5),
                features=fake.sentence(),
                country_of_origin=fake.country(),
                video=None,
                is_featured=fake.boolean(),
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake data'))
