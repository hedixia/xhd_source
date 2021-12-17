import csv

import numpy as np

import helper_func


class Recorder:
    def __init__(self):
        self.store = []
        self.current = dict()

    def __setitem__(self, key, value):
        """
        Store values to recorder.
        Starting symbols:
            !: reserved for !Epoch
            #: control the importance through its count
            _: omitted element in printouts
        :param key: the name of stored attribute, type str
        :param value: the stored value and will be averaged when .capture() is called, type numeric
        :return: None
        """
        value = helper_func.tensor_to_np(value)
        if key in self.current:
            self.current[key].append(value)
        else:
            self.current[key] = [value]

    def epoch(self, epoch):
        self['!Epoch'] = epoch

    def capture(self, verbose=False, nrows=5, ncols=3):
        for i in self.current:
            self.current[i] = np.mean(self.current[i])
        self.store.append(self.current.copy())
        self.current = dict()
        if verbose:
            self.printout(-1, nrows=nrows, ncols=ncols)

        return self.store[-1]

    def printout(self, idx, nrows=5, ncols=3):
        vals = self.store[idx]
        entry_cnt = len(vals)
        display_cap = nrows * ncols - 1
        print('\n')
        print_list = []
        for key in sorted(vals.keys()):
            if key[0] != '_':
                print_list.append('{}: {}'.format(key, vals[key]))
            if len(print_list) >= display_cap:
                print_list.append('Remain {} / total {} entries'.format(entry_cnt - display_cap + 1, entry_cnt))
                break
        for i in range(nrows):
            print(' | '.join(print_list[i * ncols: (i + 1) * ncols]))

    def tolist(self):
        labels = sorted(set().union(*self.store))
        outlist = []
        for obs in self.store:
            outlist.append([obs.get(i, np.nan) for i in labels])
        return labels, outlist

    def writecsv(self, writer, dir='.'):
        labels, outlist = self.tolist()
        if isinstance(writer, str):
            outfile = open(dir + '/' + writer, 'w')
            csvwriter = csv.writer(outfile)
            csvwriter.writerow(labels)
            csvwriter.writerows(outlist)
            outfile.close()
        else:
            csvwriter = writer
            csvwriter.writerow(labels)
            csvwriter.writerows(outlist)
