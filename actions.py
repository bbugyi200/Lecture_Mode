import public
import dmenu
import templates as temps


def kill():
    public.running = False


def bullet_factory(primary=True):
    def bullet():
        if '% ITEMIZE %' in open(public.LatexDoc.texFile).read():
            public.LatexDoc.putDate()
            public.LatexDoc.replace('ITEMIZE', temps.ITEMIZE + temps.NEW_DATE)

        prompt = "Note: (primary)" if bullet.primary else "Note: (secondary)"
        note = dmenu.show([], prompt=prompt)

        if bullet.primary:
            public.LatexDoc.replace('ITEM', temps.ITEM % note)
        else:
            if '% SUB %' not in open(public.LatexDoc.texFile).read():
                public.LatexDoc.replace('ITEM', temps.SUBITEMIZE)

            public.LatexDoc.replace('SUB', temps.SUB % note)

        public.LatexDoc.compile()

    bullet.primary = primary
    return bullet
