import pandas as pd
import random
from faker import Faker

fake = Faker()

category_items = {
    "home": ["Sofa", "Curtain", "Lamp", "Carpet", "Wall Art"],
    "appliances": ["Microwave", "Refrigerator", "Toaster", "Blender", "Washing Machine"],
    "clothes": ["T-Shirt", "Jacket", "Jeans", "Sweater", "Dress"],
    "food": ["Chocolate", "Pasta", "Rice", "Coffee", "Tea"]
}

def generate_image_url(name):
    return f"https://example.com/images/{name.replace(' ', '_').lower()}.jpg"

def generate_product(category):
    item = random.choice(category_items[category])
    name = f"{fake.color_name()} {item}"
    price = int(random.uniform(5, 500))
    description = fake.sentence(nb_words=12)
    images = generate_image_url(item)
    quantity = random.randint(0, 500)
    return {
        "category": category,
        "name": name,
        "price": price,
        "description": description,
        "images": images,
        "quantity": quantity
    }

generated_data = [generate_product(random.choice(list(category_items.keys()))) for _ in range(100)]
df = pd.DataFrame(generated_data)
df.to_csv("generated_products.csv", index=False)
