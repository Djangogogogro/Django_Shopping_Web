import csv
from django.core.management.base import BaseCommand
from showitem.models import Category, Product, ProductImage
from user_system.models import Seller
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Import products from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to the CSV file.')

    def handle(self, *args, **options):
        # 建立預設賣家
        ecommerce, created = Seller.objects.get_or_create(
            user_ID='S2',
            defaults={
                'user_name': 'ecommerce',
                'user_mail': 'ecommerce@example.com',
                'user_password': make_password('ecommerce'),
                'rating': 5.0
            }
        )
        ecommerce_seller = Seller.objects.get(user_ID='S2')
        csv_path = options['csv_path']

        with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category_name = row['category'].strip()
                category, _ = Category.objects.get_or_create(name=category_name)

                product = Product.objects.create(
                    category=category,
                    name=row['name'].strip(),
                    price=int(row['price']),
                    quantity=int(row['quantity']),
                    description='\n\n'.join(row['description'].split(';'))
                )

                for image_path in row['images'].split(','):
                    ProductImage.objects.create(
                        product=product,
                        image_path=image_path.strip()
                    )

                ecommerce_seller.products.add(product)
                self.stdout.write(self.style.SUCCESS(f"Imported: {product.name}"))
