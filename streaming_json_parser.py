from typing import Dict, Tuple, Any


class StreamingJsonParser:
    """Parses JSON data incrementally."""

    def __init__(self) -> None:
        """Initializes the parser."""
        self.data: Dict[str, Any] = {}
        self.current_key: str or None = None
        self.buffer: str = ""
        self.partial_string: str = ""
        self.partial_key: str = ""

    def _parse_object(self, s: str) -> Tuple[Dict[str, Any], str]:
        """Parses a JSON object.

        Args:
            s (str): The string containing the JSON object to parse.

        Returns:
            Tuple[Dict[str, Any], str]: A tuple containing the parsed object and the remaining string.
        """
        s = s[1:].strip()
        obj: Dict[str, Any] = {}
        while s and not s.startswith("}"):
            key, s = self._parse_any(s)
            s = s.strip()
            if not s.startswith(":"):
                return obj, s
            s = s[1:].strip()
            value, s = self._parse_any(s)
            obj[key] = value
            s = s.strip()
            if s.startswith(","):
                s = s[1:].strip()
        if s and s.startswith("}"):
            return obj, s[1:].strip()
        return obj, s

    def _parse_string(self, s: str) -> Tuple[str, str]:
        """Parses a JSON string.

        Args:
            s (str): The string containing the JSON string to parse.

        Returns:
            Tuple[str, str]: A tuple containing the parsed string value and the remaining string.
        """
        end = s.find('"', 1)
        if end == -1:
            self.partial_string += s[1:]
            return s[1:], ""
        value = s[1:end]
        s = s[end + 1:]
        if self.partial_string:
            value = self.partial_string + value
            self.partial_string = ""
        return value, s

    def _parse_any(self, s: str) -> Tuple[Any, str]:
        """Parses any JSON value.

        Args:
            s (str): The string to parse.

        Returns:
            Tuple[Any, str]: A tuple containing the parsed value and the remaining string.

        Raises:
            ValueError: If the string is empty or parsing fails.
        """
        if not s:
            raise ValueError("Empty string")
        if s[0] == "{":
            return self._parse_object(s)
        if s[0] == '"':
            return self._parse_string(s)
        value = ""
        for char in s:
            if char in ",:{}[]\" ":
                break
            value += char
        if value:
            return value, s[len(value):].strip()
        raise ValueError("Parse failed")

    def consume(self, buffer: str) -> None:
        """Consumes a chunk of JSON data.

        Args:
            buffer (str): The JSON data to consume.
        """
        self.buffer += buffer
        while self.buffer:
            try:
                if self.current_key:
                    value, self.buffer = self._parse_any(self.buffer)
                    self.data[self.current_key] = value
                    self.current_key = None
                else:
                    data, self.buffer = self._parse_any(self.buffer)
                    if isinstance(data, dict):
                        self.data.update(data)
            except ValueError:
                if self.buffer.startswith("{"):
                    self._handle_partial_object()
                self.buffer = ""

    def _handle_partial_object(self) -> None:
        """Handles partial JSON objects."""
        s = self.buffer[1:].strip()
        while s and not s.startswith("}"):
            try:
                key, s = self._parse_any(s)
                s = s.strip()
                if not s.startswith(":"):
                    self.current_key = self.partial_key + key if self.partial_key else key
                    self.partial_key = ""
                    break
                s = s[1:].strip()
                try:
                    value, s = self._parse_any(s)
                    self.data[key] = value
                    s = s.strip()
                    if s.startswith(","):
                        s = s[1:].strip()
                except ValueError:
                    self.current_key = self.partial_key + key if self.partial_key else key
                    self.partial_key = ""
                    break
            except ValueError:
                if s and s[0] == '"':
                    key, s = self._parse_string(s)
                    self.partial_key = key
                    break
                break

    def get(self) -> Dict[str, Any]:
        """Returns a copy of the parsed JSON object."""
        return self.data.copy()
