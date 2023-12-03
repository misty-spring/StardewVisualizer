import pathlib
import tkinter as tk
import os
from PIL import Image, ImageTk
from itertools import product

global index
global cv
global photo
global which_img
global max_index


def get_img():
    global photo
    try:
        spliced = Image.open(f'./Files/crop/{which_img}/{index}.png')
        if which_img == "Craftables":
            spliced = spliced.resize((64, 128), resample=0)
        else:
            spliced = spliced.resize(size=(64, 64), resample=0)
    except (FileNotFoundError, NameError):
        spliced = Image.open('./Files/empty.png')
    photo = ImageTk.PhotoImage(spliced)


class Utilities:
    @staticmethod
    def directory_is_empty(directory: str) -> bool:
        try:
            # if there's anything in the directory
            if any(os.scandir(directory)):
                return False

        # if not a directory or no dir
        except (NotADirectoryError, FileNotFoundError):
            os.makedirs(directory)
        return True

    @staticmethod
    def crop(filename, dir_in, dir_out, x, y):
        name, ext = os.path.splitext(filename)
        img = Image.open(os.path.join(dir_in, filename))
        w, h = img.size
        crop_index = 0

        grid = product(range(0, h-h % y, y), range(0, w-w % x, x))
        for i, j in grid:
            box = (j, i, j+x, i+y)
            out = os.path.join(dir_out, f'{crop_index}{ext}')
            img.crop(box).save(out)
            crop_index = crop_index + 1

    @staticmethod
    def get_all(directory: str) -> []:
        parsed = []
        as_path = pathlib.Path(directory)
        raw = as_path.iterdir()
        for item in raw:
            parsed.append(item.name)
        parsed.sort()   # key=lambda x: str(x)[::+1]


class ErrorMsg(tk.Frame):
    def __init__(self, parent):
        global index
        global which_img
        tk.Frame.__init__(self, parent)

        # agregar elementos
        self.msg = tk.Label(self, text="Please copy these images to the Files folder:")
        self.space = tk.Label(self, text=" ")
        self.l1 = tk.Label(self, text="- Craftables (from /TileSheets)")
        self.l2 = tk.Label(self, text="- emotes (from /TileSheets)")
        self.l3 = tk.Label(self, text="- springobjects (from /Maps)")
        self.spaceb = tk.Label(self, text=" ")
        self.ok = tk.Button(self, text="Ok", command=self.ok)

        self.msg.pack(side="top")
        self.space.pack(side="top")
        self.l1.pack(side="top")
        self.l2.pack(side="top")
        self.l3.pack(side="top")
        self.spaceb.pack(side="top")
        self.ok.pack(side="bottom")

    @staticmethod
    def ok():
        exit(0)


class Window(tk.Frame):
    def __init__(self, parent):
        global index
        global which_img
        tk.Frame.__init__(self, parent)

        # agregar elementos
        self.craft = tk.Button(self, text="Craftables", command=self.craft)
        self.springobj = tk.Button(self, text="Spring objects", command=self.spring)
        self.emote = tk.Button(self, text="Emotes", command=self.emote)

        self.craft.pack(side="top")
        self.springobj.pack(side="top")
        self.emote.pack(side="bottom")

        # create index thing
        self.entry = tk.Entry(self)
        self.submit = tk.Button(self, text="Go", command=self.calculate)
        self.back = tk.Button(self, text="Back", command=self.goback)
        self.next = tk.Button(self, text="Next", command=self.forward)
        self.output = tk.Label(self, text=f'{index}')

    def craft(self):
        global which_img
        global max_index
        max_index = 287
        which_img = "Craftables"
        self.change_window()

    def emote(self):
        global which_img
        global max_index
        max_index = 63
        which_img = "emotes"
        self.change_window()

    def spring(self):
        global which_img
        global max_index
        max_index = 935
        which_img = "springobjects"
        self.change_window()

    def change_window(self):
        global cv
        global index
        if which_img == "Craftables":
            cv.config(width=100, height=150)
        else:
            cv.config(width=100, height=100)
        self.craft.destroy()
        self.springobj.destroy()
        self.emote.destroy()
        # lay the widgets out on the screen
        self.output.pack(side="top", fill="x", expand=True)
        # self.panel.pack(side="top", fill="both")
        self.entry.pack(side="top", fill="x", padx=10)
        self.back.pack(side="left")
        self.next.pack(side="right")
        self.submit.pack(side="bottom")
        # for some reason it won't work until you click it
        get_img()
        self.forward()
        self.goback()

    def calculate(self):
        # get the value from the input widget, convert
        # it to an int, and do a calculation
        try:
            global index
            global max_index
            i = int(self.entry.get())
            if i < 0 or i > max_index:
                self.output.configure(text=f"Value can only be \nbetween 0 and {max_index}.")
                return
            result = "%s" % i
            index = i
            self.output.configure(text=index)

            cv.delete("all")
            get_img()
            cv.create_image(90, 50, image=photo, anchor='center')
        except ValueError:
            result = "Please enter digits only"

        # set the output widget to have our result
        self.output.configure(text=result)
        # remove entry
        self.entry.delete(0, 'end')

    def goback(self):
        global index
        global which_img
        # remove entry if exists
        self.entry.delete(0, 'end')
        # actual code to go back an element
        if which_img == "emotes":
            left = index % 4
            if left != 0:
                index = index - left
            else:
                index = index - 4
        else:
            if index == 0:
                return
            index = index - 1
        self.output.configure(text=index)
        # remove image and then get it again
        cv.delete("all")
        get_img()
        cv.create_image(90, 50, image=photo, anchor='center')

    def forward(self):
        global index
        global max_index
        global which_img
        # remove entry if exists
        self.entry.delete(0, 'end')
        # actual code
        # if bigger than max index
        if index >= max_index:
            index = max_index - 1

        if which_img == "emotes":
            # we calculate. % shows the 'rest' (e.g: 9 % 4 = 1)
            left = index % 4
            # going off prev example: added would be 9+4-1=12
            added = index + (4 - left)
            # we check if the result is bigger than max index. if so, just set to max index
            if added >= max_index:
                index = max_index
            # else, index=added. this works whether 'left' is 0 or not. example:
            # if index is 8      if index is 9
            # 8+4-0=12           9+4-1=12
            else:
                index = added
        else:
            index = index + 1
        self.output.configure(text=index)
        # remove image and then get it again
        cv.delete("all")
        get_img()
        cv.create_image(90, 50, image=photo, anchor='center')


# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop


if __name__ == "__main__":
    global index
    global cv
    global photo
    # noinspection PyRedeclaration
    index = 0

    # make tk instance
    root = tk.Tk()
    root.title("Index helper")
    root.resizable(False, False)        # don't allow resizing

    # check crops for all
    dirs = ("springobjects", "Craftables", "emotes")
    for imgname in dirs:
        # get crops OR make them
        if Utilities.directory_is_empty(f"./Files/crop/{imgname}"):
            height = 16
            if imgname == "Craftables":
                height = 32
            try:
                Utilities.crop(f"{imgname}.png", "./Files/", f"./Files/crop/{imgname}", 16, height)
            except FileNotFoundError:
                pathlib.Path.rmdir(pathlib.Path(f"./Files/crop/{imgname}"))
                pathlib.Path.rmdir(pathlib.Path(f"./Files/crop/"))
                root.title("Error")
                root.iconphoto(True,  tk.PhotoImage(file="./Files/icon/64.png"))
                ErrorMsg(root).pack(fill="both", expand=True)
                root.mainloop()

    # addition
    get_img()
    # noinspection PyRedeclaration
    cv = tk.Canvas()
    try:
        _ = which_img
        cv.config(width=100, height=100)
    except NameError:
        cv.config(width=16, height=16)
    cv.pack(side='top', fill='both')
    cv.create_image(50, 50, image=photo, anchor='center')

    # done
    root.iconphoto(True,  tk.PhotoImage(file="./Files/icon/64.png"))
    Window(root).pack(fill="both", expand=True)

    cv.mainloop()
    root.mainloop()
