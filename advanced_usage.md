---
layout: default
title: Advanced Usage
description: Advanced usage guide for SmartSubAI tool
---

# SmartSubAI - Advanced Usage Guide

This document provides detailed information for advanced users and developers working with SmartSubAI.

## Table of Contents

- [Command Line Arguments](#command-line-arguments)
- [Configuration Options](#configuration-options)
- [Custom Wordlists](#custom-wordlists)
- [Output Files](#output-files)
- [AI Providers](#ai-providers)
- [Developer Guidelines](#developer-guidelines)
- [Module Reference](#module-reference)
- [Troubleshooting](#troubleshooting)

## Command Line Arguments

SmartSubAI supports the following command-line arguments:

```
-d, --domain DOMAIN       Target domain to enumerate subdomains for
-w, --wordlist WORDLIST   Path to wordlist file for subdomain brute-forcing
-t, --threads THREADS     Number of threads for parallel enumeration (default: 10)
--timeout TIMEOUT         Timeout for DNS and HTTP requests in seconds (default: 2)
--no-http                 Disable HTTP/HTTPS connectivity checks
--save                    Save the raw subdomain list to a file
--provider {cohere,openai} Override AI provider
--output OUTPUT           Output directory for results (default: results)
-q, --quiet               Quiet mode - only output critical messages
-v, --verbose             Verbose mode - output detailed information
--test                    Test mode - use mock data instead of making API calls
-h, --help                Show help message and exit
```

### Examples

Basic usage with the default Cohere API:
```bash
python smartsubai.py -d example.com
```

Using OpenAI's API instead:
```bash
python smartsubai.py -d example.com --provider openai
```

Increasing threads and timeout for more thorough scanning:
```bash
python smartsubai.py -d example.com -t 30 --timeout 5
```

Disable HTTP checks for faster scanning (DNS only):
```bash
python smartsubai.py -d example.com --no-http
```

## Configuration Options

SmartSubAI uses a configuration file located at `config/settings.ini`. You can customize the following settings:

```ini
[AI]
provider = cohere  # or openai
api_key = YOUR_API_KEY
model = command-r7b-12-2024  # for cohere (or gpt-3.5-turbo for OpenAI)
temperature = 0.3
```

### Parameter Explanation

- `provider`: The AI service provider to use (cohere or openai)
- `api_key`: Your API key for the selected provider
- `model`: 
  - For Cohere: "command-r7b-12-2024" (recommended)
  - For OpenAI: "gpt-3.5-turbo" or "gpt-4" (if available)
- `temperature`: Controls the randomness of the AI output (0.0-1.0)
  - Lower values (0.1-0.3) produce more consistent results
  - Higher values (0.7-1.0) produce more varied results

## Custom Wordlists

SmartSubAI comes with a built-in list of common subdomains, but you can use your own wordlist for more comprehensive scanning. Wordlists should be plain text files with one subdomain prefix per line.

Example wordlist format:
```
www
mail
admin
dev
staging
test
...
```

To use a custom wordlist:
```bash
python smartsubai.py -d example.com -w path/to/wordlist.txt
```

Recommended wordlists:
- [SecLists Subdomain-Names](https://github.com/danielmiessler/SecLists/tree/master/Discovery/DNS)
- [DNSRecon](https://github.com/darkoperator/dnsrecon)
- [Amass](https://github.com/OWASP/Amass)

## Output Files

SmartSubAI generates two types of output files in the `results` directory:

### 1. JSON Results

The JSON file contains the detailed scoring results:
```
results/example.com_YYYYMMDD_HHMMSS_ranked.json
```

### 2. HTML Report

The HTML report provides an interactive visualization of the results:
```
results/example.com_YYYYMMDD_HHMMSS_report.html
```

### 3. Raw Subdomain List (Optional)

If using the `--save` flag, a raw text file with discovered subdomains is saved:
```
results/example.com_raw.txt
```

## AI Providers

### Cohere API

Cohere is the default provider and offers the `command-r7b-12-2024` model with free usage tiers.

1. Create an account at [cohere.com](https://cohere.com)
2. Generate an API key in your account dashboard
3. Add the key to your `config/settings.ini` file

### OpenAI API

To use OpenAI, you'll need to:

1. Create an account at [openai.com](https://openai.com)
2. Generate an API key in your account settings
3. Add the key to your `config/settings.ini` file
4. Change the provider to `openai` in the settings or use the `--provider openai` flag

## Developer Guidelines

### Project Structure

```
SmartSubAI/
│
├── smartsubai.py                 # Main entry point
├── config/
│   └── settings.ini              # Configuration file
│
├── core/
│   ├── enumerator.py             # Subdomain enumeration logic
│   └── ai_filter.py              # AI integration and processing
│
├── utils/
│   ├── logger.py                 # Logging utilities
│   └── report_generator.py       # HTML report generation
│
├── results/                      # Output directory
│
├── docs/                         # Documentation
│
├── tests/                        # Unit tests
│
├── requirements.txt              # Dependencies
└── README.md                     # Project overview
```

### Adding New Features

When extending SmartSubAI, follow these guidelines:

1. **Modularity**: Each component should have a single responsibility
2. **Documentation**: Add docstrings to all new functions and classes
3. **Error Handling**: Use try/except blocks and provide useful error messages
4. **Logging**: Use the existing logger for consistent outputs
5. **Testing**: Add appropriate tests for new functionality

## Module Reference

### Core Modules

#### `core.enumerator.Enumerator`

Handles subdomain discovery using DNS and HTTP requests.

```python
enumerator = Enumerator(max_threads=10, timeout=2)
subdomains = enumerator.enumerate_subdomains(domain, wordlist=None, check_http=True)
```

#### `core.ai_filter.AIFilter`

Processes discovered subdomains using AI to rank them.

```python
ai_filter = AIFilter(config_path="config/settings.ini", mock_mode=False)
results = ai_filter.score_subdomains(domain, subdomains)
```

### Utility Modules

#### `utils.logger`

Provides colored logging functionality.

```python
from utils.logger import log
log("Message", "info")  # Levels: info, success, error, warning
```

#### `utils.report_generator`

Generates HTML reports for visualizing results.

```python
from utils.report_generator import generate_html_report
html_path = generate_html_report(domain, results, output_dir="results")
```

## Troubleshooting

### Common Issues

#### API Key Errors

If you encounter API errors:
1. Verify your API key in `config/settings.ini`
2. Check your API usage limits
3. Use the `--test` flag to run without making API calls

#### DNS Resolution Issues

If subdomain enumeration is slow or fails:
1. Check your internet connection
2. Increase the timeout value (`--timeout 5`)
3. Consider using a different DNS server

#### Rate Limiting

If you're experiencing rate limiting from the API:
1. Reduce the batch size of requests
2. Implement backoff strategies
3. Consider upgrading your API tier

For more assistance, please open an issue on the GitHub repository. 

## AI Integration

SmartSubAI uses Cohere's Command models for intelligent subdomain analysis. The AI component:

- Analyzes subdomain names and patterns
- Assesses potential security risks
- Provides detailed reasoning for scores
- Suggests security improvements

### Cohere Configuration

```ini
[AI]
cohere_api_key = your-api-key
model = command-r7b-12-2024
```

### Environment Variables

```bash
# Set Cohere API key
export SMARTSUBAI_COHERE_KEY="your-api-key"
```

## Performance Tuning

### Thread Management

```bash
# Increase thread count for faster scanning
python smartsubai.py -d example.com --threads 20

# Adjust based on your system's capabilities
python smartsubai.py -d example.com --threads 50
```

### DNS Settings

```ini
[DNS]
timeout = 1
retries = 2
nameservers = 8.8.8.8,8.8.4.4,1.1.1.1,1.0.0.1
```

## Report Customization

### HTML Reports

The HTML reports include:
- Interactive tables
- Risk score visualizations
- DNS record information
- Security recommendations

### JSON Output

Example JSON structure:
```json
{
  "domain": "example.com",
  "scan_time": "2024-04-07T12:00:00",
  "subdomains": [
    {
      "name": "admin.example.com",
      "ip": "192.168.1.1",
      "score": 9,
      "reason": "Administrative subdomain with high security relevance"
    }
  ]
}
```

## API Integration

### Python API

```python
from core.enumerator import SubdomainEnumerator
from core.ai_filter import AIFilter

# Initialize components
enumerator = SubdomainEnumerator("example.com")
ai_filter = AIFilter()

# Run enumeration
subdomains = enumerator.enumerate()

# Score subdomains
results = ai_filter.score_subdomains("example.com", subdomains)
```

## Troubleshooting

### Common Issues

1. DNS Resolution Failures
   - Check your internet connection
   - Verify DNS server settings
   - Adjust timeout values

2. AI Scoring Issues
   - Verify Cohere API key
   - Check API rate limits
   - Ensure proper model configuration

### Debug Mode

```bash
# Enable debug logging
python smartsubai.py -d example.com --debug

# Test mode with mock data
python smartsubai.py -d example.com --test
```

## Best Practices

1. **Scanning**
   - Start with lower thread counts
   - Use appropriate timeouts
   - Monitor system resources

2. **AI Analysis**
   - Keep API keys secure
   - Monitor API usage
   - Use appropriate models

3. **Reporting**
   - Regular backups
   - Secure storage
   - Regular cleanup

## Contributing

See our [Contributing Guidelines](../CONTRIBUTING.md) for details on how to contribute to SmartSubAI.
