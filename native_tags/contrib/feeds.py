"""
Tags which can retrieve and parse RSS and Atom feeds, and return the
results for use in templates.

Based, in part, on the original idea by user baumer1122 and posted to
djangosnippets at http://www.djangosnippets.org/snippets/311/

"""

import datetime
import feedparser
from django.template.loader import render_to_string

from native_tags.decorators import function

def include_feed(feed_url, template_name, num_items=None):
    """
    Parse an RSS or Atom feed and render a given number of its items
    into HTML.
    
    It is **highly** recommended that you use `Django's template
    fragment caching`_ to cache the output of this tag for a
    reasonable amount of time (e.g., one hour); polling a feed too
    often is impolite, wastes bandwidth and may lead to the feed
    provider banning your IP address.
    
    .. _Django's template fragment caching: http://www.djangoproject.com/documentation/cache/#template-fragment-caching
    
    Arguments should be:
    
    1. The URL of the feed to parse.
    
    2. The name of a template to use for rendering the results into HTML.

    3. The number of items to render (if not supplied, renders all
       items in the feed).
           
    The template used to render the results will receive two variables:
    
    ``items``
        A list of dictionaries representing feed items, each with
        'title', 'summary', 'link' and 'date' members.
    
    ``feed``
        The feed itself, for pulling out arbitrary attributes.
    
    Requires the Universal Feed Parser, which can be obtained at
    http://feedparser.org/. See `its documentation`_ for details of the
    parsed feed object.
    
    .. _its documentation: http://feedparser.org/docs/
    
    Syntax::
    
        {% include_feed [feed_url] [num_items] [template_name] %}
    
    Example::
    
        {% include_feed "http://www2.ljworld.com/rss/headlines/" 10 feed_includes/ljworld_headlines.html %}
    
    """
    feed = feedparser.parse(feed_url)
    items = []
    num_items = int(num_items or len(feed['entries']))
    for i in range(num_items):
        pub_date = feed['entries'][i].updated_parsed
        published = datetime.date(pub_date[0], pub_date[1], pub_date[2])
        items.append({ 'title': feed['entries'][i].title,
                       'summary': feed['entries'][i].summary,
                       'link': feed['entries'][i].link,
                       'date': published })
    return render_to_string(template_name, { 'items': items, 'feed': feed })
include_feed = function(include_feed)

def parse_feed(feed_url):
    """
    Parses a given feed and returns the result in a given context
    variable.
    
    It is **highly** recommended that you use `Django's template
    fragment caching`_ to cache the output of this tag for a
    reasonable amount of time (e.g., one hour); polling a feed too
    often is impolite, wastes bandwidth and may lead to the feed
    provider banning your IP address.
    
    .. _Django's template fragment caching: http://www.djangoproject.com/documentation/cache/#template-fragment-caching
    
    Arguments should be:
    
    1. The URL of the feed to parse.
    
    Requires the Universal Feed Parser, which can be obtained at
    http://feedparser.org/. See `its documentation`_ for details of the
    parsed feed object.
    
    .. _its documentation: http://feedparser.org/docs/
    
    Syntax::
    
        {% parse_feed [feed_url] as [varname] %}
    
    Example::
    
        {% parse_feed "http://www2.ljworld.com/rss/headlines/" as ljworld_feed %}
    
    """
    return feedparser.parse(feed_url)
parse_feed = function(parse_feed)

