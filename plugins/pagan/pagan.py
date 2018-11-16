# -*- coding: latin-1 -*-
from plugins.pagan import generator as generator
import os


class Avatar():

    # Default output path is in the current working directory.
    DEFAULT_OUTPUT_PATH = os.path.join(os.getcwd(), "output/")

    # Default filename.
    DEFAULT_FILENAME = ('pagan')

    DEFAULT_HASHFUN = generator.HASH_MD5

    def __init__(self, inpt, hashfun=DEFAULT_HASHFUN, img_size=128):
        """Initialize the avatar and creates the image."""
        self.img_size = img_size
        self.img = self.__create_image(inpt, hashfun, img_size)

    def __create_image(self, inpt, hashfun, img_size):
        """Creates the avatar based on the input and
        the chosen hash function."""
        if hashfun not in generator.HASHES.keys():
            print ("Unknown or unsupported hash function. Using default: %s"
                   % self.DEFAULT_HASHFUN)
            algo = self.DEFAULT_HASHFUN
        else:
            algo = hashfun
        return generator.generate(inpt, algo, img_size)

    def show(self):
        """Shows a preview of the avatar in an external
        image viewer."""
        self.img.show()

    def change(self, inpt, hashfun=DEFAULT_HASHFUN):
        """Change the avatar by providing a new input.
        Uses the standard hash function if no one is given."""
        self.img = self.__create_image(inpt, hashfun)

    def save(self, path=DEFAULT_OUTPUT_PATH, filename=DEFAULT_FILENAME):
        """Saves a avatar under the given output path to
        a given filename. The file ending ".png" is appended
        automatically. If the path does not exist, it will be
        created. When no parameters are omitted, a default path
        and/or filename will be used."""

        # Creates a path when it does not exist.
        if not os.path.exists(path):
            os.makedirs(path)

        # Cut the .png file ending if one was omitted.
        if filename[-4:] == ".png":
            filename = filename[:-4]
        filename = "{0}_{1}".format(filename, self.img_size)
        # Saves the image under the given filepath.
        filepath = ("%s%s.png" % (path, filename))
        filepath = os.path.join(path, "%s.png" % filename)
        # FIXIT: filepath without SUFFIX, print writes false filename
        print ("Saving: %s" % filepath)
        self.img.save(filepath, 'PNG')
