# Represents a in-memory tablature of a piece of music
# Can be printed or stored in disk

import noteutils

class Tablature:
    def __init__(self):
        self.strings = []
        pass

    def addNotes(self, notes):
        new_pulse = ['-', '-', '-', '-', '-', '-',]

        for note in notes:
            if (note > 18):
                note += 1
            string_number = note//5
            fret_number = note % 5

            new_pulse[string_number] = fret_number

        self.strings.append( new_pulse )
        self.strings.append( ['-', '-', '-', '-', '-', '-',] )

    def addChord(self):
        pass

    def print(self):
        for string in range(5, 0):
            whole_str =""
            for step in self.strings:
                whole_str += step[string]
            print(whole_str)
            print("")

