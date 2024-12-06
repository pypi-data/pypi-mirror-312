from datasets import load_dataset

def load_dataset(name: str, max_samples: int):
    """
    Load a specific dataset and return input-reference pairs.
    """
    if name == "fever":
        dataset = load_dataset("fever", split="train")
        return [(item["claim"], item["evidence"]) for item in dataset[:max_samples]]
    elif name == "simpq":
        dataset = load_dataset("simple_questions_v2", split="train")
        return [(item["question"], item["answer"]) for item in dataset[:max_samples]]
    elif name == "truthfulqa":
        dataset = load_dataset("truthful_qa", split="validation")
        return [(item["question"], item["best_answer"]) for item in dataset[:max_samples]]
    elif name == "factcc":
        dataset = load_dataset("factcc", split="validation")
        return [(item["claim"], item["evidence"]) for item in dataset[:max_samples]]
    else:
        raise ValueError(f"Unsupported dataset: {name}")
