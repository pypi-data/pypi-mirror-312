from entropix import HallucinationAnalyzer

def evaluate_hallucination(data, api_key):
    """
    Evaluate hallucination scores for input-reference pairs.
    """
    analyzer = HallucinationAnalyzer(api_key=api_key)
    results = []

    for input_text, reference in data:
        result = analyzer.evaluate(input_text=input_text, generated_text=reference)
        results.append({
            "input": input_text,
            "reference": reference,
            "hallucination_score": result["hallucination_score"]
        })

    return results
