class ColorText:
    def __init__(self, hex_color, text):
        self.color = self.hex_to_rgb(hex_color)
        self.text = text

    def __repr__(self):
        return "<ColorText color=%s text=%s>" % (self.color, self.text)

    @staticmethod
    def hex_to_rgb(hex_color):
        return tuple(int(hex_color.strip("#")[i:i + 2], 16) for i in (0, 2, 4))


class ColorString:
    import re
    split_re = re.compile("\{|\}")

    def __init__(self, text, default_color = "#FFFFFF"):
        tokens = self.split_re.split(text)
        i = 0
        self.tokens = []
        while i < len(tokens):
            if tokens[i].startswith("#"):
                self.tokens.append(ColorText(tokens[i], tokens[i + 1]))
                i += 2
            else:
                self.tokens.append(ColorText(default_color, tokens[i]))
                i += 1

        # self.tokens = [ColorText(tokens[i * 2], tokens[i * 2 + 1]) for i in range(0, len(tokens) // 2)]

    def __repr__(self):
        return "<ColorString tokens=%s>" % self.tokens

    def __str__(self):
        return "".join([ct.text for ct in self.tokens])
