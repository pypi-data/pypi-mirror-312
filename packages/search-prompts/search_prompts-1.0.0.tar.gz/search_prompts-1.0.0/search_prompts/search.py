from datasets import load_dataset

def search_prompts(query, dataset_name, config_name, batch_size=1000, max_results=5, chunk_size=5000):
    results = []
    seen_instructions = set()

    try:
        dataset = load_dataset(dataset_name, config_name, split='train', streaming=True)
    except ValueError as e:
        raise ValueError(f"Ошибка загрузки датасета: {e}")

    batch_instructions = []
    total_processed = 0
    chunk_processed = 0

    for i, sample in enumerate(dataset):
        instruction = sample.get('instruction', None)
        if instruction:
            batch_instructions.append(instruction)
            total_processed += 1
            chunk_processed += 1

        if len(batch_instructions) >= batch_size or chunk_processed >= chunk_size:
            for instruction in batch_instructions:
                if query.lower() in instruction.lower() and instruction not in seen_instructions:
                    results.append(instruction)
                    seen_instructions.add(instruction)
                    if len(results) >= max_results:
                        return results
            batch_instructions = []
            if chunk_processed >= chunk_size:
                chunk_processed = 0

    return results
