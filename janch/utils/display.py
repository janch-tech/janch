"""Contains the utilities to display things on the screen

"""


class FixedWidth():
    """Utility to display information in a tabulated manner

    """

    def __init__(self, dimensions: dict):
        """

        Args:
            dimensions: dict containing fields as keys and column width (ints) as values
        """
        self.dim = dimensions
        self.rows = []
        self.delimiter = ''

    def get_header(self):
        """Returns the header row in a tabulated manner

        Returns: str

        """
        ret = ''
        for k, v in self.dim.items():
            ret += FixedWidth.fit(v, str(k))
            ret += self.delimiter

        return ret

    def add_row(self, row: dict):
        """Add row to the collection that is to be displayed

        Args:
            row: dict with fields as keys and values as values

        Returns:

        """
        self.rows.append(row)

    def set_delimiter(self, character):
        """Set delimiter such as '|'

        Args:
            character: str

        Returns:

        """
        self.delimiter = character

    @staticmethod
    def fit(size: int, txt: str):
        """Forces a txt to fit into the required size.

        Long texts get truncated and appended with a '..'

        Args:
            size: int the size of to fit the text in
            txt: str the text that needs to be resized

        Returns:

        """
        # Length
        l = len(txt)

        # dimension of field
        d = size

        # number of spaces to append
        s = d - l if l <= d else 0

        # ellipsis
        e = '..' if l > d else ''

        return txt[0:(l if l <= d else (d - len(e)))] + e + ' ' * s

    def format(self):
        """Iterates the rows and formats them.

        Returns: str is a text blob that can be printed

        """
        ret = ''
        for row in self.rows:
            ret += self.delimiter
            for k, v in self.dim.items():
                ret += FixedWidth.fit(v, str(row[k]))
                ret += self.delimiter

            ret += '\n'

        # The following removes trailing newline
        return ret.rstrip()
