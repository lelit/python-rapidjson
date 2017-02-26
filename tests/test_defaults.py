from contextlib import contextmanager

import pytest
import rapidjson


@contextmanager
def temp_defaults(**new_defaults):
    old_defaults = rapidjson.get_defaults()
    rapidjson.set_defaults(**new_defaults)
    yield
    rapidjson.set_defaults(**old_defaults)


@pytest.mark.unit
def test_invalid_get_defaults_params():
    with pytest.raises(TypeError):
        rapidjson.get_defaults(1)


@pytest.mark.unit
@pytest.mark.parametrize(
    'posargs,kwargs', (
        ( (1,), {} ),
        ( (), { 'this_keyword_arg_shall_never_exist': True } ),
        ( (), { 'object_hook': True } ),
        ( (), { 'datetime_mode': 'no' } ),
        ( (), { 'datetime_mode': -100 } ),
        ( (), { 'datetime_mode': 1000 } ),
        ( (), { 'datetime_mode':
                rapidjson.DATETIME_MODE_ISO8601+rapidjson.DATETIME_MODE_UNIX_TIME } ),
        ( (), { 'datetime_mode': rapidjson.DATETIME_MODE_UTC } ),
        ( (), { 'uuid_mode': 'no' } ),
        ( (), { 'uuid_mode': -100 } ),
        ( (), { 'uuid_mode': 100 } ),
        ( (), { 'number_mode': 'no' } ),
        ( (), { 'number_mode': -100 } ),
        ( (), { 'number_mode': 100 } ),
        ( (), { 'datetime_mode': rapidjson.DATETIME_MODE_ISO8601,
                'number_mode': 100 } ),
        ( (), { 'uuid_mode': rapidjson.UUID_MODE_HEX,
                'number_mode': 100 } ),
        ( (), { 'uuid_mode': 100,
                'number_mode': rapidjson.NUMBER_MODE_NATIVE } ),
        ( (), { "indent": -1 } ),
        ( (), { "default": True } ),
    ))
def test_invalid_set_defaults_params(posargs, kwargs):
    defaults = rapidjson.get_defaults()
    try:
        rapidjson.set_defaults(*posargs, **kwargs)
    except (TypeError, ValueError) as e:
        assert defaults == rapidjson.get_defaults()
    else:
        assert False, "Expected either a TypeError or a ValueError"


@pytest.mark.unit
def test_object_hook():
    class Foo:
        def __init__(self, foo):
            self.foo = foo

    def hook(d):
        if 'foo' in d:
            return Foo(d['foo'])

        return d

    assert rapidjson.loads('{"foo": 1}') == {"foo": 1}

    with temp_defaults(object_hook=hook):
        res = rapidjson.loads('{"foo": 1}')
        assert isinstance(res, Foo)
        assert res.foo == 1
        assert rapidjson.loads('{"foo": 1}', object_hook=None) == {"foo": 1}

    assert rapidjson.loads('{"foo": 1}') == {"foo": 1}

    # assert rapidjson.dumps(rapidjson.loads('{"foo": 1}', object_hook=hook),
    #         default=default) == '{"foo":1}'
    # res = rapidjson.loads(rapidjson.dumps(Foo(foo="bar"), default=default),
    #         object_hook=hook)
    # assert isinstance(res, Foo)
    # assert res.foo == "bar"
