#!/usr/bin/env python3
"""
SmartSubAI - Advanced Subdomain Enumeration Tool
A professional tool for discovering and analyzing subdomains with AI-powered risk assessment.
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path
import json

from core.enumerator import SubdomainEnumerator
from core.ai_filter import AIFilter
from utils.report_generator import generate_html_report

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# ASCII Banner
BANNER = """
███████╗███╗   ███╗ █████╗ ██████╗ ████████╗███████╗██╗   ██╗██████╗  █████╗ ██╗
██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║   ██║██╔══██╗██╔══██╗██║
███████╗██╔████╔██║███████║██████╔╝   ██║   ███████╗██║   ██║██████╔╝███████║██║
╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   ╚════██║██║   ██║██╔══██╗██╔══██║██║
███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   ███████║╚██████╔╝██████╔╝██║  ██║██║
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝
                                                                                 
Advanced Subdomain Enumeration with AI-Powered Risk Assessment
Version 1.0.0 | https://github.com/yourusername/SmartSubAI
"""

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="SmartSubAI - Advanced Subdomain Enumeration Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Basic usage:
    python smartsubai.py -d example.com
  
  With custom wordlist:
    python smartsubai.py -d example.com -w custom_wordlist.txt
  
  Test mode with mock AI:
    python smartsubai.py -d example.com --test
  
  Advanced usage:
    python smartsubai.py -d example.com -w custom_wordlist.txt -t 30 --model command-r7b-12-2024
        """
    )
    
    parser.add_argument("-d", "--domain", required=True, help="Target domain to enumerate")
    parser.add_argument("-w", "--wordlist", default="wordlists/subdomains.txt", help="Path to wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads for enumeration")
    parser.add_argument("--test", action="store_true", help="Run in test mode with mock AI responses")
    parser.add_argument("--model", help="Cohere model to use (default: command-r7b-12-2024)")
    parser.add_argument("--limit", type=int, default=200, help="Maximum number of subdomains to enumerate (default: 200)")
    parser.add_argument("--no-limit", action="store_true", help="Remove subdomain enumeration limit")
    
    return parser.parse_args()

def main():
    """Main entry point for the tool."""
    # Display banner
    print(BANNER)
    
    args = parse_args()
    
    # Initialize components
    enumerator = SubdomainEnumerator(
        domain=args.domain,
        wordlist_path=args.wordlist,
        num_threads=args.threads,
        max_subdomains=None if args.no_limit else args.limit
    )
    
    ai_filter = AIFilter(
        model=args.model,
        test_mode=args.test
    )
    
    try:
        # Enumerate subdomains
        logging.info(f"Starting enumeration for {args.domain}")
        subdomains = enumerator.enumerate()
        
        if not subdomains:
            logging.error("No subdomains found")
            sys.exit(1)
            
        # Score subdomains
        logging.info("Scoring subdomains with AI")
        scored_subdomains = ai_filter.score_subdomains(subdomains)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)
        
        # Prepare results dictionary
        results = {
            "domain": args.domain,
            "scan_time": timestamp,
            "scored_subdomains": scored_subdomains
        }
        
        json_path = results_dir / f"{args.domain}_{timestamp}_ranked.json"
        html_path = results_dir / f"{args.domain}_{timestamp}_report.html"
        
        # Save JSON results
        with open(str(json_path), "w") as f:
            json.dump(results, f, indent=2)
        logging.info(f"Results saved to {json_path}")
        
        # Generate HTML report with the same timestamp
        generate_html_report(args.domain, results, str(results_dir))
        logging.info(f"HTML report generated at {html_path}")
        
        # Display summary
        logging.info("\nTop 10 subdomains by pentesting relevance:")
        for subdomain in sorted(scored_subdomains, key=lambda x: x["score"], reverse=True)[:10]:
            logging.info(f"{subdomain['subdomain']} (Score: {subdomain['score']}) - {subdomain['reason']}")
            
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 