import unittest
from unittest.mock import mock_open, patch

from app.parser import (
    ParserContext,
    TextDependenciesParser,
    TomlDependenciesParser,
    YamlDependenciesParser,
)


class TestTomlDependenciesParser(unittest.TestCase):
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=b'{"tool": {"poetry": {"dependencies": {"python": "^3.11", "pytest": "^8.2.2", "requests": "^2.32.3"}}}}',
    )
    @patch("os.path.isfile", return_value=True)
    def test_parse(self, mock_isfile, mock_file):
        pass
        # parser = TomlDependenciesParser("test.toml")
        # dependencies = parser.parse()
        # self.assertEqual(len(dependencies), 1)
        # self.assertEqual(dependencies[0].name, "requests")
        # self.assertEqual(dependencies[0].version, "2.25.1")


class TestTextDependenciesParser(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="requests==2.25.1\n")
    @patch("os.path.isfile", return_value=True)
    def test_parse(self, mock_isfile, mock_file):
        parser = TextDependenciesParser("requirements.txt")
        dependencies = parser.parse()
        self.assertEqual(len(dependencies), 1)
        self.assertEqual(dependencies[0].name, "requests")
        self.assertEqual(dependencies[0].version, "2.25.1")


class TestYamlDependenciesParser(unittest.TestCase):
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="dependencies:\n  requests: 2.25.1\n",
    )
    @patch("os.path.isfile", return_value=True)
    def test_parse(self, mock_isfile, mock_file):
        pass
        # parser = YamlDependenciesParser("test.yml")
        # dependencies = parser.parse()
        # self.assertEqual(dependencies["dependencies"]["requests"], "2.25.1")


class TestParserContext(unittest.TestCase):
    @patch("os.path.isfile", return_value=True)
    def test_get_parser_toml(self, mock_isfile):
        context = ParserContext("test.toml")
        self.assertIsInstance(context.parser, TomlDependenciesParser)

    @patch("os.path.isfile", return_value=True)
    def test_get_parser_txt(self, mock_isfile):
        context = ParserContext("requirements.txt")
        self.assertIsInstance(context.parser, TextDependenciesParser)

    @patch("os.path.isfile", return_value=True)
    def test_get_parser_yaml(self, mock_isfile):
        context = ParserContext("test.yaml")
        self.assertIsInstance(context.parser, YamlDependenciesParser)

    @patch("os.path.isfile", return_value=True)
    def test_get_parser_unsupported(self, mock_isfile):
        with self.assertRaises(ValueError):
            ParserContext("test.json")


if __name__ == "__main__":
    unittest.main()
