#!/usr/bin/env python
SITENAME = 'more_categories test website'

THEME = './theme'

PLUGINS = ['more_categories']

TIMEZONE = 'Europe/Paris'
DEFAULT_DATE_FORMAT = '%-d %B %Y'
LOCALE = {'en_GB.utf8', 'gbr'}
DEFAULT_LANG = 'en'
DEFAULT_DATE = 'fs'

# Menu
MAIN_MENU = True
DISABLE_URL_HASH = True

DIRECT_TEMPLATES = ['index', 'archives']
DEFAULT_PAGINATION = False
SLUGIFY_SOURCE = 'title'
SLUG_REGEX_SUBSTITUTIONS = [
        (r'[^\w\s\-+]', ''),  # remove non-alphabetical/whitespace/'-'/'+' chars
        (r'(?u)\A\s*', ''),  # strip leading whitespace
        (r'(?u)\s*\Z', ''),  # strip trailing whitespace
        (r'[-\s]+', '-'),  # reduce multiple whitespace or '-' to single '-'
    ]

ARTICLE_TRANSLATION_ID = None

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

ARTICLE_URL = '{slug}'
ARTICLE_SAVE_AS = '{slug}.html'
PAGE_URL = '{slug}'
PAGE_SAVE_AS = '{slug}.html'
ARCHIVES_SAVE_AS = ''

AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORY_URL = '{slug}'
CATEGORY_SAVE_AS = '{slug}.html'
TAG_SAVE_AS = ''
TAGS_SAVE_AS = ''

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
