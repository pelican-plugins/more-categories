"""Unit tests for the more_categories plugin"""

import os
from shutil import rmtree
from tempfile import mkdtemp
import unittest

from pelican.generators import ArticlesGenerator
from pelican.tests.support import get_context, get_settings

from . import more_categories


class TestArticlesGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_path = mkdtemp(prefix='pelicantests.')
        more_categories.register()
        settings = get_settings()
        settings['DEFAULT_CATEGORY'] = 'default'
        settings['CACHE_CONTENT'] = False
        settings['PLUGINS'] = more_categories
        context = get_context(settings)

        base_path = os.path.dirname(os.path.abspath(__file__))
        test_data_path = os.path.join(base_path, 'test_data')
        cls.generator = ArticlesGenerator(
            context=context,
            settings=settings,
            path=test_data_path,
            theme=settings['THEME'],
            output_path=cls.temp_path,
        )
        cls.generator.generate_context()
        cls.cats = {cat.name: cat for cat, _ in cls.generator.categories}

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.temp_path)

    def test_generate_categories(self):
        """Test whether multiple categories are generated correctly,
        including ancestor categories"""

        cats_expected = ['default', 'foo', 'foo/bar', 'foo/b#az', 'foo/b#az/quux']
        self.assertEqual(sorted(list(self.cats.keys())), sorted(cats_expected))

    def test_extended_family(self):
        """Test whether categories correctly include their extended family"""

        self.assertEqual(
            self.cats['foo/b#az/quux'].parent,
            self.cats['foo/b#az']
        )
        self.assertEqual(
            self.cats['foo/b#az/quux'].ancestors,
            [self.cats['foo'], self.cats['foo/b#az'], self.cats['foo/b#az/quux'], ]
        )
        self.assertEqual(
            self.cats['foo'].children,
            [self.cats['foo/bar'], self.cats['foo/b#az']]
        )
        self.assertEqual(
            self.cats['foo'].descendents,
            [self.cats['foo/bar'], self.cats['foo/b#az'], self.cats['foo/b#az/quux'], ]
        )

    def test_categories_slug(self):
        """Test whether category slug substitutions are used"""

        slugs_generated = [cat.slug for cat in self.cats.values()]
        slugs_expected = ['default', 'foo', 'foo/bar', 'foo/baz', 'foo/baz/quux']
        self.assertEqual(sorted(slugs_generated), sorted(slugs_expected))

    def test_assign_articles_to_categories(self):
        """Test whether articles are correctly assigned to categories,
        including whether articles are not assigned multiple times to the same
        ancestor category"""

        for cat, articles in self.generator.categories:
            self.assertEqual(len(articles), 1)
