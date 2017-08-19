class UrlFetchError(Exception):
    def __init__(self, url, cause):
        self.message = "{} cannot be fetched due to: {}".format(url, cause)