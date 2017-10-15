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

    def deleteEndRange(self, start_patterns, end_patterns):
        startNum = 0
        endNum = 0
        beginNum = 0
        lineNum = 1
        with open(self.texFile) as file:
            for line in file:
                if r'\begin{document}' in line:
                    beginNum = lineNum
                if any(x in line for x in start_patterns) and (beginNum != 0):
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
        BadItemize = False
        BadSubItemize = False
        with fileinput.FileInput(self.texFile, inplace=True) as file:
            for line in file:
                if lineNum > beginNum:
                    if lineNum == startNum:
                        deleteLine = True

                    if not deleteLine:
                        print(line, end='')

                        if r'\begin{itemize}' in line:
                            BadItemize = True
                        if r'\begin{subitemize}' in line:
                            BadSubItemize = True
                        if r'\item ' in line:
                            BadItemize = False
                            BadSubItemize = False

                    if lineNum == endNum:
                        deleteLine = False
                else:
                    print(line, end='')

                lineNum += 1

        if BadItemize:
            self.replace('DATE', '% ITEMIZE %')
            self.deleteEndRange([r'\begin{itemize}'], [r'% ITEMIZE %'])

        if BadSubItemize:
            self.deleteEndRange([r'\begin{subitemize}'], [r'% ITEM %'])

    def undoChanges(self):
        if os.path.isfile(self.bakPath):
            shutil.move(self.bakPath, self.pdfPath)
        else:
            os.remove(self.texFile)
