"""
This components module contains classes for holding the information individual components.

`MechanicalComponent` is a base class and can also be used for generic components
    that have no source code
`GeneratedMechanicalComponent` is a child class of `MechanicalComponent`, it contains
    all the information for ExSource to generate the CAD models for this component
`Assembly` is a child class of `GeneratedMechanicalComponent` it holds groups of
    sub-components
`AssembledComponent` is a class that holds any assembly information for a given
   `MechanicalComponent`
"""
from __future__ import annotations
from copy import copy, deepcopy
from typing import Any


from cadorchestrator.utilities import Export

#pylint: disable=fixme



class MechanicalComponent:
    """
    This is a generic class for any mechanical component. If it is a generic
    component rather than a generated one then use this class, for generated
    components use the child-class `GeneratedMechanicalComponent`
    """

    _documentation_md = None
    _documentation_filename = None
    _renders = None

    def __init__(self, key: str, name: str, description:str, output_files: list) -> None:
        """
        :param key: A unique id to identify this component
        :param name: A human readable name to identify this component
        :param name: A human readable description of this component
        :param output_files: A list of any STEP/STL/GLB files for this object. They are called
        "output" as they should be similar to the files output by your own generated
        components
        """
        self._key = key
        self._name = name
        self._description = description
        self._output_files = output_files
        self._init_extra_params()

    def _init_extra_params(self):
        # These are done in a seperate function so it can be called by
        # GeneratedMechanicalComponent without running full init.
        self._documentation_md = None
        self._documentation_filename = None
        self._renders = []

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
    def renders(self):
        """Return a copy of the list all the renders."""
        return copy(self._renders)

    @property
    def step_representation(self):
        """
        Return the path to the STEP file that represents this part. Return None
        if not defined
        """
        for output_file in self.output_files:
            if output_file.lower().endswith(('stp','step')):
                return output_file
        return None

    @property
    def stl_representation(self):
        """
        Return the path to the STL file that represents this part. Return None
        if not defined.
        """
        for output_file in self.output_files:
            if output_file.lower().endswith('stl'):
                return output_file
        return None

    def add_render(self, render):
        """
        Add a render for this component.

        :param render: a `Render` object with the parameters needed to create the render.
        """
        if isinstance(render, Render):
            self._renders.append(render)
            return
        raise TypeError("Expecting render to be of class Render")

    def set_documentation(self, md: str):
        """
        Add a documentation for this component. If the filename is not set with
        `set_documentation_filename` then the output filename will be this component's key
        followred by `.md`

        :param md: The GitBuilding markdown (BuildUp) for making this component.
        """
        self._documentation_md = md

    @property
    def documentation(self):
        """
        Return the documentation for this component. This will be None
        if the documentation is not set.
        """
        return self._documentation_md

    def set_documentation_filename(self, filename: str):
        """
        Override the default filename for the documentation.
        The filename should be the filename relative to the root documentation
        directory. If not set, the default filename is the component key
        followed by `.md`.

        :param filename: The filename to use instead of default.
        """
        if filename.endswith('.md'):
            self._documentation_filename = filename
        else:
            raise ValueError('Documentation filename should end with `.md`')

    @property
    def documentation_filename(self):
        """
        Return the documentation file name
        """
        if self._documentation_filename:
            return self._documentation_filename
        return self.key+'.md'

class GeneratedMechanicalComponent(Export, MechanicalComponent):

    """
    This is a class for a mechanical component that needs to be generated from
    source files. All methods for this class are inherited from
    `cadorchestrator.utilities.Export` and `MechanicalComponent`
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
        See `cadorchestrator.utilities.Export` for initialisation parameter
        descriptions.
        """
        super().__init__(key,
                         name,
                         description,
                         output_files,
                         source_files,
                         parameters,
                         application)
        # Initialise these manually rather than call MechanicalComponent.
        # Init as this will try to initialise key, name, etc again.
        self._init_extra_params()


class Assembly(GeneratedMechanicalComponent):
    """
    This class represents an assembly of other components. It is a child class of
    `GeneratedMechanicalComponent`.

    This object also:
    * Can have components added to it (As `AssembledComponent`s)
    * Automatically adds these components to its dependencies so they are generated first
    * Automatically generates an extra key in its parameter dictionary. This key is a list of
    the components data. Note! This is the `data` stored in the the `AssembledComponent` object,
    not the parameters passed to the underlying `GeneratedMechanicalComponent`.
    """

    _assembled_components: list

    def __init__(
        self,
        key: str,
        name: str,
        description: str,
        output_files: list,
        source_files: list,
        parameters: dict,
        application: str,
        component_data_parameter:str = 'components'
    ) -> None:
        """
        See `cadorchestrator.utilities.Export` for inherited initialisation
        parameter descriptions. Non-inherited parameters:

        :param component_data_parameter: The parameters for the assembly will be
        the input parameters above plus another key, with a list of component data.
        You can use this parameter to override this component data key.
        """
        super().__init__(
            key=key,
            name=name,
            description=description,
            output_files=output_files,
            source_files=source_files,
            parameters=parameters,
            application=application
        )
        self._component_data_parameter = component_data_parameter
        self.add_parameter(component_data_parameter, [], add_missing_keys=True)
        self._assembled_components = []

    def add_component(self, component: AssembledComponent):
        """
        Add a component to this assembly.
        
        :param component: The component to add to the assembly. This must be an
        `AssembledComponent`. This is a wrapper around a component that
        can be a `MechanicalComponent`, or sub-classes of this such as
        `GeneratedMechanicalComponent` or another Assembly.

        To notify the source file about this component and extra information on how to
        add this component to the assembly, you should either set `data` for the
        `AssembledComponent`, or this can be provided by amending this assembly's
        parameters using the `add_parameter` or `append_to_parameter` methods.
        """
        self._assembled_components.append(component)
        if component.assembly_parameters:
            self.append_to_parameter(
                self._component_data_parameter,
                component.assembly_parameters
            )

    @property
    def dependencies(self):
        """
        Return the dependencies for this assembly. This is autogenerated
        currently and no options exist for modifying this.
        """
        deps = []
        if self._parameter_file:
            deps.append(self._parameter_file[1])
        for component in self.components:
            if not isinstance(component, GeneratedMechanicalComponent):
                # Only add dependencies for generated components
                continue
            if component.step_representation:
                deps.append(component.step_representation)
            if component.stl_representation:
                deps.append(component.stl_representation)
        return deps

    @property
    def all_components_and_assemblies(self):
        """
        Return a list of all sub-assemblies and components. This is a de-duplicated
        list, so if the same component is used multiple times it will only be returned
        once. To get each instance see the `assembled_components` property.
        """
        components = []
        components.append(self)
        #Loop first over direct components (these have already been deduplicated)
        for component in self.components:
            if isinstance(component, Assembly):
                for sub_component in component.all_components_and_assemblies:
                    #Before adding sub component, check it is not already a component
                    if sub_component not in components:
                        components.append(sub_component)
            else:
                components.append(component)
        return components

    @property
    def components(self):
        """
        Return a list of the components directly added to this assembly.
        There is only one per each type of component, to see all copies
        of identical components for the assembly see
        `assembled_components()`

        Each object in the list is an instance of MechanicalComponent
        """

        components = []
        for assembled_component in self._assembled_components:
            component = assembled_component.component
            if component not in components:
                components.append(component)
        return components

    @property
    def assembled_components(self):
        """
        Return a list of the components assembled in this system.

        Each object in the list is an instance of AssembledComponent, giving information
        such as the position and the assembly step. To just see the list of component types
        see `components()`
        """
        return deepcopy(self._assembled_components)


class AssembledComponent:
    """
    A class for an assembled component. This includes a key (unique name), its data,
    and the component to be assembled.
    """

    def __init__(self,
                 key: str,
                 component: MechanicalComponent,
                 data: Any = None,
                 include_key: bool = False,
                 include_stepfile: bool = False,
                 include_stlfile: bool = False):
        """
        :param key: A unique id to identify this component in the assembly.
        :param component: The underlying component to be added into the assembly.
        :param data: Data about the assembly to be added to the `Assembly` object in its
        component data list. Note:
          * If no data is added, no entry will be added to the list.
          * Any type of data can be added. However, this needs to be able to be passed by
          ExSource to your CAD either directly or via a YAML parameter file.
          * You should pass all data that your CAD assembly needs to add this component,
          no other data about it will be sent. One way to do this is to create a dictionary
          for this data and use the include parameters that follow. If this is left blank
          you can still use the include options below.
        :param include_key: Optional, Boolean (default False). Include the key `key` into this
        component's data (data must be a dictionary or not set), the value will be this object's
        `key` as set above.
        :param include_stepfile: Optional, Boolean (default False). Include the key `step-file`
        into this component's data (data must be a dictionary or not set), the value will be
        the STEP file set for the underlying component.
        :param include_stlfile: Optional, Boolean (default False). Include the key `stl-file`
        into this component's data (data must be a dictionary or not set), the value will be
        the STL file set for the underlying component.
        """
        self._key = key
        self._component = component
        self._data = deepcopy(data)
        self._include_key = include_key
        self._include_stepfile = include_stepfile
        self._include_stlfile = include_stlfile

    @property
    def name(self):
        """
        Return the name of the assembled component. This is the same name as the
        component that is to be assembled.
        """
        return self._component.name

    @property
    def key(self):
        """
        A unique key to identify the assembled component.
        """
        return self._key

    @property
    def component(self):
        """
        Return the Object describing the component that is being assembled
        This is either a MechanicalComponent object or a child object such as
        GeneratedMechanicalComponent.
        """
        return self._component

    @property
    def data(self):
        """
        Return the input assembly data for this component. To see the full assembly
        parameters that will be passed to any `Assembly` see the `assembly_parameters` method,
        this has extra keys defined by the include options set at initialisation.
        """
        return deepcopy(self._data)

    @property
    def assembly_parameters(self):
        """
        Return the assembly parameters for this component as they will be added to the
        `Assembly` object's component data parameter.
        """
        if not isinstance(self.data, dict):
            if self._include_key or self._include_stepfile or self._include_stlfile:
                print(f"For component {self._key}, extra data cannot be included."
                      "As the data is not a dictionary.")
            return self.data

        par_dict = self.data
        if self._include_key:
            par_dict['key'] = self.key
        if self._include_stepfile:
            par_dict['step-file'] = self._component.step_representation
        if self._include_stlfile:
            par_dict['stl-file'] = self._component.stl_representation
        return par_dict

class Render(Export):
    """
    A class to handle rendering via an ExSource export. All methods for this class are
    inherited from `cadorchestrator.utilities.Export`.
    """
