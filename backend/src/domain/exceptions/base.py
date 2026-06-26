class DomainException(Exception):
    def __init__(self, message: str, code: str = "DOMAIN_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class EntityNotFoundException(DomainException):
    def __init__(self, entity: str, entity_id: str) -> None:
        super().__init__(f"{entity} with id {entity_id} not found", "NOT_FOUND")


class ValidationException(DomainException):
    def __init__(self, message: str) -> None:
        super().__init__(message, "VALIDATION_ERROR")


class UnauthorizedException(DomainException):
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message, "UNAUTHORIZED")


class BusinessRuleViolationException(DomainException):
    def __init__(self, message: str) -> None:
        super().__init__(message, "BUSINESS_RULE_VIOLATION")
