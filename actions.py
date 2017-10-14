import public
import dmenu
import datetime

itemize = '''
\\begin{enumerate}
   \item %s
   %% NEXT BULLET %%
\end{enumerate}

%% TIMESTAMP %%'''


class Actions:
    running = True
    public.documentModified = False

    def kill(self):
        self.running = False

    def timestamp(self):
        dt = datetime.date.today()
        stamp = datetime.datetime.strftime(dt, '%B %d, %Y')
        public.LatexDoc.replace('% TIMESTAMP %',
                                '\\section*{%s}' % stamp)

    def bullet(self):
        if not public.documentModified:
            public.documentModified = True
            self.timestamp()
        note = dmenu.show([], prompt="Note: ")
        public.LatexDoc.replace('% BEGIN %', itemize % note)
