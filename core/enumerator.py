import dns.resolver
import requests
from concurrent.futures import ThreadPoolExecutor
import time
from utils.logger import log
import threading
import os

class SubdomainEnumerator:
    """Class for enumerating subdomains using various techniques."""
    
    def __init__(self, domain, wordlist_path=None, num_threads=10, max_subdomains=200):
        """
        Initialize the subdomain enumerator.
        
        Args:
            domain (str): Target domain to enumerate
            wordlist_path (str, optional): Path to wordlist file
            num_threads (int, optional): Number of threads for parallel enumeration
            max_subdomains (int, optional): Maximum number of subdomains to enumerate. Set to None for no limit.
        """
        self.domain = domain
        self.wordlist_path = wordlist_path
        self.num_threads = num_threads
        self.max_subdomains = max_subdomains
        self.found_subdomains = set()
        self.lock = threading.Lock()
        
        # Configure DNS resolver with multiple public DNS servers
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 1  # Reduce timeout to 1s
        self.resolver.lifetime = 1  # Reduce lifetime to 1s
        self.resolver.nameservers = [
            '8.8.8.8',   # Google
            '8.8.4.4',   # Google
            '1.1.1.1',   # Cloudflare
            '1.0.0.1',   # Cloudflare
            '9.9.9.9',   # Quad9
            '149.112.112.112',  # Quad9
            '208.67.222.222',  # OpenDNS
            '208.67.220.220'   # OpenDNS
        ]
    
    def enumerate(self):
        """
        Enumerate subdomains using various techniques.
        
        Returns:
            list: List of discovered subdomains
        """
        log(f"Starting subdomain enumeration for {self.domain}", "info")
        
        # Load wordlist if provided
        wordlist = []
        if self.wordlist_path and os.path.exists(self.wordlist_path):
            with open(self.wordlist_path, 'r') as f:
                wordlist = [line.strip() for line in f if line.strip()]
            log(f"Loaded {len(wordlist)} words from wordlist", "info")
        
        # Create thread pool
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            # Submit DNS enumeration tasks
            futures = []
            for word in wordlist:
                if self.max_subdomains and len(self.found_subdomains) >= self.max_subdomains:
                    log(f"Reached maximum subdomain limit of {self.max_subdomains}", "info")
                    break
                    
                subdomain = f"{word}.{self.domain}"
                futures.append(executor.submit(self._check_subdomain, subdomain))
            
            # Wait for all tasks to complete
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    pass  # Suppress individual task errors as they're already logged
        
        # Convert set to list and sort
        subdomains = sorted(list(self.found_subdomains))
        log(f"Found {len(subdomains)} subdomains", "success")
        return subdomains
        
    def _check_subdomain(self, subdomain):
        """
        Check if a subdomain exists using DNS resolution.
        
        Args:
            subdomain (str): Subdomain to check
        """
        try:
            # Check if we've reached the limit
            if self.max_subdomains and len(self.found_subdomains) >= self.max_subdomains:
                return
                
            # Try to resolve the subdomain with multiple record types
            for record_type in ['A', 'AAAA', 'CNAME']:
                try:
                    answers = self.resolver.resolve(subdomain, record_type)
                    if answers:
                        with self.lock:
                            self.found_subdomains.add(subdomain)
                            log(f"Found subdomain: {subdomain} - {answers[0]} ({record_type})", "success")
                        return
                except:
                    continue
                    
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            pass
        except dns.resolver.Timeout:
            pass  # Silently ignore timeouts
        except Exception as e:
            pass  # Silently ignore other errors to reduce noise
    
    def load_wordlist(self, wordlist_path):
        """
        Load a wordlist from a file.
        
        Args:
            wordlist_path (str): Path to the wordlist file
            
        Returns:
            list: List of subdomains from the wordlist
        """
        try:
            with open(wordlist_path, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            log(f"Error loading wordlist: {str(e)}", "error")
            return [] 