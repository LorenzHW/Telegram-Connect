class BackendException(Exception):
    def __init__(self, message):
        super(BackendException, self).__init__(message)
