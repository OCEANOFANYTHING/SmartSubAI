import json
import os
from configparser import ConfigParser
import cohere
import sys
from utils.logger import log

class AIFilter:
    """
    AI-powered filter for ranking subdomains based on pentesting relevance.
    Uses Cohere's language models for analysis.
    """
    
    def __init__(self, provider=None, model=None, test_mode=False, config_path="config/settings.ini"):
        """
        Initialize the AI filter with the specified configuration.
        
        Args:
            provider (str, optional): Override the provider from config (must be 'cohere')
            model (str, optional): Override the model from config
            test_mode (bool): If True, use mock data instead of real API calls
            config_path (str): Path to the configuration file
        """
        self.config = ConfigParser()
        self.test_mode = test_mode
        
        # Check if config file exists
        if not os.path.exists(config_path):
            log(f"Config file not found: {config_path}", "warning")
            log("Using default settings", "info")
        else:
            self.config.read(config_path)
        
        # Load AI settings
        try:
            # Use provided provider or get from config
            self.provider = provider or self.config.get("AI", "provider", fallback="cohere").lower()
            
            # Validate provider
            if self.provider != "cohere":
                log("Only Cohere is supported as an AI provider", "error")
                sys.exit(1)
            
            # Get API key from environment or config
            self.api_key = os.environ.get("SMARTSUBAI_COHERE_KEY") or self.config.get("AI", "cohere_api_key", fallback="")
            
            # Use provided model or get from config
            self.model = model or self.config.get("AI", "model", fallback=self._get_default_model())
            self.temperature = self.config.getfloat("AI", "temperature", fallback=0.3)
        except Exception as e:
            log(f"Error loading AI settings: {str(e)}", "error")
            sys.exit(1)
        
        # If we're in test mode, we don't need to validate the API key
        if not self.test_mode:
            # Validate API key
            if not self.api_key or self.api_key in ["YOUR_API_KEY", "YOUR_API_KEY_HERE"]:
                log("Cohere API key not configured. Please set environment variable or update config/settings.ini", "error")
                sys.exit(1)
                
        log(f"Using Cohere as AI provider with model: {self.model}", "info")
    
    def _get_default_model(self):
        """Get the default model for Cohere."""
        return "command-r7b-12-2024"
    
    def score_subdomains(self, subdomains):
        """
        Score the subdomains using Cohere's AI.
        
        Args:
            subdomains (list): List of subdomains to score
            
        Returns:
            list: Scored subdomains with pentesting relevance
        """
        if not subdomains:
            return []
        
        # If we're in test mode, return mock data
        if self.test_mode:
            log("Using mock data for AI scoring (testing mode)", "warning")
            return self._get_mock_results(subdomains)
        
        # Prepare the prompt for AI scoring
        prompt = self._create_scoring_prompt(subdomains)
        
        try:
            # Get the AI response from Cohere
            response = self._cohere_request(prompt)
                
            # Process and format the response
            result = self._process_ai_response(subdomains, response)
            return result
            
        except Exception as e:
            log(f"Error scoring subdomains: {str(e)}", "error")
            # Return a basic structure with error info
            return [{"subdomain": s, "score": 0, "reason": f"Error during scoring: {str(e)}"} for s in subdomains]
    
    def _get_mock_results(self, subdomains):
        """
        Generate mock scoring results for testing without API keys.
        
        Args:
            subdomains (list): List of subdomains to score
            
        Returns:
            list: Mock scored results
        """
        scored = []
        
        # Create mock scores for each subdomain
        for subdomain in subdomains:
            subdomain_name = subdomain.lower()
            
            # Assign a mock score based on the subdomain name
            score = 5  # Default score
            reason = "Standard subdomain with moderate security relevance"
            
            # Increase score for potentially sensitive subdomains
            if any(name in subdomain_name for name in ["admin", "dashboard", "manage", "control"]):
                score = 9
                reason = "Administrative interface with potential access to sensitive controls"
            elif any(name in subdomain_name for name in ["api", "service", "rest", "graphql"]):
                score = 8
                reason = "API endpoint that may contain security vulnerabilities"
            elif any(name in subdomain_name for name in ["dev", "staging", "test", "uat"]):
                score = 7
                reason = "Development/testing environment that may have less security"
            elif any(name in subdomain_name for name in ["db", "database", "sql", "mongo"]):
                score = 9
                reason = "Database-related subdomain with high data sensitivity"
            elif any(name in subdomain_name for name in ["vpn", "remote", "connect"]):
                score = 8
                reason = "Network access point that could provide entry to internal systems"
            elif any(name in subdomain_name for name in ["storage", "s3", "file", "cdn"]):
                score = 6
                reason = "Storage service that may contain sensitive files or data"
            elif any(name in subdomain_name for name in ["auth", "login", "account"]):
                score = 7
                reason = "Authentication-related endpoint with potential security implications"
            
            scored.append({
                "subdomain": subdomain,
                "score": score,
                "reason": reason
            })
        
        # Sort by score (high to low)
        scored = sorted(scored, key=lambda x: x["score"], reverse=True)
        
        return scored
    
    def _create_scoring_prompt(self, subdomains):
        """
        Create a scoring prompt for the AI.
        
        Args:
            subdomains (list): List of subdomains to score
            
        Returns:
            str: The prompt for the AI
        """
        subdomain_list = "\n".join([f"- {sub}" for sub in subdomains])
        
        return f"""
You are a security professional evaluating subdomains for penetration testing.
Rank the following subdomains by their potential security relevance from 1-10:

{subdomain_list}

For each subdomain, provide:
1. A score from 1-10 (10 being highest priority for pentesting)
2. A brief reason for the score

Respond in valid JSON format like this:
[
  {{
    "subdomain": "subdomain1.example.com",
    "score": 8,
    "reason": "Administrative interface with potential access to sensitive controls"
  }},
  ...
]
"""

    def _cohere_request(self, prompt):
        """
        Make a request to the Cohere API.
        
        Args:
            prompt (str): The prompt to send to the API
            
        Returns:
            str: The API response
        """
        try:
            client = cohere.Client(api_key=self.api_key)
            response = client.chat(
                model=self.model,
                message=prompt,
                temperature=self.temperature
            )
            return response.text
        except Exception as e:
            log(f"Cohere API error: {str(e)}", "error")
            raise
    
    def _process_ai_response(self, subdomains, response):
        """
        Process the AI response and format it.
        
        Args:
            subdomains (list): Original list of subdomains
            response (str): The AI response
            
        Returns:
            list: Formatted result with scored subdomains
        """
        try:
            # Try to parse the JSON response
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)
                
                # Ensure we have a list
                if not isinstance(data, list):
                    data = [data]
                
                # Sort by score in descending order
                data = sorted(data, key=lambda x: x.get("score", 0), reverse=True)
                
                return data
            else:
                # If JSON parsing fails, create a basic structure
                log("Failed to parse AI response as JSON", "warning")
                return [{"subdomain": s, "score": 0, "reason": "Could not parse AI response"} for s in subdomains]
                
        except Exception as e:
            log(f"Error processing AI response: {str(e)}", "error")
            return [{"subdomain": s, "score": 0, "reason": f"Error processing AI response: {str(e)}"} for s in subdomains] 