import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional, Callable

class DirHunter:
    def __init__(
        self, 
        base_url: str, 
        max_workers: int = 10, 
        timeout: int = 5
    ):
        self.base_url = base_url.rstrip('/')
        self.max_workers = max_workers
        self.timeout = timeout
        self.found_directories: List[str] = []
        self.live_print_callback: Optional[Callable] = None

    def set_live_print(self, callback: Callable):
        self.live_print_callback = callback
        return self

    def check_directory(self, directory: str) -> Dict[str, Any]:
        full_url = f"{self.base_url}/{directory.lstrip('/')}"
        
        try:
            start_time = time.time()
            response = requests.get(
                full_url, 
                timeout=self.timeout, 
                allow_redirects=True
            )
            response_time = time.time() - start_time
            
            result = {
                'url': full_url,
                'status_code': response.status_code,
                'exists': response.status_code in [200, 204, 301, 302],
                'redirected': response.url != full_url,
                'response_time': round(response_time, 3),
                'directory': directory
            }
            
            if self.live_print_callback:
                self.live_print_callback(result)
            
            return result
        
        except requests.RequestException as e:
            result = {
                'url': full_url,
                'status_code': 'Error',
                'exists': False,
                'error': str(e),
                'response_time': 0,
                'directory': directory
            }
            
            if self.live_print_callback:
                self.live_print_callback(result)
            
            return result

    def scan_directories(
        self, 
        directories: List[str], 
        verbose: bool = False
    ) -> List[Dict[str, Any]]:
        self.found_directories = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.check_directory, dir): dir 
                for dir in directories
            }

            results = []
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                
                if result['exists']:
                    self.found_directories.append(result['url'])

            return results