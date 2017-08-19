from collections import deque


class LinkNotFound(Exception):
    def __init__(self, link, cause=""):
        self.message = "link '{}' not found. {}".format(link, cause)


class EmptyList(Exception):
    def __init__(self, message):
        self.message = message


class LinkRepository(object):
    STATUS_WAITING = "waiting"
    STATUS_PROCESSING = "processing"
    STATUS_DONE = "done"

    def __init__(self):
        self.waiting = deque()
        self.links = {}

    def append(self, link):
        if link not in self.links:
            self.append_to_waiting(link)

    def append_all(self, links):
        for link in links:
            self.append(link)

    def find_all(self):
        return self.links

    def set_status(self, link, status):
        self.links[link] = status

    def find_one_waiting(self):
        link = self.waiting.pop()
        if not link:
            raise EmptyList("waiting list of links is empty")
        return link

    def is_queue_empty(self):
        return len(self.waiting) == 0

    def append_to_waiting(self, link):
        self.waiting.appendleft(link)
        self.links[link] = LinkRepository.STATUS_WAITING
