from shutil import copyfile, move
import fileinput
import os
import public


class LatexDoc:
    def __init__(self):
        self.texFile = ''
        self.bakFile = ''
        self.oldNotesExist = False

    def build(self):
        self.texFile = 'LaTeX/%s.tex' % public.topic.replace(' ', '_')
        self.bakFile = self.texFile.replace('tex', 'bak')

        if os.path.isfile(self.texFile):
            self.oldNotesExist = True
            copyfile(self.texFile, self.bakFile)
        else:
            copyfile('LaTeX/template.tex', self.texFile)
            with fileinput.FileInput(self.texFile, inplace=True) as file:
                for line in file:
                    print(line.replace('(( TITLE ))', public.topic), end='')

    def undoChanges(self):
        if self.oldNotesExist:
            move(self.bakFile, self.texFile)
        else:
            os.remove(self.texFile)
