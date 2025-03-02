# Streaming JSON Parser

This project implements a streaming JSON parser in Python, as requested for the DeepJudge software engineering
interview.

## Description

The `StreamingJsonParser` class provides functionality to incrementally parse JSON data from a stream. It handles a
subset of JSON, including objects and strings, and is designed to handle partial JSON responses, as would be encountered
in streaming LLM output.

## Features

- Incremental parsing of JSON objects and strings.
- Handles partial JSON data and returns the current state of the parsed object.
- Supports nested objects.
- Clear and well-documented code with type hints.

## Usage

```python
from streaming_json_parser import StreamingJsonParser

parser = StreamingJsonParser()
parser.consume('{"foo":')
parser.consume('"bar"')
result = parser.get()
print(result)  # Output: {"foo": "bar"}
```