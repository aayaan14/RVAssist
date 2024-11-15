config = {
    'llm': {
        'provider': 'huggingface',
        'config': {
            'model': 'mistralai/Mistral-7B-Instruct-v0.3',
            'top_p': 0.5
        }
    },
    'embedder': {
        'provider': 'huggingface',
        'config': {
            'model': 'sentence-transformers/all-mpnet-base-v2'
        }
    }
}
