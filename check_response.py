class TululuResponseError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def check_response(response, message):
    response.raise_for_status()
    if response.url == 'http://tululu.org/':
        raise TululuResponseError(message)
