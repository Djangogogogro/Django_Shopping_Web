import csv
from django.core.management.base import BaseCommand
from showitem.models import Category, Product, ProductImage
from user_system.models import Seller, User
from user_system.views import Register_View
from django.contrib.auth.hashers import make_password
class Command(BaseCommand):
    help = 'Import products from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('item.csv', type=str, help='Path to the CSV file.')

    def handle(self, *args, **options):
        ecommerce, created = Seller.objects.get_or_create(
            user_ID='E1',
            defaults={
                'user_name': 'ecommerce',
                'user_mail': 'ecommerce@example.com',
                'user_password': make_password('ecommerce'),
                'rating': 5.0
            }
        )
        ecommerce_seller = Seller.objects.get(user_ID='E1')
        csv_path = options['item.csv']

        with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category_name = row['category'].strip()
                category, _ = Category.objects.get_or_create(name=category_name)

                product = Product.objects.create(
                    category=category,
                    name=row['name'].strip(),
                    price=int(row['price'].strip()),
                    quantity=int(row['quantity'].strip()),
                    description = '\n\n'.join(row['description'].split(';'))
                )

                for image_path in row['images'].split(','):
                    ProductImage.objects.create(
                        product=product,
                        image_path=image_path.strip()
                    )
                ecommerce_seller.products.add(product)
                self.stdout.write(self.style.SUCCESS(f"Imported: {product.name}"))
