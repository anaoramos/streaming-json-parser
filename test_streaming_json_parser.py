import unittest

from streaming_json_parser import StreamingJsonParser


class StreamingJsonParserTests(unittest.TestCase):
    def test_streaming_json_parser(self):
        parser = StreamingJsonParser()
        parser.consume('{"foo": "bar"}')
        self.assertEqual(parser.get(), {"foo": "bar"})

    def test_chunked_streaming_json_parser(self):
        parser = StreamingJsonParser()
        parser.consume('{"foo":')
        parser.consume('"bar')
        self.assertEqual(parser.get(), {"foo": "bar"})

    def test_partial_streaming_json_parser(self):
        parser = StreamingJsonParser()
        parser.consume('{"foo": "bar')
        self.assertEqual(parser.get(), {"foo": "bar"})

    def test_partial_string_value(self):
        parser = StreamingJsonParser()
        parser.consume('{"test": "hello", "country": "Switzerl')
        self.assertEqual(parser.get(), {"test": "hello", "country": "Switzerl"})

    def test_partial_key_value_pair(self):
        parser = StreamingJsonParser()
        parser.consume('{"test": "hello", "worl')
        self.assertEqual(parser.get(), {"test": "hello"})

    def test_complete_json(self):
        parser = StreamingJsonParser()
        parser.consume('{"test": "hello", "country": "Switzerland"}')
        self.assertEqual(parser.get(), {"test": "hello", "country": "Switzerland"})

    def test_nested_object_partial(self):
        parser = StreamingJsonParser()
        parser.consume('{"a":{"b":"c"')
        self.assertEqual(parser.get(), {'a': {'b': 'c'}})

    def test_nested_object_complete(self):
        parser = StreamingJsonParser()
        parser.consume('{"a":{"b":"c"}}')
        self.assertEqual(parser.get(), {"a": {"b": "c"}})

    def test_partial_nested_object_key(self):
        parser = StreamingJsonParser()
        parser.consume('{"a":{"b')
        self.assertEqual(parser.get(), {"a": {}})

    def test_partial_nested_object_value(self):
        parser = StreamingJsonParser()
        parser.consume('{"a":{"b": "c')
        self.assertEqual(parser.get(), {'a': {'b': 'c'}})

    def test_empty_object(self):
        parser = StreamingJsonParser()
        parser.consume('{}')
        self.assertEqual(parser.get(), {})

    def test_empty_object_partial(self):
        parser = StreamingJsonParser()
        parser.consume('{')
        self.assertEqual(parser.get(), {})

    def test_empty_object_partial_closing(self):
        parser = StreamingJsonParser()
        parser.consume('{')
        parser.consume('}')
        self.assertEqual(parser.get(), {})

    def test_partial_key_then_complete(self):
        parser = StreamingJsonParser()
        parser.consume('{"test": "hello", "worl')
        parser.consume('d": "complete"}')
        self.assertEqual(parser.get(), {"test": "hello"})

    def test_multiple_nested_objects(self):
        parser = StreamingJsonParser()
        parser.consume('{"a":{"b":"c"}, "d":{"e":"f"}}')
        self.assertEqual(parser.get(), {"a": {"b": "c"}, "d": {"e": "f"}})

    def test_nested_object_multiple_consumes(self):
        parser = StreamingJsonParser()
        parser.consume('{"a":{"b":"c"')
        parser.consume('}}')
        self.assertEqual(parser.get(), {"a": {"b": "c"}})


if __name__ == '__main__':
    unittest.main()
