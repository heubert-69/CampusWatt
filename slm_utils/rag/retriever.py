from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

class EnergyRetriever:

    def __init__(self):

        self.encoder = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

        with open(
            "knowledge_base/building_energy_knowledge.json"
        ) as f:
            self.docs = json.load(f)

        texts = [
            d["problem"] + " " + d["cause"]
            for d in self.docs
        ]

        embeddings = self.encoder.encode(texts)

        self.index = faiss.IndexFlatL2(
            embeddings.shape[1]
        )

        self.index.add(
            np.array(embeddings).astype("float32")
        )

    def search(self, query, k=3):

        q = self.encoder.encode([query])

        distances, idx = self.index.search(
            np.array(q).astype("float32"),
            k
        )

        return [
            self.docs[i]
            for i in idx[0]
        ]
