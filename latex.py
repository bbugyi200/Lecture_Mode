from shutil import copyfile
import fileinput
import os


def build(topic):
    texFile = 'LaTeX/%s.tex' % topic.replace(' ', '_')

    if os.path.isfile(texFile):
        pass
    else:
        copyfile('LaTeX/template.tex', texFile)
        with fileinput.FileInput(texFile, inplace=True) as file:
            for line in file:
                print(line.replace('(( TITLE ))', topic), end='')
