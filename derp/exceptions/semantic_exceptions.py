from . import SemanticException


class NoLoadedModulesSException(SemanticException):
    pass


class NoPostsAddedSException(SemanticException):
    pass


class EmptyStringLiteralSException(SemanticException):
    pass


class EmptySelectionOrCriteriaSException(SemanticException):
    pass


class SaveSelectionAsCriteriaSException(SemanticException):
    pass


class SaveCriteriaAsSelectionSException(SemanticException):
    pass


class MissingIdSException(SemanticException):
    pass


class MissingCriteriaSException(SemanticException):
    pass


class MissingSelectionSException(SemanticException):
    pass


class MissingModuleSException(SemanticException):
    pass


class ModuleAlreadyLoadedSException(SemanticException):
    pass


class ModuleNotLoadedSException(SemanticException):
    pass


class InvalidDateSException(SemanticException):
    pass


class MissingExactDateSException(SemanticException):
    pass


class CircularReferenceSException(SemanticException):
    pass


class FailToParseExistingSException(SemanticException):
    pass


class FailToLoadExistingSException(SemanticException):
    pass
