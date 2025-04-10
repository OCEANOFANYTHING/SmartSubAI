# SmartSubAI

![SmartSubAI](docs/images/SMARTSUBAI.png)

## Advanced Subdomain Enumeration with AI-Powered Risk Assessment

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Configuration](#configuration) • [Examples](#examples) • [Contributing](#contributing)

## Features

- 🔍 **Advanced Subdomain Enumeration**
  - Multi-threaded DNS resolution
  - Custom wordlist support
  - Configurable timeout and retry settings
  - Support for multiple DNS record types (A, AAAA, CNAME)

- 🤖 **AI-Powered Risk Assessment**
  - Powered by Cohere's advanced language models
  - Intelligent scoring of subdomains based on security relevance
  - Detailed reasoning for each risk score
  - Customizable scoring criteria

- 📊 **Comprehensive Reporting**
  - Interactive HTML reports
  - JSON export for integration
  - Detailed subdomain information
  - Risk score breakdowns
  - IP address and DNS record information

## Installation

1. Clone the repository:

```bash
git clone https://github.com/OCEANOFANYTHING/SmartSubAI.git
cd SmartSubAI
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure your Cohere API key:

   - Get your API key from [Cohere](https://cohere.com/)
   - Add it to `config/settings.ini` or set the `SMARTSUBAI_COHERE_KEY` environment variable

## Usage

Basic usage:

```bash
python smartsubai.py -d example.com
```

Advanced options:

```bash
python smartsubai.py -d example.com -w custom_wordlist.txt --threads 20 --limit 100
```

### Command Line Arguments

- `-d, --domain`: Target domain to enumerate (required)
- `-w, --wordlist`: Path to custom wordlist file
- `--threads`: Number of threads for parallel enumeration (default: 10)
- `--limit`: Maximum number of subdomains to enumerate
- `--no-limit`: Remove subdomain limit
- `--test`: Run in test mode (uses mock data)
- `--output-dir`: Custom directory for saving results

## Configuration

The tool can be configured through `config/settings.ini`:

```ini
[AI]
cohere_api_key = your_api_key_here
model = command-r7b-12-2024

[DNS]
timeout = 1
retries = 2
nameservers = 8.8.8.8,8.8.4.4,1.1.1.1,1.0.0.1

[Scanning]
max_threads = 10
max_subdomains = 200
```

## Examples

1. Basic scan:

```bash
python smartsubai.py -d example.com
```

2. Custom wordlist:

```bash
python smartsubai.py -d example.com -w wordlists/custom.txt
```

3. High-performance scan:

```bash
python smartsubai.py -d example.com --threads 20 --no-limit
```

4. Limited scan:

```bash
python smartsubai.py -d example.com --limit 50
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Cohere](https://cohere.com/) for providing the AI capabilities
- [dnspython](https://www.dnspython.org/) for DNS resolution
- All contributors and users of SmartSubAI
- Special thanks to the open-source community for their invaluable support
