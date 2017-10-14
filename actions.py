import public


class Actions:
    running = True
    public.documentModified = False

    def kill(self):
        self.running = False
