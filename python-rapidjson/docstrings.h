#ifndef DOCSTRINGS_H_
#define DOCSTRINGS_H_

PyDoc_STRVAR(rapidjson_module_docstring,
             "Fast, simple JSON encoder and decoder. Based on RapidJSON C++ library.");

PyDoc_STRVAR(rapidjson_loads_docstring,
             "loads(s, object_hook=DEF, use_decimal=DEF, allow_nan=DEF,"
             " datetime_mode=DEF, uuid_mode=DEF, number_mode=DEF)\n"
             "\n"
             "Decodes a JSON string into Python object.");

PyDoc_STRVAR(rapidjson_dumps_docstring,
             "dumps(obj, skipkeys=DEF, ensure_ascii=DEF, allow_nan=DEF,"
             " indent=DEF, default=DEF, sort_keys=DEF,"
             " use_decimal=DEF, max_recursion_depth=2048,"
             " datetime_mode=DEF, uuid_mode=DEF, number_mode=DEF)\n"
             "\n"
             "Encodes Python object into a JSON string.");

PyDoc_STRVAR(rapidjson_get_defaults_docstring,
             "get_defaults()\n"
             "\n"
             "Returns a dictionary containing default settings.");

PyDoc_STRVAR(rapidjson_set_defaults_docstring,
             "set_defaults(*, object_hook=DEF, use_decimal=DEF, allow_nan=DEF,"
             " datetime_mode=DEF, uuid_mode=DEF, number_mode=DEF, skipkeys=DEF,"
             " ensure_ascii=DEF, sort_keys=DEF, indent=DEF, default=DEF)\n"
             "\n"
             "Changes default settings.");

#endif
