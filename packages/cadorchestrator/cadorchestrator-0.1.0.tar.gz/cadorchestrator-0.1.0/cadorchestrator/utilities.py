"""
A module containting utilitiy functions
"""

import pathlib
from copy import copy, deepcopy
import os

import yaml


def clean_dict(data: dict) -> dict:
    """
    Clean the input dictionary (recursively). Removing any keys where the value is
    none, changing pathlib.Path to strings and converting tuples to strings.

    :param data: A single dictionary.
    :returns: The cleaned dictionary.
    """
    # iterate over entries
    keys_to_delete = []
    for key, value in data.items():
        # remove empty entries
        if value is None:
            keys_to_delete.append(key)
        else:
            data[key] = _clean_object(value)
    # delete empty entries
    for key in keys_to_delete:
        del data[key]
    return data


def _clean_object(obj: object) -> object:
    # clean up lists
    if isinstance(obj, list):
        return [_clean_object(x) for x in obj]
    # clean up dicts
    if isinstance(obj, dict):
        return clean_dict(obj)
    if isinstance(obj, tuple):
        # convert to string like "(1,2,3)"
        return str(obj)
    if isinstance(obj, pathlib.Path):
        # convert to string
        return str(obj)
    return obj


def get_nested_dict(dictionary, keylist, add_if_missing=False):
    """
    Return a dictionary deeply nested within another. It is returned in place for editing.
    Optionally an empty dictionary can be added if the key is missing.
    
    :param dictionary: The overall dictionary to look within
    :param dictionary: A list of keys to select the sub dictionary. For example, if
        `["a","b","c"]. This function returns `dictionary[a][b][c]`
    :param add_if_missing: If any key is missing, an empty dictionary is added for this key.
    :returns: The nested dictionary (returned in place, so editing will edit the original
    dictionary).
    """
    d = dictionary
    for key_name in keylist:
        if key_name not in d:
            if add_if_missing:
                d[key_name] = {}
            else:
                raise KeyError(f"Couldn't access {keylist} in dict {dictionary}. No key {key_name}")
        if not isinstance(d[key_name], dict):
            raise TypeError(f"Couldn't access {keylist} in dict {dictionary}. "
                            f"{key_name} has a non-dict value")
        d = d[key_name]
    return d

class Export:

    """
    This is a base class that should not be used directly. It is the parent for
    `cadorchestrator.components.GeneratedMechanicalComponent` and
    `cadorchestrator.components.Render`.
    """

    def __init__(
        self,
        key: str,
        name: str,
        description: str,
        output_files: list,
        source_files: list,
        parameters: dict,
        application: str
    ) -> None:
        """
        :param key: A unique id to identify this export.
        :param name: A human readable name to identify this export.
        :param name: A human readable description of this export.
        :param output_files: A list of filenames to be exported (this will be passed to
        the application).
        :param source_files: A list of filenames that define the source (also passed to
        application).
        :param parameters: A dictionary of parameters that to customise how the outputs
        are generated from the source files (also passed to application).
        :param application: The application. See
        [ExSource-Tools](https://gitlab.com/gitbuilding/exsource-tools) for supported
        applications.
        """
        self._key = key
        self._name = name
        self._description = description
        self._output_files = output_files
        self._source_files = source_files
        self._parameters = parameters
        self._application = application
        self._parameter_file = None

    def __eq__(self, other):
        if isinstance(other, str):
            return self.key==str
        if isinstance(other, Export):
            return self.as_exsource_dict == other.as_exsource_dict
        return NotImplemented

    @property
    def key(self):
        """Return the unique key identifying the component"""
        return self._key

    @property
    def name(self):
        """Return the human readable name of the component"""
        return self._name

    @property
    def description(self):
        """Return the description of the component"""
        return self._description

    @property
    def output_files(self):
        """Return a copy of the list of output CAD files that represent the component"""
        return copy(self._output_files)

    @property
    def source_files(self):
        """Return a copy of the list of the input CAD files that represent the component"""
        return copy(self._source_files)

    @property
    def parameters(self):
        """Return the parameters associated with generating this mechancial component"""
        if self._parameter_file:
            return {self._parameter_file[0]: self._parameter_file[1]}
        return deepcopy(self._parameters)

    @property
    def application(self):
        """Return the name of the application used to process the input CAD files"""
        return self._application

    @property
    def dependencies(self):
        """Return the list of dependent files, or None if none are set.
        Note this currently is not implemented except for in the child classes.
        """
        return None

    @property
    def as_exsource_dict(self):
        """Return this object as a dictionary of the part information for ExSource"""
        component_data = {
            "name": self.name,
            "description": self.description,
            "output-files": self.output_files,
            "source-files": self.source_files,
            "parameters": self.parameters,
            "application": self.application,
            "dependencies": self.dependencies
        }
        component_data = clean_dict(component_data)
        return {self.key: component_data}

    def set_parameter_file(self, file_id: str, filename: str):
        """
        Return all parameters to a parameter file rather than store directly in the
        ExSource definition.
        By default, parameters are directly entered into the exsource-def file and passed
        by ExSource to your designated CAD program, this function overrides this behaviour.
        This is useful for complex nested parameters that ExSource may not know how to pass
        correctly.
        
        Use this method to specify a YAML file to write the parameters to. ExSource will
        then pass this file (as `{file_id: filename}`) to your CAD program. You can use your
        CAD program to open the YAML file.

        :param file_id: The variable name to use when passing the filename to you can program.
        :param filename: The filename to save the parameters to.
        
        """
        self._parameter_file = (file_id, filename)

    def write_parameter_file(self, root_dir='.'):
        """
        Write parameter file to disk. You should not need to call this yourself. CadOrchestrator
        will call this during generation.
        """
        if not self._parameter_file:
            return
        filename = os.path.join(root_dir, self._parameter_file[1])
        with open(filename, "w", encoding="utf-8") as f:
            yaml.dump(clean_dict(self._parameters), f, sort_keys=False)

    def add_parameter(self, key, value, add_missing_keys=False):
        """
        Add a parameter to the parameter dictionary.

        :param key: The key in the dictionary you want to add to. To access nested 
        parameters, you can pass multiple keys all separated by `.`s. For example to
        add `key2` to `key1` if `key1` already exists and its value is a dictionary,
        set key to `"key1.key2"`
        :param value: The value to add to the key.
        :add_missing_key: Set to true to add any missing keys.
        """
        keys = key.split('.')
        if len(keys) == 1:
            d = self._parameters
        else:
            d = get_nested_dict(self._parameters, keys[:-1], add_missing_keys)
        d[keys[-1]] = value

    def append_to_parameter(self, key, value):
        """
        Append to a list parameter in the parameter dictionary.

        :param key: The key in the dictionary you want to add to, it should already exist
        and its type should be a list. To access nested parameters, you can pass multiple
        keys all separated by `.`s.
        :param value: The value to add to the list.
        """
        keys = key.split('.')
        if len(keys) == 1:
            d = self._parameters
        else:
            d = get_nested_dict(self._parameters, keys[:-1])


        if not isinstance(d[keys[-1]], list):
            raise TypeError(f"Could not append to {keys} in parameters. "
                            f"{keys[-1]} has a non-list value")
        d[keys[-1]].append(value)
