# Represents a in-memory tablature of a piece of music
# Can be printed or stored in disk
# E2 has a value of 0
# F2 has a value of 1
# Fs2 has a value of 2

import noteutils

class Tablature:
    def __init__(self):
        self.strings = []
        pass

    def addNote(self, note):
        self.addNotes([note])

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
        for string in range(0, 6):
            whole_str =""
            for step in self.strings:
                whole_str += str(step[5-string])
            print(whole_str)
            

