import logging

_LOGGER = logging.getLogger(__name__)


class Client:
    """ """

    def __init__(self, username, password, domain):
        self.username = username
        self.password = password
        self.domain = domain
