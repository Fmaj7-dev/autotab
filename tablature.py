# Represents a in-memory tablature of a piece of music
# Can be printed or stored in disk
# E2 has a value of 0
# F2 has a value of 1
# Fs2 has a value of 2

import noteutils

class Tablature:
    def __init__(self):
        self.strings = []
        self.time_marks = []

        self.title = "My Song"
        pass

    def setTitle(self, name):
        self.name = name

    

    def addNote(self, note):
        self.addNotes([note])

    def addNotes(self, notes):
        new_pulse = ['-', '-', '-', '-', '-', '-']

        for note in notes:
            print("adding "+str(note))
            #if (note > 28):
            #    continue
            if (note > 18):
                note += 1
            string_number = note//5
            fret_number = note % 5
            print("string_number: "+str(string_number))
            
            new_pulse[string_number ] = fret_number

        self.strings.append( new_pulse )
        self.strings.append( ['-', '-', '-', '-', '-', '-'] )
        self.time_marks.append('  ')

    def addBar(self):
        self.strings.append( ['|', '|', '|', '|', '|', '|'] )
        self.time_marks.append(' ')

    def addTime(self, time_str):
        #self.strings.append( ['-', '-', '-', '-', '-', '-'] )
        time_str = time_str + " "
        self.time_marks.append(time_str)

        for i in range(0, len(time_str)):
            self.strings.append( ['-', '-', '-', '-', '-', '-'] )

    def addChord(self, chord_name):
        pass

    def print(self):
        print("")
        print(self.title)

        # print strings
        for string in range(0, 6):
            whole_str =""
            for step in self.strings:
                whole_str += str(step[5-string])
            print(whole_str)

        # print time marks
        print(print("".join(self.time_marks)))

    def save(self, filename):
        pass
            

