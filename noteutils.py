
class NoteUtils:
    offsetGuitar = 28

    def __init__(self):
        # guitar note 0 (e2) is actually note 28 in the whole scale
        self.C = "c"
        self.Cs = "cs"

    
# based on https://pages.mtu.edu/~suits/notefreqs.html
def printNotes():
    # c0 frequency
    c_base_freq = 16.3516015625
    # relation between consecutive notes
    factor = 1.059462742437609

    for i in range(0, 66):
        freq = c_base_freq * factor**i
        print(str(i) + "\t" + num2note(i) + "\t" + str(round(freq, 2) ) + "Hz")

# print the name of the note based on the given order of the scale
def num2note(num):
    octave = int(num/12)
    remaining = num - octave*12

    name = ""
    if remaining == 0:
        name = "c"
    elif remaining == 1:
        name = "cs"
    elif remaining == 2:
        name = "d"
    elif remaining == 3:
        name = "ds"
    elif remaining == 4:
        name = "e"
    elif remaining == 5:
        name = "f"
    elif remaining == 6:
        name = "fs"
    elif remaining == 7:
        name = "g"
    elif remaining == 8:
        name = "gs"
    elif remaining == 9:
        name = "a"
    elif remaining == 10:
        name = "as"
    elif remaining == 11:
        name = "b"
    else:
        print("error, note not found "+num)    

    return name + str(octave)

# given a note name (i.e. "e5"), it returns the order of such note
def note2num(note, octave):
    #octave = int( notename[-1] )
    note_name = note
    offset = 0

    if note_name == "c":
        offset = 0
    elif note_name == "cs":
        offset = 1
    elif note_name == "d":
        offset = 2
    elif note_name == "ds":
        offset = 3
    elif note_name == "e":
        offset = 4
    elif note_name == "f":
        offset = 5
    elif note_name == "fs":
        offset = 6
    elif note_name == "g":
        offset = 7
    elif note_name == "gs":
        offset = 8
    elif note_name == "a":
        offset = 9
    elif note_name == "as":
        offset = 10
    elif note_name == "b":
        offset = 11
    else:
        print("error, note not found "+note_name)

    return int(octave)*12 + offset