import subprocess
import shutil
import fileinput
import os
import public
import time
import datetime
import templates as temps


class LatexDoc:

    def __init__(self):
        self.build()
        self.compile()
        self.open()

    def build(self):
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.texFile = 'LaTeX/%s.tex' % public.topic.replace(' ', '_')
        self.pdfPath = r'/home/bryan/Dropbox/notes/Study/Lectures/' + self.texFile.replace('tex', 'pdf').replace('LaTeX/', '')
        self.bakPath = self.pdfPath.replace('pdf', 'bak')

        if os.path.isfile(self.pdfPath):
            shutil.copyfile(self.pdfPath, self.bakPath)
        else:
            shutil.copyfile('LaTeX/template.tex', self.texFile)
            self.replace('TITLE', public.topic)

        self.putDate()

    def putDate(self):
        dt = datetime.date.today()
        stamp = datetime.datetime.strftime(dt, '%B %d, %Y')
        self.replace('DATE',
                     temps.DATE % stamp)

    def compile(self):
        cmd = ['pdflatex', '-file-line-error', '-output-directory', '/tmp',
               self.script_dir + '/' + self.texFile]
        subprocess.Popen(cmd)

        count = 0
        while(True):
            try:
                shutil.move('/tmp/' + os.path.basename(self.pdfPath), self.pdfPath)
                break
            except FileNotFoundError:
                if count < 5:
                    time.sleep(1)
                    count += 1
                else:
                    raise FileNotFoundError()

    def open(self):
        cmd = ['zathura', self.pdfPath]
        subprocess.Popen(cmd)

    def replace(self, target, text):
        with fileinput.FileInput(self.texFile, inplace=True) as file:
            for line in file:
                print(line.replace('% ' + target + ' %', text), end='')

    def undoChanges(self):
        if os.path.isfile(self.bakPath):
            shutil.move(self.bakPath, self.pdfPath)
        else:
            os.remove(self.texFile)
