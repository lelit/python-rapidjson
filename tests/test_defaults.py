from contextlib import contextmanager

import pytest

import rapidjson as rj


@contextmanager
def temp_defaults(**new_defaults):
    old_defaults = rj.get_defaults()
    rj.set_defaults(**new_defaults)
    yield
    rj.set_defaults(**old_defaults)


@pytest.mark.unit
def test_invalid_get_defaults_params():
    with pytest.raises(TypeError):
        rj.get_defaults(1)


@pytest.mark.unit
@pytest.mark.parametrize(
    'posargs,kwargs', (
        ( (1,), {} ),
        ( (), { 'this_keyword_arg_shall_never_exist': True } ),
        ( (), { 'object_hook': True } ),
        ( (), { 'datetime_mode': 'no' } ),
        ( (), { 'datetime_mode': -100 } ),
        ( (), { 'datetime_mode': rj.DATETIME_MODE_UNIX_TIME + 1 } ),
        ( (), { 'datetime_mode': rj.DATETIME_MODE_SHIFT_TO_UTC } ),
        ( (), { 'uuid_mode': 'no' } ),
        ( (), { 'uuid_mode': -100 } ),
        ( (), { 'uuid_mode': 100 } ),
        ( (), { 'number_mode': 'no' } ),
        ( (), { 'number_mode': -100 } ),
        ( (), { 'number_mode': 100 } ),
        ( (), { 'datetime_mode': rj.DATETIME_MODE_ISO8601,
                'number_mode': 100 } ),
        ( (), { 'uuid_mode': rj.UUID_MODE_HEX,
                'number_mode': 100 } ),
        ( (), { 'uuid_mode': 100,
                'number_mode': rj.NUMBER_MODE_NATIVE } ),
        ( (), { "indent": -1 } ),
        ( (), { "default": True } ),
    ))
def test_invalid_set_defaults_params(posargs, kwargs):
    defaults = rj.get_defaults()
    try:
        rj.set_defaults(*posargs, **kwargs)
    except (TypeError, ValueError) as e:
        assert defaults == rj.get_defaults()
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

    assert rj.loads('{"foo": 1}') == {"foo": 1}

    with temp_defaults(object_hook=hook):
        res = rj.loads('{"foo": 1}')
        assert isinstance(res, Foo)
        assert res.foo == 1
        assert rj.loads('{"foo": 1}', object_hook=None) == {"foo": 1}

    assert rj.loads('{"foo": 1}') == {"foo": 1}


@pytest.mark.unit
def test_default():
    class Foo:
        def __init__(self, foo):
            self.foo = foo

    def default(o):
        if isinstance(o, Foo):
            return dict(foo=o.foo)

    foo = Foo('bar')

    with pytest.raises(TypeError):
        rj.dumps(foo)

    with temp_defaults(default=default):
        assert rj.dumps(foo) == rj.dumps(dict(foo='bar'))
        with pytest.raises(TypeError):
            rj.dumps(foo, default=None)
