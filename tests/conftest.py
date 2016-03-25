from collections import namedtuple
from functools import partial
from operator import attrgetter

Contender = namedtuple('Contender', 'name,dumps,loads')


# See https://github.com/ionelmc/pytest-benchmark/issues/48

def pytest_benchmark_group_stats(config, benchmarks, group_by):
    result = {}
    for bench in benchmarks:
        if config.option.compare_other_engines:
            engine, data_kind = bench.param.split('-')
            if engine.endswith('not precise'):
                group = result.setdefault("not precise floats: %s" % bench.group, [])
            else:
                group = result.setdefault("%s: %s" % (data_kind, bench.group), [])
        else:
            group = result.setdefault(bench.group, [])
        group.append(bench)
    return sorted(result.items())


def pytest_addoption(parser):
    parser.addoption('--compare-other-engines', action='store_true',
                     help='compare against other JSON engines')


contenders = []
inaccurate_floats_contenders = []

import rapidjson

contenders.append(Contender('rapidjson',
                            rapidjson.dumps,
                            partial(rapidjson.loads, precise_float=True)))

inaccurate_floats_contenders.append(Contender('rapidjson not precise',
                                              rapidjson.dumps,
                                              partial(rapidjson.loads,
                                                      precise_float=False)))

try:
    import yajl
except ImportError:
    pass
else:
    contenders.append(Contender('yajl',
                                yajl.Encoder().encode,
                                yajl.Decoder().decode))

try:
    import simplejson
except ImportError:
    pass
else:
    contenders.append(Contender('simplejson',
                                simplejson.dumps,
                                simplejson.loads))

try:
    import json
except ImportError:
    pass
else:
    contenders.append(Contender('stdlib json',
                                json.dumps,
                                json.loads))

try:
    import ujson
except ImportError:
    pass
else:
    contenders.append(Contender('ujson',
                                ujson.dumps,
                                partial(ujson.loads, precise_float=True)))
    inaccurate_floats_contenders.append(Contender('ujson not precise',
                                                  ujson.dumps,
                                                  partial(ujson.loads,
                                                          precise_float=False)))


def pytest_generate_tests(metafunc):
    if 'contender' in metafunc.fixturenames:
        if metafunc.config.option.compare_other_engines:
            metafunc.parametrize('contender', contenders, ids=attrgetter('name'))
        else:
            metafunc.parametrize('contender', contenders[:1], ids=attrgetter('name'))

    if 'inaccurate_floats_contender' in metafunc.fixturenames:
        if metafunc.config.option.compare_other_engines:
            metafunc.parametrize('inaccurate_floats_contender',
                                 inaccurate_floats_contenders,
                                 ids=attrgetter('name'))
        else:
            metafunc.parametrize('inaccurate_floats_contender',
                                 inaccurate_floats_contenders[:1],
                                 ids=attrgetter('name'))
