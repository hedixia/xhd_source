import re
import warnings


def get_start(full_str, char):
    assert type(char) == str
    assert len(char) == 1
    a = re.search('(?!{})'.format(char), full_str)
    return a.start()


class ArgumentParser:
    StoreMap = {'store_true': False, 'store_false': True}

    def __init__(self):
        self.argument_dict = dict()
        self.default_dict = dict()
        self.ref_link = dict()

    def _add_argument(self, s, val, default=False):
        self.argument_dict[s] = val
        if default:
            self.default_dict[s] = val

    def _ref_link(self, s1, s2):
        """
        Link alias of the same argument with different notation '--xxx' and '-x'
        :return:
        """
        if s2 is None:
            return

        # check
        assert get_start(s1, '-') == 1
        assert get_start(s2, '-') == 2

        self.ref_link[s1] = s2

    def add_argument(self, s, s2=None, *, type=None, default=None, action=None, **kwargs):
        if type is not None:
            if default is not None:
                default = type(default)
            val = (default, type)
        elif action in self.StoreMap:
            val = (self.StoreMap[action], None)
        else:
            raise NotImplementedError

        self._ref_link(s, s2)

        s = s if s2 is None else s2
        self._add_argument(s, val=val, default=True)

    def _pstr(self, s):
        """
        Get parsed string
        :param s: type string, '--xxx' or '-xxx'
        :return: type string 'xxx'
        """
        starting_underscore = get_start(s, '-')
        return s[starting_underscore:].replace('-', '_')

    def parse_args(self, s=""):
        s_list = s.split(' ')
        for i in range(len(s_list)):
            w = s_list[i]
            starting_underscore = get_start(w, '-')
            if starting_underscore == 0:
                continue
            elif starting_underscore == 1:
                if w in self.ref_link:
                    idx = self.ref_link[w]
                else:
                    idx = w
            elif starting_underscore == 2:
                idx = w
            else:
                raise ValueError('Invalid input argument {}'.format(w))

            if idx not in self.default_dict:
                # Check whether the next one in line exist and is a valid value
                next_valid = (len(s_list) > i + 1)
                if next_valid:
                    next_valid = (get_start(s_list[i + 1], '-') == 0)

                if next_valid:
                    # Argument passed, treated as type=str
                    self.argument_dict[idx] = (s_list[i + 1], str)
                else:
                    # No arguments passed, treated as store_true
                    self.argument_dict[idx] = (True, None)
                warnings.warn('Undocumented argument {} added with value {}'.format(idx, self.argument_dict[idx]))
            else:
                arg_type = self.default_dict[idx][-1]
                if arg_type is None:
                    # store_true / store_false mode
                    self.argument_dict[idx] = (not self.default_dict[idx][0], None)
                else:
                    val = s_list[i + 1]
                    assert get_start(val, '-') == 0
                    self.argument_dict[idx] = (arg_type(val), arg_type)

        for idx in self.argument_dict:
            setattr(self, self._pstr(idx), self.argument_dict[idx][0])

        return self


if __name__ == '__main__':
    arg_str = "python main.py --t 2.0 --a -n 30 --seed 0 -l 20 --xxx"
    parser = ArgumentParser()
    parser.add_argument('--t', type=float, default=1.0)
    parser.add_argument('--a', action='store_true')
    parser.add_argument('-l', type=float, default=1.0)
    parser.add_argument('-n', '--n-iters', type=int, default=50)
    parser.parse_args(arg_str)
    opt = vars(parser)

    print(">Options Available:")
    for key in opt:
        if key not in ['argument_dict', 'default_dict']:
            print('>>>', key, ':', opt[key])
