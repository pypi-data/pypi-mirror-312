import hashlib
import json
import warnings

from scrapy.utils.request import request_fingerprint
from scrapy_splash.dupefilter import splash_request_fingerprint

from scrapypuppeteer import PuppeteerRequest


def puppeteer_request_fingerprint(request, include_headers=None, fallback=None):
    """
    Fingerprint for Puppeteer requests based on Puppeteer action.

    TODO: move to scrapy-puppeteer
    """
    if isinstance(request, PuppeteerRequest):
        fp = request_fingerprint(request, include_headers)
        fp = json.dumps(
            [fp, request.action.endpoint, request.action.payload()], sort_keys=True
        )
        return hashlib.sha1(fp.encode("utf-8")).hexdigest()

    if puppeteer_request := request.meta.get("puppeteer_request"):
        # Contrary to scrapy-splash, PuppeteerMiddleware produces requests with dont_filter=True,
        # so we have to reuse initial request fingerprint to filter them in subsequent crawls.
        return puppeteer_request_fingerprint(
            puppeteer_request, include_headers, fallback
        )

    return (fallback or request_fingerprint)(request, include_headers)


def default_request_fingerprint(request):
    # Temporarily silence warnings so Scrapy won't warn about deprecated fingerprinter on EVERY request
    # TODO: Replace fingerprinter with new implementation (https://jira.ispras.ru/browse/TALCR-1374)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return puppeteer_request_fingerprint(
            request, fallback=splash_request_fingerprint
        )
