import subprocess
import shutil
import fileinput
import os
import public as pub
import time
import datetime
from templates import DATE, NEWPAGE
# TODO : Move templates.tex into templates.py


class LatexDoc:
    def __init__(self):
        self.build()
        self.compile()
        self.open()

    def setDate(self):
        dt = datetime.date.today()
        timestamp = datetime.datetime.strftime(dt, '%B %d, %Y')
        if r'\section' in open(self.texFile).read():
            fmtTuple = (NEWPAGE, timestamp)
        else:
            fmtTuple = ('', timestamp)
        self.replace('DATE', DATE % fmtTuple)

    def build(self):
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.texFile = 'LaTeX/%s.tex' % pub.topic.replace(' ', '_')
        self.pdfPath = r'/home/bryan/Dropbox/notes/Study/Lectures/' + self.texFile.replace('tex', 'pdf').replace('LaTeX/', '')
        self.bakPath = self.pdfPath.replace('pdf', 'bak')

        if os.path.isfile(self.pdfPath):
            shutil.copyfile(self.pdfPath, self.bakPath)
        else:
            shutil.copyfile('LaTeX/template.tex', self.texFile)
            self.replace('TITLE', pub.topic)

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
        vanilla_conf = '/home/bryan/Dropbox/dotfiles/.config/zathura/vanilla-zathurarc'
        cmd = ['zathura', '-c', vanilla_conf, self.pdfPath]
        subprocess.Popen(cmd)

    def replace(self, target, text):
        Target = '% ' + target + ' %'
        lineNum = 1
        targetNum = 0
        with open(self.texFile) as file:
            for line in file:
                if Target in line:
                    targetNum = lineNum
                lineNum += 1

        if targetNum == 0:
            raise Exception("targetNum == 0")

        lineNum = 1
        with fileinput.FileInput(self.texFile, inplace=True) as file:
            for line in file:
                if lineNum == targetNum:
                    print(line.replace(Target, text), end='')
                else:
                    print(line, end='')
                lineNum += 1

    def deleteEndRange(self, start, end_patterns):
        startNum = 0
        endNum = 0
        beginNum = 0
        lineNum = 1
        with open(self.texFile) as file:
            for line in file:
                if r'\begin{document}' in line:
                    beginNum = lineNum
                if (start in line) and (beginNum != 0):
                    startNum = lineNum
                lineNum += 1

        if end_patterns == []:
            endNum = startNum
        else:
            lineNum = 1
            with open(self.texFile) as file:
                for line in file:
                    if lineNum > startNum:
                        if any(x in line for x in end_patterns) and (endNum == 0) and (lineNum > beginNum):
                            endNum = lineNum - 1
                    lineNum += 1

        lineNum = 1
        deleteLine = False
        EmptyItemize = False
        EmptySubItemize = False
        with fileinput.FileInput(self.texFile, inplace=True) as file:
            for line in file:
                if lineNum > beginNum:
                    if lineNum == startNum:
                        deleteLine = True

                    if not deleteLine:
                        print(line, end='')

                        if r'\begin{itemize}' in line:
                            EmptyItemize = True
                        if r'\begin{subitemize}' in line:
                            EmptySubItemize = True
                        if r'\item ' in line:
                            EmptyItemize = False
                            EmptySubItemize = False

                    if lineNum == endNum:
                        deleteLine = False
                else:
                    print(line, end='')

                lineNum += 1

        if EmptyItemize:
            self.deleteEndRange(r'\section', [r'% DATE %'])
            pub.Actions.DateIsSet = False

        if EmptySubItemize:
            self.deleteEndRange(r'\begin{subitemize}', [r'% ITEM %'])
