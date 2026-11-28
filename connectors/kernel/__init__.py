"""Shared marketplace adapter kernel."""

from .errors import (AuthError, EntitlementError, MarketplaceError, ModerationError,
                     RateLimitError, TransientError, ValidationError)
from .http import HttpAdapter, RateLimiter
from .profile import CapabilityProfile, load

__all__ = [
    "AuthError", "EntitlementError", "MarketplaceError", "ModerationError",
    "RateLimitError", "TransientError", "ValidationError",
    "HttpAdapter", "RateLimiter", "CapabilityProfile", "load",
]
