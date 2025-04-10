---
layout: default
title: SmartSubAI Documentation
description: Comprehensive guide for SmartSubAI - Advanced Subdomain Enumeration Tool
---

# SmartSubAI Documentation

## Overview

SmartSubAI is an advanced subdomain enumeration tool that combines efficient DNS scanning with AI-powered risk assessment. The tool uses Cohere's language models to analyze discovered subdomains and provide intelligent security insights.

## Key Features

### Subdomain Enumeration
- Multi-threaded DNS resolution
- Support for multiple DNS record types (A, AAAA, CNAME)
- Custom wordlist support
- Configurable scanning parameters

### AI-Powered Analysis
- Powered by Cohere's Command models
- Intelligent risk scoring
- Detailed security insights
- Customizable analysis criteria

### Reporting
- Interactive HTML reports
- JSON export for integration
- Comprehensive subdomain information
- Risk score visualizations

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your Cohere API key:
```bash
# Either set environment variable
export SMARTSUBAI_COHERE_KEY="your-api-key"

# Or add to config/settings.ini
[AI]
cohere_api_key = your-api-key
```

3. Run a basic scan:
```bash
python smartsubai.py -d example.com
```

## Configuration

### AI Settings
```ini
[AI]
cohere_api_key = your-api-key
model = command-r7b-12-2024
```

### DNS Settings
```ini
[DNS]
timeout = 1
retries = 2
nameservers = 8.8.8.8,8.8.4.4,1.1.1.1,1.0.0.1
```

### Scanning Settings
```ini
[Scanning]
max_threads = 10
max_subdomains = 200
```

## Advanced Usage

See [Advanced Usage](advanced_usage.md) for detailed information about:
- Custom wordlists
- Performance tuning
- Report customization
- API integration

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](../CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Advanced Usage](#advanced-usage)
4. [Debug Mode](#debug-mode)
5. [Configuration](#configuration)
6. [Output Files](#output-files)
7. [Troubleshooting](#troubleshooting)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/OCEANOFANYTHING/SmartSubAI.git
cd SmartSubAI
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/macOS
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Basic Usage

### Quick Start
```bash
python smartsubai.py -d example.com
```

This will:
- Enumerate subdomains (limited to 200 by default)
- Generate a JSON report with AI risk scores
- Create an interactive HTML visualization

### Common Options
```bash
# Use a custom wordlist
python smartsubai.py -d example.com -w custom_wordlist.txt

# Change the subdomain limit
python smartsubai.py -d example.com --limit 500

# Remove subdomain limit
python smartsubai.py -d example.com --no-limit

# Use test mode (mock AI responses)
python smartsubai.py -d example.com --test
```

## Debug Mode

### Verbose Output
```bash
# Enable debug logging
python smartsubai.py -d example.com --debug

# Show all HTTP requests
python smartsubai.py -d example.com --debug --show-requests

# Log to file
python smartsubai.py -d example.com --debug --log-file debug.log
```

### Testing Features
```bash
# Test DNS resolution
python smartsubai.py -d example.com --test-dns

# Test AI scoring
python smartsubai.py -d example.com --test-ai

# Test report generation
python smartsubai.py -d example.com --test-report
```

## Output Files

### JSON Report Structure
```json
{
  "domain": "example.com",
  "timestamp": "2024-04-07T12:00:00Z",
  "stats": {
    "total_subdomains": 150,
    "high_risk": 15,
    "medium_risk": 45,
    "low_risk": 90
  },
  "subdomains": [
    {
      "name": "admin.example.com",
      "risk_score": 9,
      "reason": "Administrative interface",
      "ip": "192.168.1.1",
      "status": "HTTPS-200"
    }
  ]
}
```

### HTML Report Features
- Interactive dashboard
- Risk distribution charts
- Sortable subdomain tables
- Search and filter capabilities
- Export functionality
- Mobile-responsive design

## Troubleshooting

### Common Issues

1. **DNS Resolution Failures**
   ```bash
   # Test with alternative DNS servers
   python smartsubai.py -d example.com --dns-server 8.8.8.8
   ```

2. **API Rate Limiting**
   ```bash
   # Enable rate limiting protection
   python smartsubai.py -d example.com --rate-limit 60
   ```

3. **Memory Issues**
   ```bash
   # Enable memory-efficient mode
   python smartsubai.py -d example.com --memory-efficient
   ```

### Debug Commands

```bash
# Check tool version and dependencies
python smartsubai.py --version

# Verify AI configuration
python smartsubai.py --check-ai-config

# Test connectivity
python smartsubai.py --test-connectivity

# Generate debug report
python smartsubai.py --generate-debug-report
```

### Error Messages

| Error Code | Description | Solution |
|------------|-------------|----------|
| E001 | DNS resolution failed | Check network connectivity |
| E002 | API key not found | Set environment variable |
| E003 | Rate limit exceeded | Increase delay between requests |
| E004 | Memory error | Use memory-efficient mode |

For more help or to report issues, visit our [GitHub repository](https://github.com/OCEANOFANYTHING/SmartSubAI/issues). 
