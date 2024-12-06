# Colorful: simple functions that provide the additional benefit of colours when viewing the data.

from dataclasses import dataclass


class ColorfulConfig:
    def __init__(self, *, default):
        self._default = default

    def __set_name__(self, owner, name):
        self._name = "_" + name

    def __get__(self, obj, type):
        if obj is None:
            return self._default

        return getattr(obj, self._name, self._default)

    def __set__(self, obj, value):
        setattr(obj, self._name, (value))


@dataclass
class Colorful:
    fg: ColorfulConfig = ColorfulConfig(default=None)
    bg: ColorfulConfig = ColorfulConfig(default=None)
    bo: ColorfulConfig = ColorfulConfig(default=False)
    ft: ColorfulConfig = ColorfulConfig(default=False)
    it: ColorfulConfig = ColorfulConfig(default=False)
    ul: ColorfulConfig = ColorfulConfig(default=False)
    st: ColorfulConfig = ColorfulConfig(default=False)
    sh: ColorfulConfig = ColorfulConfig(default=False)


    def write(self, words:str):
        # TODO update to also be able to print lists, dict etc etc.
        """Functions exactly like a normal print statement with the additional bonus
        of being able to set the style and colours."""
        styling = []
        fg = []
        bg = []
        styles = [(self.it, 3), (self.bo, 1), (self.ul, 4), (self.st, 9), (self.sh, 7)]
        colours = [(self.fg, self.bg)]
        for key, value in styles:
            if key:
                s = f"\033[{value};5m"
                styling.append(s)

        for key, value in colours:
            if key:
                f = f"\033[38;5;{key}m"
                fg.append(f)
            if value:
                v = f"\033[48;5;{value}m"
                bg.append(v)
        z = "\033[0m"

        s1 = styling + fg + bg
        styled_text = "".join(s1) + words + z
        print(styled_text)

    def styleme(self, words:str):
        """Exactly the same as write(), but simply return the styled words
        so they can be used in further manipulations."""
        styling = []
        fg = []
        bg = []
        styles = [(self.it, 3), (self.bo, 1), (self.ul, 4), (self.st, 9), (self.sh, 7)]
        colours = [(self.fg, self.bg)]
        for key, value in styles:
            if key:
                s = f"\033[{value};5m"
                styling.append(s)

        for key, value in colours:
            if key:
                f = f"\033[38;5;{key}m"
                fg.append(f)
            if value:
                v = f"\033[48;5;{value}m"
                bg.append(v)
        z = "\033[0m"

        s1 = styling + fg + bg
        styled_text = "".join(s1) + words + z
        return(styled_text)

    def listme(self, list:list, heading=None, heading_style=None):
        v = [self.styleme(str(item)) for item in list]
        if not heading and not heading_style:
            print(f"{"\n".join(v)}")
        elif not heading:
            print(f"{"\n".join(v)}")
        elif heading and heading_style:
            print(f"{heading_style.styleme(str(heading))}\033[0m\n{"\n".join(v)}")
        elif heading and not heading_style:
            print(f"{heading}\033[0m\n{"\n".join(v)}")

        else:
            print("You might want to check you have configured the colors and styles.")

        def reverseme(self, words):
            pass


if __name__ == "__main__":

    items = ["Enjoy the", "simplicity"]
    c = Colorful(fg=33)
    c.listme(items)
