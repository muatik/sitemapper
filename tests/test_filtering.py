from sitemapper.traverse import filter_links
from sitemapper.fitlers import FilterStartsWith, FilterSameHost


def test_filter_links_starting_with():
    links = [
        "http://google.com/search",
        "http://google.com/settings",
        "https://google.com/settings",
        "http://anotherhost.com/page"
    ]
    filters = [
        FilterStartsWith("http://google.com")
    ]
    assert len(list(filter_links(links, filters))) == 2


def test_same_host():
    same_host = FilterSameHost("http://www.google.com/", check_scheme=False)
    assert same_host.satisfied("http://google.com")
    assert same_host.satisfied("https://google.com")
    assert same_host.satisfied("https://google.com/page/section/x/y")
    assert same_host.satisfied("https://www.google.com?a=2")
    assert same_host.satisfied("https://www.google.com?a=2#sec")
    assert same_host.satisfied("https://google.com?r")
    assert same_host.satisfied("https://www.google.com")
    assert not same_host.satisfied("https://www.r.com")
    assert not same_host.satisfied("https://r.com")


def test_same_host_with_scheme():
    same_host = FilterSameHost("https://www.google.com/", check_scheme=True)
    assert not same_host.satisfied("http://google.com")
    assert not same_host.satisfied("http://www.google.com")
    assert same_host.satisfied("https://google.com")
    assert same_host.satisfied("https://www.google.com")
    assert same_host.satisfied("https://www.google.com/a/b/c")
    assert same_host.satisfied("https://www.google.com?a=2")
    assert same_host.satisfied("https://www.google.com?a=2#sec")
    assert not same_host.satisfied("https://www.r.com")


def test_filter_links_same_host():
    links = [
        "http://google.com/search",
        "http://google.com/settings",
        "https://google.com/settings",
        "https://www.google.com/a/b/c",
        "https://www.google.com?a=2#sec",
        "http://anotherhost.com/page"
    ]
    filters = [
        FilterSameHost("http://google.com", check_scheme=False)
    ]
    assert len(list(filter_links(links, filters))) == 5
