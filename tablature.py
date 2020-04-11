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

        self.size = 0

    def setTitle(self, name):
        self.name = name

    def getSize(self):
        return self.size

    def addNote(self, note):
        self.addNotes([note])

    def addNotes(self, notes):
        new_pulse = ['-', '-', '-', '-', '-', '-']

        for note in notes:

            # ignore notes out of guitar bonds
            if note < 28:
                #print("Note " + noteutils.num2note(note)+ " out of bonds, ignoring")
                continue

            #print("Adding "+noteutils.num2note(note))
            
            note_order = note - noteutils.NoteUtils.offsetGuitar

            if (note_order > 18):
                note_order += 1
            string_number = note_order//5
            fret_number = note_order % 5

            while(string_number > 5):
                string_number -= 1
                fret_number += 5

            #print("string_number: "+str(string_number))

            if fret_number > 9:
                new_pulse = ['--', '--', '--', '--', '--', '--']

            new_pulse[ string_number ] = fret_number

            self.size += 1

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
            

