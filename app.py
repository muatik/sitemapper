import logging
import sys
from time import time
import click

import requests

from sitemapper.fitlers import FilterSameHost, FilterExcludeFileTypes
from sitemapper.link_repository import LinkRepository
from sitemapper.traverse import traverse


@click.command()
@click.option('--url',
              default="https://muatik.github.io/",
              prompt="site url:",
              help='the url of the site to traverse')
def get_sitemap(url):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    lr = LinkRepository()
    client = requests

    filters = [
        FilterSameHost(url),
        FilterExcludeFileTypes(["js", "css", "png", "jpg", "ico"]),
        # FilterCustom(custom_filter=lambda r: "mailto:" not in r)
    ]

    logger.info("===== starting traversing from {} =====".format(url))
    lr.append(url)

    timer_start = time()
    while not lr.is_queue_empty():
        link = lr.find_one_waiting()
        try:
            logger.info("traversing url: {}".format(link))
            lr.set_status(link, LinkRepository.STATUS_PROCESSING)

            links = traverse(link, client, filters)
            lr.append_all(links)

            lr.set_status(link, LinkRepository.STATUS_DONE)
        except Exception as e:
            logger.warning("cannot fetch url. " + str(e))

    elapsed = time() - timer_start
    print(
        "====== completed. found {} links. took {:.3f} seconds. =====".format(
            len(lr.find_all()),
            elapsed))

    for i, link in enumerate(lr.find_all().keys()):
        print("{}. {}".format(i + 1, link))


if __name__ == "__main__":
    get_sitemap()
