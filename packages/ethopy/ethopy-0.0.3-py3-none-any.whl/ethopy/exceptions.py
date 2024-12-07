from typing import Optional, Dict, Any

class LoggerError(Exception):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.details = details or {}
        super().__init__(message)

class DatabaseConnectionError(LoggerError):
    """Raised when database connection fails"""
    pass

class DataInsertionError(LoggerError):
    """Raised when data insertion fails"""
    pass

class ValidationError(LoggerError):
    """Raised when data validation fails"""
    pass

class ConfigurationError(LoggerError):
    """Raised when configuration is invalid"""
    pass

class SessionError(LoggerError):
    """Raised when session operations fail"""
    pass