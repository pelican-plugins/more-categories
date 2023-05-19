# More Categories: A Plugin for Pelican

[![Build Status](https://img.shields.io/github/actions/workflow/status/pelican-plugins/more-categories/main.yml?branch=main)](https://github.com/pelican-plugins/more-categories/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-more-categories)](https://pypi.org/project/pelican-more-categories/)
![License](https://img.shields.io/pypi/l/pelican-more-categories?color=blue)

This Pelican plugin adds support for multiple categories per article and nested
categories. It requires Pelican 4.2.0 or newer.

The `example` directory contains a minimal Pelican web site that can be used for testing.

## Installation

This plugin can be installed via:

    python -m pip install pelican-more-categories

As long as you have not explicitly added a `PLUGINS` setting to your Pelican settings file, then the newly-installed plugin should be automatically detected and enabled. Otherwise, you must add `more-categories` to your existing `PLUGINS` list. For more information, please see the [How to Use Plugins](https://docs.getpelican.com/en/latest/plugins.html#how-to-use-plugins) documentation.

## Multiple Categories

To indicate that an article belongs to multiple categories, use a
comma-separated string:

    Category: foo, bar, bazz

This will add the article to the categories `foo`, `bar`, and `bazz`.

### Templates

Existing themes that use `article.category` will display only the first of
these categories, `foo`. This plugin adds `article.categories` that you can
loop over instead. To accommodate this plugin in a theme whether it is present
or not, use:

```jinja2
{% for cat in article.categories or [article.category] %}
    <a href="{{ SITEURL }}/{{ cat.url }}">{{ cat }}</a>{{ ', ' if not loop.last }}
{% endfor %}
```

## Nested Categories

(This is a re-implementation of the `subcategory` plugin.)

To indicate that a category is a child of another category, use a
slash-separated string:

    Category: foo/bar/bazz

This will add the article to the categories `foo/bar/bazz`, `foo/bar` and
`foo`.

### Templates

Existing themes that use `article.category` will display the full path to the
most specific of these categories, `foo/bar/bazz`. For any category `cat`, this
plugin adds `cat.shortname`, which in this case is `bazz`, `cat.parent`, which
in this case is the category `foo/bar`, and `cat.ancestors`, which is a list of
the category’s ancestors, ending with the category itself. For instance, to
also include a link to each of the ancestor categories on an article page, in
case this plugin in present, use:

```jinja2
{% for cat in article.category.ancestors or [article.category] %}
    <a href="{{ SITEURL }}/{{ cat.url }}">{{ cat.shortname or cat }}</a>{{ '/' if not loop.last }}
{% endfor %}
```

Likewise, `category.shortname`, `category.parent`, and `category.ancestors` can
also be used on the category template.

Additionally, this plugin adds `category.children`: a `list` of categories
that have `category` as a parent.

```jinja2
{% for child in category.children %}
    <a href="{{ SITEURL }}/{{child.url}}">{{child.shortname|capitalize}}</a>
{% endfor %}
```

If you need all descendent children and not just the immediate children, you can use the `list` of descendent children: `category.descendents`

### Slug

The slug of a category is generated recursively by slugifying the short name of
the category and its ancestors (preserving slashes):

    slug-of-(foo/bar/baz) := slug-of-foo/slug-of-bar/slug-of-baz

### Category Folders

To specify categories using the directory structure, you can configure
`PATH_METADATA` to extract the article path into the `category` metadata. The
following settings would use the entire structure:

```python
    PATH_METADATA = "(?P<category>.*)/.*"
```

If you store all articles in a single `articles/` folder that you want to
ignore for this purpose, use:

```python
    PATH_METADATA = "articles/(?P<category>.*)/.*"
```

### Categories in Templates

The list `categories` of all pairs of categories with their corresponding
articles, which is available in the context and can be used in templates (e.g.
to make a menu of available categories), is ordered lexicographically, so
categories always follow their parent:

    aba
    aba/dat
    abaala

## Contributing

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/pelican-plugins/more-categories/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

## License

This project is licensed under the AGPL-3.0 license.
