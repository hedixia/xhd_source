class ParsedArgs:
    pass


class ArgumentParser:
    def __init__(self):
        self.argument_dict = dict()

    def add_argument(self, s, *, type=None, default=None, action=None, **kwargs):
        if type is not None:
            if default is not None:
                default = type(default)
            self.argument_dict[self._pstr(s)] = (default, type)
        elif action in ['store_true']:
            self.argument_dict[self._pstr(s)] = (False, type)

    def _pstr(self, s):
        return s[2:]

    def parse_args(self, s=""):
        pa = ParsedArgs()
        for key in self.argument_dict:
            setattr(pa, key, self.argument_dict[key][0])

        sl = [ss.split() for ss in s.split('--')]
        for ssl in sl:
            if len(ssl) == 0:
                continue
            elif len(ssl) == 1:
                setattr(pa, ssl[0], True)
            elif len(ssl) == 2:
                type = self.argument_dict[ssl[0]][1]
                setattr(pa, ssl[0], type(ssl[1]))

        return pa


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--t', type=float, default=1.0)
    parser.add_argument('--a', action='store_true')
    print(parser.__dict__)
    parser.parse_args("--t 2.0 --a")
    opt = vars(parser)
    print(opt)
