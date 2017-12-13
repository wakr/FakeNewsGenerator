"""Python wrapper for datamuse API.

Original module: https://github.com/margaret/python-datamuse

Changes done to make it useable in Python 3.x

Datamuse API: http://www.datamuse.com/api/

"""
import requests

# See Datamuse API for these
WORD_PARAMS = [
    'ml',
    'sl',
    'sp',
    'rel_jja',
    'rel_jjb',
    'rel_syn',
    'rel_ant',
    'rel_spc',
    'rel_gen',
    'rel_com',
    'rel_par',
    'rel_bga',
    'rel_bgb',
    'rel_rhy',
    'rel_nry',
    'rel_hom',
    'rel_cns',
    'v',
    'topics',
    'lc',
    'rc',
    'max'
]

# See Datamuse API for these
SUGGEST_PARAMS = [
    's',
    'max',
    'v'
]


class Datamuse():
    '''Wrapper for Datamuse API'''
    def __init__(self, max_results=100):
        self.api_root = 'https://api.datamuse.com'
        self._validate_max(max_results)
        self.max = max_results

    def __repr__(self):
        # See e.g. https://stackoverflow.com/a/2626364 and
        # https://stackoverflow.com/a/44595282
        return "{}({!r})".format(self.__class__.__name__, self.__dict__)

    def _validate_max(self, max_results):
        if not (0 < max_results <= 1000):
            raise ValueError("Datamuse only supports values of max in (0, 1000]")

    def _validate_args(self, args, param_set):
        for arg in args:
            if arg not in param_set:
                raise ValueError('{0} is not a valid parameter for this endpoint.'.format(arg))
            if arg == 'max':
                self._validate_max(args[arg])

    def _get_resource(self, endpoint, **kwargs):
        url = '/'.join([self.api_root, endpoint])
        response = requests.get(url, params=kwargs)
        data = response.json()

        return data

    def set_max_default(self, max_results):
        '''Set maximum number of results API calls should return'''
        self._validate_max(max_results)
        self.max = max_results

    def words(self, **kwargs):
        '''https://www.datamuse.com/api/
        '''
        self._validate_args(kwargs, WORD_PARAMS)
        if 'max' not in kwargs:
            kwargs.update({'max': self.max})

        return self._get_resource('words', **kwargs)

    def suggest(self, **kwargs):
        '''https://www.datamuse.com/api/
        '''
        self._validate_args(kwargs, SUGGEST_PARAMS)

        return self._get_resource('sug', **kwargs)
