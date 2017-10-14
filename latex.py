import subprocess
import shutil
import fileinput
import os
import public
import time


class LatexDoc:
    def __init__(self):
        self.texFile = ''
        self.bakFile = ''
        self.oldNotesExist = False
        self.pdfDir = r'/home/bryan/Dropbox/notes/Study/Lectures'
        self.script_dir = os.path.dirname(os.path.realpath(__file__))

    def build(self):
        self.texFile = 'LaTeX/%s.tex' % public.topic.replace(' ', '_')
        self.bakFile = self.texFile.replace('tex', 'bak')
        self.pdfFile = self.texFile.replace('tex', 'pdf').replace('LaTeX/', '')

        if os.path.isfile(self.texFile):
            self.oldNotesExist = True
            shutil.copyfile(self.texFile, self.bakFile)
        else:
            shutil.copyfile('LaTeX/template.tex', self.texFile)
            self.replace('% TITLE %', public.topic)

    def compile(self):
        cmd = ['pdflatex', '-file-line-error', '-output-directory', '/tmp',
               self.script_dir + '/' + self.texFile]
        subprocess.Popen(cmd)

        count = 0
        while(True):
            try:
                shutil.move('/tmp/' + self.pdfFile, self.pdfDir + '/' + self.pdfFile)
                break
            except FileNotFoundError:
                if count < 5:
                    time.sleep(1)
                    count += 1
                else:
                    raise FileNotFoundError()

    def open(self):
        cmd = ['zathura', self.pdfDir + '/' + self.pdfFile]
        subprocess.Popen(cmd)

    def replace(self, target, text):
        with fileinput.FileInput(self.texFile, inplace=True) as file:
            for line in file:
                print(line.replace(target, text), end='')

    def undoChanges(self):
        if self.oldNotesExist:
            shutil.move(self.bakFile, self.texFile)
        else:
            os.remove(self.texFile)
