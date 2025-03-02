Thank you for your interest in our software engineering position - we are excited to see what you can do!
We would like to ask you to complete a small coding task as part of our interview process.
This task should take you around an hour to complete.
The task description is as follows:

## Develop a Streaming JSON Parser

### Objective:
You are required to implement a streaming JSON parser that processes JSON data incrementally in Python.
For this task we consider a subset of JSON, where values consist solely of strings and objects. Escape sequences in strings or duplicate keys in objects are not expected.
The primary motivation for this task is to simulate partial responses as would be encountered in the streaming output of a large language model (LLM).
Even if the input JSON data is incomplete, the parser should be able to return the current state of the parsed JSON object at any given point in time.
This should include partial string-values and objects, but not the keys themselves, i.e. `{"test": "hello", "worl` is a partial representation of `{"test": "hello"}`, but not `{"test": "hello", "worl": ""}`.
Only once the value type of the key is determined should the parser return the key-value pair.
String values on the other hand can be partially returned: `{"test": "hello", "country": "Switzerl` is a partial representation of `{"test": "hello", "country": "Switzerl"}`.

The parser should be efficient in terms of algorithmic complexity.

Create a class named `StreamingJsonParser`.
Implement the following methods within this class:

- `__init__()`: Initializes the parser.
- `consume(buffer: str)`: Consumes a chunk of JSON data.
- `get()`: Returns the current state of the parsed JSON object as an appropriate Python object.

### Examples:

```py
def test_streaming_json_parser():
 parser = StreamingJsonParser()
 parser.consume('{"foo": "bar"}’)
 assert parser.get() == {"foo": "bar"}

def test_chunked_streaming_json_parser():
 parser = StreamingJsonParser()
 parser.consume('{"foo":’)
 parser.consume('"bar’)
 assert parser.get() == {"foo": "bar"}

def test_partial_streaming_json_parser():
 parser = StreamingJsonParser()
 parser.consume('{"foo": "bar’)
 assert parser.get() == {"foo": "bar"}
```

Read the requirements carefully before you start with the task.
If you feel like something is not well specified, feel free to make a reasonable assumption and state it in your solution.
If there are still open questions, let us know (as a response to this E-Mail).
You can use whatever tools you want (Debugger, Editor, Copilot, ChatGPT, …).
Once you're done, send us a python file with your solution as a response to this E-Mail.

Thank you and good luck!