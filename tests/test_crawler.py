import mock
import pytest
import requests
from requests import Response

from sitemapper.traverse import find_links, fetch_url_content
from sitemapper.crawler_exceptions import UrlFetchError


def test_find_links_in_text():
    text = "<a href='http://google.com/a.html' />" \
           "<a href='https://www.google.co/#/r' /> " \
           "<a href='https://g.c/k.php' />" \
           "<a href='https://g.c/k.php?r=2' /> " \
           "<a href='https://g.c/k.php?r=3' />" \
           "<a href='https://g.c/k.php?r=3' />" \
           "<a href='/page' />" \
           "<a href='page2' />"  # interpreted as "http://google.com/page2"

    base_host = "https://google.com/"
    links = list(find_links(text, base_host))

    assert len(links) == 8  # find_links does not handle duplicated entries
    assert len(set(links)) == 7

    expected_links = [
        "http://google.com/a.html",
        "https://www.google.co/#/r",
        "https://g.c/k.php",
        "https://g.c/k.php?r=2",
        "https://g.c/k.php?r=3",
        "https://google.com/page",
        "https://google.com/page2"]

    assert sorted(set(links)) == sorted(expected_links)


def test_fetch_url_content_return_text(mocker):
    mocker.patch.object(Response, "text")
    Response.text.__get__ = mock.Mock(return_value="mock content")
    res = Response()
    res.status_code = 200

    mocker.patch.object(requests, "get")
    requests.get.return_value = res
    url = "http://google.com"
    text = fetch_url_content(url, client=requests)

    assert text == "mock content"
    requests.get.assert_called_once_with(url)


def test_fetch_url_content_raise_fetch_error(mocker):
    res = Response()
    res.status_code = 404

    mocker.patch.object(requests, "get")
    requests.get.return_value = res

    with pytest.raises(UrlFetchError):
        fetch_url_content("http://google.com", client=requests)

