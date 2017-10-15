import public
import dmenu
import templates as temps


def kill():
    public.running = False


def bullet_factory(major=True):
    def bullet():
        if '% ITEMIZE %' in open(public.LatexDoc.texFile).read():
            public.LatexDoc.replace('ITEMIZE', temps.ITEMIZE + temps.NEW_DATE)

        prompt = "Note (major): " if bullet.major else "Note (minor): "
        note = dmenu.show([], prompt=prompt)

        if bullet.major:
            public.LatexDoc.replace('ITEM', temps.ITEM % note)
            public.LatexDoc.deleteEndRange(['% SUB %'], [])
        else:
            if '% SUB %' not in open(public.LatexDoc.texFile).read():
                public.LatexDoc.replace('ITEM', temps.SUBITEMIZE)

            public.LatexDoc.replace('SUB', temps.SUB % note)

        public.LatexDoc.compile()

    bullet.major = major
    return bullet


def delete_factory(major=True):
    def delete():
        if delete.major:
            start = [r'\begin{subitemize}']
            end = [r'% ITEM %']
            public.LatexDoc.deleteEndRange(start, end)

        start = [r'\item ']
        end = [r'\item ', r'% SUB %', r'% ITEM %', r'\end{itemize}', r'\end{subitemize}']

        public.LatexDoc.deleteEndRange(start, end)
        public.LatexDoc.compile()

    delete.major = major
    return delete
