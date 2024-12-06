# Findme: the intention is to easily find placeholders and other items in text and make them stand out in the whole context of the text. This to quickly get an overview of the text pertaining to the words or fragments of interest in the big scheme of things.
from colorful import Colorful

class FindMe(dict, Colorful):
    def __missing__(self, key):
        return str(key)


    def showme(self, doc):  # Could name to makemepop
        """Add placeholders and alternative text and set the configuration of colors. Can also be used for invoicing, emails, etc to change placeholder text to something different."""
        for key, value in self.items():
            v = Colorful()
            v = self.styleme(value)
            self.update({key: v})
        print(doc.format_map(self))

    def reverseme(self, words):
        pass

    def mirrorme(self, words):
        bg = dict(bg="fg")
        print(f"abc {bg["bg"]} def")


    def but_why(self, doc):  # To find why, what, and how sections of text for text analysis, text edit, and text manipulation purposes.
        """
        a = "Get text"
        b = "Get list of why words from db"
        c = "Find the words in the doc"
        cd = "Split the sentences where the words are present and store this list"
        d = "wrap only the words in the doc so to be able to display the whole text with the sentences"
        e = "return the list with only the sentences, and second, return the text where the words have been highlighted (to be able to check the sentences in the full context)."
        """

        why_words = ["why", "because", "which means", "therefore"]
        r = [doc.partition(why) for why in why_words]
        print(r)

    def but_what(self, doc):
        what_words = ["list of", "what", "essentially"]
        print(what_words)


    def but_how(self, list, doc):
        how_words = ["how", "you do", "first take"]
        print(how_words)




if __name__ == "__main__":

    f = FindMe(
        ought="choose",
        should="can decide to",
        cannot="is ok for now to"
    )
    f.fg = 33
    f.bg = 220

    template = "We have an example where we {ought} to update a lot of the code to be better organised. It {cannot} be arranged like this. We {should} make it a priority."
    f.showme(template)
