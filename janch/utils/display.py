class Display():
    def __init__(self, dimensions: dict):
        self.dim = dimensions
        self.rows = []
        self.delimiter=''

    def get_header(self):
        ret = ''
        for k, v in self.dim.items():
            ret += Display.fit(v, str(k))
            ret += self.delimiter

        return ret

    def add_row(self, row: dict):
        self.rows.append(row)

    def set_delimiter(self, character):
        self.delimiter=character

    @staticmethod
    def fit(size, txt):
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
        ret = ''
        for row in self.rows:
            ret += self.delimiter
            for k, v in self.dim.items():
                ret += Display.fit(v, str(row[k]))
                ret += self.delimiter

            ret += '\n'

        # The following removes trailing newline
        return ret.rstrip()
