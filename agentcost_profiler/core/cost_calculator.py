"""
Cost calculation module for AgentCost-Profiler.

Provides accurate cost calculations for various LLM providers,
including OpenAI, Anthropic, Google, and others.
"""

import yaml
import json
from typing import Dict, Optional, List
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum


class Provider(Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    COHERE = "cohere"
    MISTRAL = "mistral"
    AZURE = "azure"
    DEEPSEEK = "deepseek"
    LOCAL = "local"


@dataclass
class TokenUsage:
    """Token usage data."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    
    def __post_init__(self):
        if self.total_tokens == 0:
            self.total_tokens = self.prompt_tokens + self.completion_tokens


@dataclass
class CostBreakdown:
    """Detailed cost breakdown."""
    provider: str
    model: str
    prompt_cost: float
    completion_cost: float
    total_cost: float
    token_usage: TokenUsage
    currency: str = "USD"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "provider": self.provider,
            "model": self.model,
            "prompt_cost": round(self.prompt_cost, 6),
            "completion_cost": round(self.completion_cost, 6),
            "total_cost": round(self.total_cost, 6),
            "token_usage": {
                "prompt_tokens": self.token_usage.prompt_tokens,
                "completion_tokens": self.token_usage.completion_tokens,
                "total_tokens": self.token_usage.total_tokens
            },
            "currency": self.currency
        }


class CostCalculator:
    """
    Calculator for LLM API costs.
    
    Supports multiple providers and models with up-to-date pricing.
    Can load custom pricing configurations.
    
    Example:
        calculator = CostCalculator()
        
        usage = TokenUsage(prompt_tokens=1000, completion_tokens=500)
        cost = calculator.calculate(Provider.OPENAI, "gpt-4", usage)
        
        print(f"Cost: ${cost.total_cost:.4f}")
    """
    
    # Default pricing (per 1K tokens)
    DEFAULT_PRICING = {
        Provider.OPENAI.value: {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-4o": {"input": 0.005, "output": 0.015},
            "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
            "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
            "gpt-3.5-turbo-16k": {"input": 0.001, "output": 0.002},
        },
        Provider.ANTHROPIC.value: {
            "claude-3-opus": {"input": 0.015, "output": 0.075},
            "claude-3-sonnet": {"input": 0.003, "output": 0.015},
            "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
            "claude-3-5-sonnet": {"input": 0.003, "output": 0.015},
        },
        Provider.GOOGLE.value: {
            "gemini-pro": {"input": 0.0005, "output": 0.0015},
            "gemini-ultra": {"input": 0.0035, "output": 0.0105},
            "gemini-1.5-pro": {"input": 0.0035, "output": 0.0105},
            "gemini-1.5-flash": {"input": 0.00035, "output": 0.00105},
        },
        Provider.COHERE.value: {
            "command": {"input": 0.001, "output": 0.002},
            "command-light": {"input": 0.0003, "output": 0.0006},
            "command-r": {"input": 0.0005, "output": 0.0015},
            "command-r-plus": {"input": 0.003, "output": 0.015},
        },
        Provider.MISTRAL.value: {
            "mistral-tiny": {"input": 0.00015, "output": 0.00046},
            "mistral-small": {"input": 0.001, "output": 0.003},
            "mistral-medium": {"input": 0.0027, "output": 0.0081},
            "mistral-large": {"input": 0.004, "output": 0.012},
        },
        Provider.DEEPSEEK.value: {
            "deepseek-chat": {"input": 0.00014, "output": 0.00028},
            "deepseek-coder": {"input": 0.00014, "output": 0.00028},
        },
        Provider.LOCAL.value: {
            "default": {"input": 0.0, "output": 0.0},
        }
    }
    
    def __init__(self, pricing_file: Optional[str] = None):
        """
        Initialize the cost calculator.
        
        Args:
            pricing_file: Optional path to custom pricing YAML file
        """
        self._pricing = self.DEFAULT_PRICING.copy()
        
        if pricing_file and Path(pricing_file).exists():
            self._load_pricing(pricing_file)
    
    def _load_pricing(self, file_path: str) -> None:
        """Load pricing from YAML file."""
        try:
            with open(file_path, 'r') as f:
                custom_pricing = yaml.safe_load(f)
                if custom_pricing:
                    self._pricing.update(custom_pricing)
        except Exception as e:
            print(f"Warning: Could not load pricing file: {e}")
    
    def calculate(
        self,
        provider: Provider,
        model: str,
        usage: TokenUsage
    ) -> CostBreakdown:
        """
        Calculate the cost for a given usage.
        
        Args:
            provider: The LLM provider
            model: The model name
            usage: Token usage data
            
        Returns:
            CostBreakdown with detailed cost information
        """
        provider_key = provider.value
        
        # Get pricing for model
        if provider_key not in self._pricing:
            raise ValueError(f"Unknown provider: {provider}")
        
        model_pricing = self._pricing[provider_key].get(model)
        if not model_pricing:
            # Try to find a partial match
            for m, p in self._pricing[provider_key].items():
                if m in model or model in m:
                    model_pricing = p
                    break
            
            if not model_pricing:
                # Use default pricing
                model_pricing = {"input": 0.0, "output": 0.0}
        
        # Calculate costs (price is per 1K tokens)
        prompt_cost = (usage.prompt_tokens / 1000) * model_pricing["input"]
        completion_cost = (usage.completion_tokens / 1000) * model_pricing["output"]
        total_cost = prompt_cost + completion_cost
        
        return CostBreakdown(
            provider=provider_key,
            model=model,
            prompt_cost=prompt_cost,
            completion_cost=completion_cost,
            total_cost=total_cost,
            token_usage=usage
        )
    
    def estimate_cost(
        self,
        provider: Provider,
        model: str,
        prompt_tokens: int,
        expected_completion_tokens: int
    ) -> CostBreakdown:
        """
        Estimate cost before making an API call.
        
        Args:
            provider: The LLM provider
            model: The model name
            prompt_tokens: Expected prompt tokens
            expected_completion_tokens: Expected completion tokens
            
        Returns:
            CostBreakdown with estimated costs
        """
        usage = TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=expected_completion_tokens
        )
        return self.calculate(provider, model, usage)
    
    def get_supported_models(self, provider: Optional[Provider] = None) -> Dict:
        """
        Get list of supported models.
        
        Args:
            provider: Optional provider to filter by
            
        Returns:
            Dictionary of provider -> models
        """
        if provider:
            return {provider.value: list(self._pricing.get(provider.value, {}).keys())}
        return {k: list(v.keys()) for k, v in self._pricing.items()}
    
    def compare_costs(
        self,
        usage: TokenUsage,
        models: List[tuple[Provider, str]]
    ) -> List[CostBreakdown]:
        """
        Compare costs across multiple models.
        
        Args:
            usage: Token usage data
            models: List of (provider, model) tuples
            
        Returns:
            List of CostBreakdown objects sorted by total cost
        """
        results = []
        for provider, model in models:
            try:
                cost = self.calculate(provider, model, usage)
                results.append(cost)
            except ValueError:
                continue
        
        return sorted(results, key=lambda x: x.total_cost)
    
    def get_pricing_info(self, provider: Provider, model: str) -> Optional[Dict]:
        """
        Get pricing information for a specific model.
        
        Args:
            provider: The provider
            model: The model name
            
        Returns:
            Pricing dictionary or None
        """
        return self._pricing.get(provider.value, {}).get(model)
    
    @staticmethod
    def count_tokens(text: str, provider: Provider = Provider.OPENAI) -> int:
        """
        Estimate token count for text.
        
        This is a rough estimation. For accurate counts,
        use the provider's tokenizer.
        
        Args:
            text: The text to count
            provider: The provider (affects tokenization)
            
        Returns:
            Estimated token count
        """
        # Rough estimation: ~4 characters per token for English
        # This varies by language and content
        if provider == Provider.ANTHROPIC:
            # Claude uses ~3.5 chars per token on average
            return len(text) // 3
        elif provider == Provider.GOOGLE:
            # Gemini uses ~4 chars per token
            return len(text) // 4
        else:
            # OpenAI and others ~4 chars per token
            return len(text) // 4
    
    def save_pricing(self, file_path: str) -> None:
        """Save current pricing to YAML file."""
        with open(file_path, 'w') as f:
            yaml.dump(self._pricing, f, default_flow_style=False)
