from progressbar import ProgressBar, ETA, ReverseBar, Bar


class DefaultProgressBar(ProgressBar):
    def __init__(self, maxval, caption=''):
        widgets = [caption, Bar('>'), ' ', ETA(), ' ', ReverseBar('<')]
        super(DefaultProgressBar, self).__init__(widgets=widgets, maxval=maxval)


def progress(gen, caption='', pb_class=DefaultProgressBar):
    pbar = pb_class(len(gen), caption).start()
    i = 0
    for elem in gen:
        pbar.update(i)
        i += 1
        yield(elem)
    pbar.finish()
