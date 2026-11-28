"""Domain error taxonomy shared by every marketplace adapter."""


class MarketplaceError(Exception):
    code = "unknown"


class AuthError(MarketplaceError):
    code = "unauthorized"


class EntitlementError(MarketplaceError):
    code = "forbidden"


class ValidationError(MarketplaceError):
    code = "bad_request"


class RateLimitError(MarketplaceError):
    code = "rate_limited"


class TransientError(MarketplaceError):
    code = "internal"


class ModerationError(MarketplaceError):
    code = "moderation"
