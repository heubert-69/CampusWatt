from rag.retriever import EnergyRetriever

retriever = EnergyRetriever()

def retrieve_context(prediction):

    query = (
        f"energy demand {prediction}"
    )

    docs = retriever.search(query)

    filtered = []

    for d in docs:

        if len(d["recommendation"]) > 10:
            filtered.append(d)

    return filtered
