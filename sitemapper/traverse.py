import re
from urllib.parse import urlsplit

from sitemapper.crawler_exceptions import UrlFetchError


def fetch_url_content(url, client):
    """
    makes a HTTP GET request to the url by using given client

    :param url: url including scheme and hostname
    :param client: http client
    :return:
    """
    response = client.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise UrlFetchError(url, "got {} not 200".format(response.status_code))


def urljoin(*args):
    """
    Joins given arguments into a url. Trailing but not leading slashes are
    stripped for each argument.
    """
    return "/".join(map(lambda x: str(x).strip("/"), args))


def find_links(text, base_host):
    """
    find links in href attribute of html `<a />` tag elements.
    If href value doesn't start with scheme, base host value will be added as a
    prefix.

    :param text: where links will be searched in
    :param base_host: base host for non-scheme links
    :return: generator of links
    """
    for i in re.findall(r'href=[\'"]?([^\'" >]+)', text):
        if i.startswith("http"):
            yield i
        else:
            yield urljoin(base_host, i)


def filter_links(links, filters):
    """
    filter links via the given filters

    :param links: list of links
    :param filters: list of filters
    :return: generator of filtered links
    """
    for link in links:
        satisfied = True
        for f in filters:
            if not f.satisfied(link):
                satisfied = False
                break
        if satisfied:
            yield link


def traverse(url, client, filters):
    """
    traverse the given url by fetching it, finding links and filtering them.

    :param url: url including scheme and hostname
    :param client: http client
    :param filters: list of filters
    :return: list of found links
    """
    base_host = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    content = fetch_url_content(url, client)
    links = set(find_links(content, base_host))
    site_links = filter_links(links, filters)
    return site_links


