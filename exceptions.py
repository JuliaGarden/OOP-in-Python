class UserAlreadyExistsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class InvalidEmailError(Exception):
    pass

class ContentNotFoundError(Exception):
    pass

class SubscriptionExpiredError(Exception):
    pass