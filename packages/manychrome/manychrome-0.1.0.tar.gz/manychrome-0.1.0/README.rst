Manychrome
==========

This is a package predominantly created for those who prefer working
from the CLI. It is to add colours and to style text so to easily make
warnings, notification messages, or finding text when searching for it
easily pop out.

Simple functions, with an intention to allow the user to simply just
type ‘write’, or ‘listme’ or similar to get things done. The function
names are intended to be logical and selfexplanatory and easy to
remember.

   [!NOTE] This package is currently being updated, and pip install is
   not working at the moment. It is in a public reposiory on GitHub so
   feel free to check out the code.

Installation
============

``pip install manychrome``

To uninstall use: ``pip uninstall manychrome``

Background
==========

This package was created because I prefer to work from the terminal and
I wanted a simple way to let certain reminders and text manipulation to
easily grab my attention. I also find myself to to repeat code again and
again, and therefore wanted to create a package that I could just pip
install and use in my different environments without having to repeat it
in different directories.

I am new to coding, and this is my first package, so it might not yet
follow all the right principles yet I hope it’ll over time be helpful to
others who also like some colour on their cli.

My intention is to keep adding to it, and make it extremely user
friendly.

*For the interested one* the name manychrome was selected as a play on
the word monochrome to reflect it’s opposite nature.

What manychrome contains
========================

Classes
-------

.. code:: python

   Colorful()
   Stylish()
   FindMe()

What Colorful() can be used for
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*Colorful:* simple functions that provide the additional benefit of
colours when viewing the data.

*Stylish:* the intention of stylish is to provide CLI text styling also
without color.

*Findme:* the intention is to easily find placeholders and other items
in text and make them stand out in the whole context of the text. This
to quickly get an overview of the text pertaining to the words or
fragments of interest in the big scheme of things. Also provides an
extremely simple and straight forward way to update placeholder text for
emails, documents, and invoice creation etc.

How to Use manychrome
=====================

   Use ``pip install manychrome`` Use pip uninstall manychrome to
   uninstall it

.. code:: python

   from colorful import Colorful
   from stylish import Stylish
   from findme import FindMe

Functions of Colorful()
-----------------------

.. code:: python

   c.write(words)  # To simply print text (strings) with or without colour and style configuration. Use list me to instead view lists (it will pretty print the lists)

   c.styleme(words)  # Identical to write but returns the styed text instead of printing it, so it can be used for further text manipulation.

   c.listme(list)  # An extremely easy way to pretty print lists.
   c.listme(list, heading="ACTIONS", heading_style=c)  # Can add a heading to the list.
   c.listme(list, heading="DIFFERENT", heading_style=h)  # Can use a different instance for the heading style to make it stick out from the text in the list.

   choose_color()  # Just an extremely easy way to see the colours and it's corresponding value in order to select colours to use. Depending on theme settings and colours at the CLI or IDE used the colours might show up differently so good to be able to view them. This function does not belong to any class.

   save_favs()  # Creates an ini file to save the colour favourites to easily find the ones you like without having to remember the values or use choose_color(). This function does not belong to any class.

How to configure the colours when using Colorful()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For ``Colorful()`` the configuration can either be set when initiating
the instance, or by setting the values. This makes for a super simple
view to organise the differences especially when several different
instances are created. Text can contain multiple different combinations
by using several instances of ``Colorful()`` for different fragments of
the text.

The different styles can also be combined so for example, text can be
both underlined, and bold, and italics at the same time. If just wanting
to print normally there is no need to do anything exept instantiate
``Colorful()``. No values are required for normal printing of the text.

.. code:: python

   c = Colorful(fg=1, bg=2, it=True)  # All config for Colorful() can be set inside here, or as shown below
   c.fg = 1  # Sets the foreground (text) colour
   c.bg = 2  # Sets the background colour
   c.it = True  # Set it as True for text in italics
   c.ul = False  # Set ul as True for underlined text
   c.bo = False  # Set bo as True for bold text
   c.st = False  # Set st as True for strikethrough
   c.sh = False  # Set sh as True to shift the colour between the foreground and the background
   c.ft = False  # Set ft as True for faint text. NOTE: This one is having varying effects and is not yet entierly reliable. There are some colours that can be selected in combination that prints very faint text. On my IDE and cli using fg=23, fg=33 prints very faint (but coloured) text.

Functions of FindMe()
---------------------

See below for the current functions and config for class ``FindMe()``

.. code:: python

   # Set the placeholders, no limit set for the number of placeholders.
   f = FindMe(
       placeholder="value"
       company="Awesome company name",
       email="colourful@email.com",
       greeting="Ohoy there",
   )
   # The template containing the placeholders.
   template = "{greeting}. For your template, make sure to wrap the {placeholder} in curly brackets, to update the values, such as {email}, and {company}"

   # Configure the style and colour of the placeholder text.
   f.fg=220
   f.bg=33
   f.it=True

   # Prints the text.
   f.showme(template)

The placeholders are to be wrapped in curly brackets in the template
text, for where you want to change the text.

Functions of Stylish()
----------------------

See below for the current functions and config for class ``Stylish()``.
There is a substantial overlap and ineffective intermixing between
classes so might all get moved to ``Colorful()``.

These provide super self explanatory and easy to remember ways to print
text on the cli in whatever style. The primary function of the name of
these will ignore other configuration settings, thus these can be used
in combination where some text is highlighted, and depending of choice
it will not be affected by that.

.. code:: python

   findme(words)  # TODO check this, it's the same as showme(). Make it make sense.
   bold(words)  # Prints the text bold.
   italics(words)  # Prints the text in italics.
   underline(words)  # Prints the text underlined.
   strikethrough(words)  # Prints the text strikethrough.
   highlight(words)  # Highlights the text in whatever bg colour selected.
   swap(words)  # Swaps the fg / bg colours with each other.

How to use Stylish()
~~~~~~~~~~~~~~~~~~~~

.. code:: python

   For stylish, set config
   s = Stylish()
   s.fg = 117
   s.bg = 218
   # Can do s.it = True etc but the functions below aren't affected by that so they can be used in combination with each others.

Example Usages and Combinations of instances
--------------------------------------------

.. code:: python

   dogs = ["Max", "Bobby", "Dracula", "Leopold"]
   c = Colorful(fg=204, it=True)
   c.listme([c.styleme(dog) for dog in dogs])
