import os
from typing import List

def load_wordlist(file_path: str) -> List[str]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Wordlist file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def filter_directories(
    results: List[dict], 
    status_codes: List[int] = [200, 204, 301, 302]
) -> List[str]:
    return [
        result['url'] 
        for result in results 
        if result['status_code'] in status_codes
    ]