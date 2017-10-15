import public as pub
import dmenu
from templates import ITEMIZE, SUBITEMIZE, ITEM, SUB


class Actions:
    def __init__(self):
        self.DateIsSet = False

    def toggleDateCheck(self):
        self.DateIsSet = not self.DateIsSet

    def kill(self):
        pub.running = False

    def bullet_factory(self, major=True):
        def bullet():
            if not self.DateIsSet:
                pub.LatexDoc.setDate()
                pub.LatexDoc.replace('ITEMIZE', ITEMIZE)
                self.DateIsSet = True

            prompt = "Note (major): " if bullet.major else "Note (minor): "
            note = dmenu.show([], prompt=prompt)

            if bullet.major:
                pub.LatexDoc.replace('ITEM', ITEM % note)
                pub.LatexDoc.deleteEndRange('% SUB %', [])
            else:
                if '% SUB %' not in open(pub.LatexDoc.texFile).read():
                    pub.LatexDoc.replace('ITEM', SUBITEMIZE)

                pub.LatexDoc.replace('SUB', SUB % note)

            pub.LatexDoc.compile()

        bullet.major = major
        return bullet

    def delete_factory(self, major=True):
        def delete():
            if delete.major:
                start = r'\begin{subitemize}'
                end_patterns = [r'% ITEM %']
                pub.LatexDoc.deleteEndRange(start, end_patterns)

            start = r'\item '
            end_patterns = [r'\item ', r'% SUB %', r'% ITEM %', r'\end{itemize}', r'\end{subitemize}']

            pub.LatexDoc.deleteEndRange(start, end_patterns)
            pub.LatexDoc.compile()

        delete.major = major
        return delete
