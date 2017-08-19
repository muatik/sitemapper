from urllib.parse import urlsplit


class Filter:
    def satisfied(self, link):
        raise NotImplementedError()


class FilterStartsWith(Filter):
    def __init__(self, starts_with):
        self.starts_with = starts_with

    def satisfied(self, link):
        return link.startswith(self.starts_with)


class FilterSameHost(Filter):
    def __init__(self, url, check_scheme=False):
        self.check_scheme = check_scheme
        self.base_host = FilterSameHost.extract_domain_name(
            url, check_scheme)

    def satisfied(self, link):
        return self.base_host == FilterSameHost.extract_domain_name(
            link, self.check_scheme)

    @classmethod
    def extract_domain_name(cls, url, include_scheme):
        parts = urlsplit(url)
        domain = parts.netloc

        if domain.startswith("www."):
            domain = domain[4:]

        if include_scheme:
            return "{0.scheme}://{1}/".format(parts, domain)
        else:
            return domain


class FilterExcludeFileTypes(Filter):
    def __init__(self, extensions):
        self.extensions = extensions

    def satisfied(self, link):
        for i in self.extensions:
            if link.endswith(i):
                return False
        return True


class FilterCustom(Filter):
    def __init__(self, custom_filter):
        self.custom_filter = custom_filter

    def satisfied(self, link):
        return self.custom_filter(link)