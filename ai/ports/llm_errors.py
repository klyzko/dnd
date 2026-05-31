from symtable import Class


class LLMError(Exception):
    """Базовая ошибка работы LLM"""

class LLMTimeoutError(LLMError):
    pass

class LLMRateLimitError(LLMError):
    pass

class LLMUnavailableError(LLMError):
    pass

class LLMResponseFormatError(LLMError):
    pass


class LLMResponseJsonFormatError(LLMError):
    pass