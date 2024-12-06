from colorful import Colorful

"""The intention of stylish is to provide CLI text styling also without color"""
class Stylish(dict, Colorful):
    def __missing__(self, key):
        return str(key)

    def findme(self, doc):
        for key, value in self.items():
            v = Colorful()
            v = self.styleme(value)
            self.update({key: v})
        print(doc.format_map(self))

    """The only reason for these below is to only have to type, 'italics' or 'bold' or whatever when wanting to print in that style. So that all that's needed is to remember what style one wants and can then just type that. Not sure why I didn't just add these to the class Colorful straight though..."""
    def italics(self, txt):
        v = Colorful()
        v.it = True
        v.fg = self.fg
        print(v.styleme(txt))

    def highlight(self, txt):
        v = Colorful()
        v.fg = self.fg
        v.bg = self.bg
        print(v.styleme(txt))

    def underline(self, txt):
        v = Colorful()
        v.ul = True
        v.fg = self.fg
        print(v.styleme(txt))

    def strikethrough(self, txt):
        v = Colorful()
        v.st = True
        v.fg = self.fg
        print(v.styleme(txt))

    def bold(self, txt):
        v = Colorful()
        v.bo = True
        v.fg = self.fg
        print(v.styleme(txt))

    def swap(self, txt):
        # This one is not quite working
        v = Colorful()
        v.sh = True
        v.fg = self.fg
        v.bg = self.bg
        print(v.styleme(txt))



if __name__ == "__main__":

    msg = "This text will be printed one way or another."
    s = Stylish()
    s.fg=89
    s.bg=75
    s.italics(msg)
    s.swap(msg)
    s.bold(msg)
    s.underline("Read This!")
