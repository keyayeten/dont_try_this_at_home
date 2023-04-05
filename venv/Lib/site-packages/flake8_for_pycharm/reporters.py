"""
Reporter implementation for pycharm compatible flake8 output
"""
import json

from flake8.formatting import base


class DefaultJSON(base.BaseFormatter):
    """
    Default output class for this reporter
    """

    def __init__(self, options):

        self.newline = ""
        self.first_error: bool = True
        super(DefaultJSON, self).__init__(options)

    def _write(self, output):
        if self.output_fd is not None:
            self.output_fd.write(output + self.newline)
        if self.output_fd is None or self.options.tee:
            print(output, end=self.newline)

    def write_line(self, line):
        """Override write for convenience."""
        self.write(line, None)

    def stop(self):
        self.write_line("]")

    def start(self):
        self.first_error = True
        self.write_line("[")

    def format(self, error):
        """Format a violation."""
        formatted = {
            "type": "warning",
            "module": "",
            "obj": "",
            "line": error.line_number,
            "column": error.column_number,
            "path": error.filename,
            "symbol": error.code,
            "message": f"[{error.code}] {error.text}",
            "message-id": error.code,
        }
        # Pycharm doesn't like when error's column number exceed line's length
        max_line_length = 999
        if error.physical_line:
            max_line_length = len(error.physical_line)
        if error.column_number >= max_line_length:
            formatted["column"] = max_line_length - 1
        # Convert to json and return
        formatted = json.dumps(formatted)
        if self.first_error:
            self.write_line(formatted)
            self.first_error = False
        else:
            self.write_line(", {}".format(formatted))
