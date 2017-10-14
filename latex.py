from shutil import copyfile
import fileinput


def build(topic):
    temp = '/tmp/%s.tex' % topic.replace(' ', '_')
    copyfile('template.tex', temp)
    with fileinput.FileInput(temp, inplace=True) as file:
        for line in file:
            print(line.replace('(( TITLE ))', topic), end='')
