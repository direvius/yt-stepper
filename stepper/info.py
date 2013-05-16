from progressbar import ProgressBar, ETA, ReverseBar, Bar


def progress(gen, progress=''):
    widgets = [progress, Bar('>'), ' ', ETA(), ' ', ReverseBar('<')]
    pbar = ProgressBar(widgets=widgets, maxval=len(gen)).start()
    i = 0
    for elem in gen:
        pbar.update(i)
        i += 1
        yield(elem)
    pbar.finish()
