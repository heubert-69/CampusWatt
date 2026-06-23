from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="./models/phi3_energy"
)

def generate_recommendation(
    prediction,
    causal_effect,
    confidence,
    retrieved_docs
):

    prompt = f"""
    Energy Forecast: {prediction}

    Causal Effect:
    {causal_effect}

    Confidence:
    {confidence}

    Knowledge:
    {retrieved_docs}

    Give concise building energy recommendations.
    """

    response = generator(
        prompt,
        temperature=0.2, #balance of creativity and determinism
        top_p=0.9,
        max_new_tokens=128,
        do_sample=False
    )

    return response[0]["generated_text"]
