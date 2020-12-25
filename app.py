#!/usr/bin/env python3

from aws_cdk import core

from url_shortener.url_shortener_stack import UrlShortenerStack
from url_shortener.trafficStack import TrafficStack


app = core.App()
UrlShortenerStack(app, "url-shortener")
TrafficStack(app, "test-traffic")

app.synth()
