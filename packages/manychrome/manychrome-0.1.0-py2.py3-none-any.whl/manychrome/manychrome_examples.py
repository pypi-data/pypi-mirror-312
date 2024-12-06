from colorful import Colorful
from findme import FindMe
from stylish import Stylish

# From Colorful: simple functions that provide the additional benefit of colours when viewing the data.
"""Simple function to print a list with the added bonus of ability to add colors and highlights"""
heading = "Important"
stuff = ["Super", "Cool", "Stuff"]

"""Use it to print a list"""
ls = Colorful()
ls.listme(stuff)

"""Print the list in color with a heading"""
c = Colorful(fg=213)
c.listme(stuff, heading="Amazingly", heading_style=c)

"""Print the list in color (or not) with different colors for the items vs the heading."""
h = Colorful(fg=56, bg=1, bo=True)
c = Colorful()
c.listme(stuff, heading=heading, heading_style=h)


template = "Once upon a time there was a {noun} who really wanted to {desire}. Everybody knew it would take {verb} and {stuff}..."
doc2 = "Some other stuff here {text} and there is also a {doc}, and {someone} said they really wanted to go outside."


wrap = Stylish(
    noun=" doggo ",
    desire=" jump around ",
    verb=" a joyous attitude ",
    stuff=" heaps of time "
)
wrap.fg = 123
wrap.bg = 129
wrap.it = True
wrap.findme(template)

styled = FindMe(
    text="Named",
    doc="Excellent Book",
    someone="Unnamed"
)
styled.fg = 201
styled.it = True
styled.bo = True
styled.showme(doc2)

s = Colorful(bg=69, it=True)
s.write("This is a colorful highlighted message.")

c = Colorful(fg=195, it=True, bo=True)
c.write("Here is an example that has other colors.")



# TODO >> need to organise the code because right now the classes Colorful and Stylish seems to overlap, so need some structure later when I write more functions with these. Use colorful for colour, stylish for style. But then the FindMe should be elsewhere...

# Example Code
heading = " DOGGOS "
dogs = ["Ziggy", "Bobby", "Dracula", "Leopold"]
d = FindMe()
c = Colorful(fg=204, it=True)
h = Colorful(fg=195, bg=204, bo=True)
heading = h.styleme(heading)
d.listme([c.styleme(dog) for dog in dogs], heading=heading)

nn = FindMe()
nn.fg=47
nn.bg=96
nn.listme(dogs, heading=heading, heading_style=h)


v = FindMe()
v.listme(["here", "we", "have", "dogs", "cats", 1, 4, "teddy"])
j = Colorful(fg=209, it=True)
li = ["here", "we", "have", "dogs", "cats", 1, 4, "teddy"]
bob = [j.styleme(str(item)) for item in li]
v.listme(bob)

m = FindMe()
m.fg = 24

mm = FindMe()
mm.fg = 199
mm.bg=57
mm.bo = True
m.listme(li, heading=" SOME LIST ", heading_style=mm)
