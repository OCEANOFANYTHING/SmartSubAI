from colorama import Fore, Style, init
from datetime import datetime
import os
import json

# Initialize colorama
init()

def log(msg, level="info"):
    """
    Log a message with the specified level and color.
    
    Args:
        msg (str): The message to log
        level (str): The log level (info, success, error, warning)
    """
    time = datetime.now().strftime("%H:%M:%S")
    color = {
        "info": Fore.CYAN,
        "success": Fore.GREEN,
        "error": Fore.RED,
        "warning": Fore.YELLOW
    }.get(level, Fore.WHITE)
    
    print(f"{color}[{time}] [{level.upper()}] {msg}{Style.RESET_ALL}")

def save_results(domain, results, output_dir="results"):
    """
    Save the results to a JSON file.
    
    Args:
        domain (str): The target domain
        results (dict): The results to save
        output_dir (str): The directory to save the results to
    
    Returns:
        str: The path to the saved file
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create the output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{domain}_{timestamp}_ranked.json"
    filepath = os.path.join(output_dir, filename)
    
    # Write the results to the file
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=4)
    
    return filepath 