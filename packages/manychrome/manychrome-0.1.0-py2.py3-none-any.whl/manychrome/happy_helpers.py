# TODO Update this one as to add many colours before writing the file.
def save_favs(save_as):
    fav_fg = []
    fg_resp = input("Favourite Col#\n")
    fav_fg.append(fg_resp)
    go = ["Col: "+ str(col) + "\n" for col in fav_fg]
    with open(save_as, "a") as fi:
        fi.writelines(go)
    print("file saved: ", save_as)

file = "manychrome/examples/save_my_colors.ini"
# save_favs(file)


def choose_color():
    for i in range(0, 256):
        print(f"\033[38;5;16;48;5;{i}m  Col: {i}  \033[0m", "", f"\033[38;5;255;48;5;{i}m  Col: {i}  \033[0m")



def listme(self, list, heading=None):
    v = [str(item) for item in list]
    if not heading:
        print(f"{"\n".join(v)}")
    else:
        print(f"\33[48;5;{self.fg}m{heading}\033[0m\n{"\n".join(v)}")
