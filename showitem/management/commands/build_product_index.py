from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

from showitem.models import Product  # 修改為你實際的 app 名稱

class Command(BaseCommand):
    help = "Build FAISS index for product semantic search"

    def handle(self, *args, **options):
        products = Product.objects.all()

        if not products.exists():
            self.stdout.write("No products to index.")
            return

        # 1. 將產品資料轉為文字描述
        texts = [f"{p.name}" for p in products]

        # 2. 使用預訓練模型轉換為向量
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(texts, convert_to_numpy=True)

        # 3. 建立 FAISS index 並加入向量
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)

        # 4. 建立對應的 Product ID 清單
        product_ids = [p.id for p in products]

        # 5. 儲存 index 與 id 映射
        vector_dir = os.path.join("vector_store")
        os.makedirs(vector_dir, exist_ok=True)

        faiss.write_index(index, os.path.join(vector_dir, "product_index.faiss"))
        np.save(os.path.join(vector_dir, "product_ids.npy"), np.array(product_ids))

        self.stdout.write(f"✅ Indexed {len(product_ids)} products.")