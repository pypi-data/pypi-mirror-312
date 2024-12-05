"""
CadOrchestrator is a new Python framework for creating consistent production files,
assembly documentation, and assembly images for modular hardware projects.

Once your project is configured in CadOrchestrator you will be able to generate documentation
and production files for a specific configuration from your terminal, or to launch a webapp
with an interactive interface for configuration.

CadOrchestrator uses a number of other tools such as [GitBuilding](https://gitbuilding.io)
for documentation, and [ExSource](https://gitlab.com/gitbuilding/exsource-tools) for running
CAD file generation. It supports CAD files generated in OpenSCAD, CadQuery and FreeCAD.

Currently the framework is in an experimental stage. If your CAD models do not build please
open an issue either in this project or in
[ExSource Tools](https://gitlab.com/gitbuilding/exsource-tools).


## Installation

To install you will need Python 3.10 or newer, as well as pip. From your terminal run:

    pip install cadorchestrator


## Running the example

To run the example you should start by cloning a copy of
[the example project](https://gitlab.com/gitbuilding/CadOrchestrator-Example). Note
that you will also need to install [OpenSCAD](https://openscad.org/), to run this example.

You should now be able to run

```
cadorchestrator serve
```

from your terminal (from the base of the project). This should start serving a web application.
In your browser navigate to

`http://127.0.0.1:8000/`

From here you should be able to customise the example project (a little cup stand), and generate
documentation and models to build your own.

If you are interested in the web API for this web app, the API docs can be
located at:

`http://127.0.0.1:8000/docs`


## Getting started with your own configuration

For this we also recommend cloning a copy of
[the example project](https://gitlab.com/gitbuilding/CadOrchestrator-Example).

There are three main files to consider when doing so.

* `cadorchestration.yml` - This is your main configuration file. It points to
the Python module you will use for configuration, and points to the file that sets
your configuration options. For more detail see `cadorchestrator.settings`
* `OrchestratorConfigOptions.json` - This holds the configuration options that will
be displayed in the web interface, and will be passed through to your configuration
function. Please see our schema [documentation](./schema_doc.html) for more information.
You can rename this file if you modify `cadorchestration.yml`.
* `configure.py` - This holds the configuration function. A configuration is passed
to this function as a Python dictionary, and a `cadorchestrator.components.Assembly`
object is returned. You can rename this file if you modify the
`configuration-function -> module` option in `cadorchestration.yml`

For more information on writing your assembly code see `cadorchestrator.components`.


## Understanding the Assembly object that describes your project.

Let's take the example of a simple container made in OpenSCAD. You have three files inside
a directory named `openscad`:

* `container_base.scad` - This contains the OpenSCAD code for the base of the container.
* `container_lid.scad` - This contains the OpenSCAD code for the lid.
* `assembly.scad` - This creates an OpenSCAD model of the assembled container.
This can be used to send a complete model for display, or to create renders of assembly.

***Note:*** *CadOrchestrator is a configuration tool for generating customised models
and documentation. It does not provide any extra tools for creating assemblies, or renders
of these assemblies. To do this you must use tools provided by the CAD package you have
chosen.*

To start we make a configuration script in our repository, `configuration.py`,
with the function `main(config)`. We make sure that our `cadorchestration.yml`
points to this.

### Creating Components

Within `configuration.py` we import some classes that we will need:

```python
from cadorchestrator.components import (GeneratedMechanicalComponent,
                                        AssembledComponent,
                                        Assembly,
                                        Render)
```

Now to start configuring. Within the configuration function we need to create
the components within our project. Starting with the base:

```python
base = GeneratedMechanicalComponent(
    key="base",
    name="Container Base",
    description="The base of the container",
    output_files=["./container_base.stl"],
    source_files=["../openscad/container_base.scad.scad"],
    parameters={"WIDTH": config.['width']},
    application="openscad"
)
```

Taking this line-by-line:

* `base = GeneratedMechanicalComponent(` -
`cadorchestrator.components.GeneratedMechanicalComponent` is the base class
for any component that is generated. Note that there is an even more basic `MechanicalComponent`
class you can use to track standard items such as screws, motors, etc, if your project has them.
We are not using any `MechanicalComponent` objects in this example.
* `key="base",` - here we are setting a unique identifier for this specific component.
* `name="Container Base",` - A human readable name for the component.
* `description="The base of the container",` - A human readable description for the component.
* `output_files=["./container_base.stl"],` - The resulting file we want to create (this always
needs to be a list).
* `source_files=["../openscad/container_base.scad"],` - The source file we want to generate from
(also a list). **Note**. That is the source relative to the build directory. The build directory
will be created within your project root folder.
* `parameters={"WIDTH": config['width']},` - Any parameters to be passed to your CAD package to
 customise the component. In this case we are assuming that your configuration as defined in the
`OrchestratorConfigOptions.json` file sets the parameter "width".
* `application="openscad"` - Here we tell it we want to use OpenSCAD to generate the output files
from the source.

We can create something similar for the lid:

```python
lid = GeneratedMechanicalComponent(
    key="lid",
    name="Container Lid",
    description="The lid of the container",
    output_files=["./container_lid.stl"],
    source_files=["../openscad/container_lid.scad"],
    parameters={"WIDTH": config.['width']},
    application="openscad"
)
```

### Creating AssembledComponents

Before a Component can be added to an `Assembly`, we need to make another object we call
an AssembledComponent (cadorchestrator.components.AssembledComponent).

For the base this would look like:
```python
assm_base = AssembledComponent(
    key="base",
    component=base
)
assm_lid = AssembledComponent(
    key="lid",
    component=lid
)
```

***What is the point of this!?***

The purpose of assembled components is to make a distinction between the identical components that
are in your project. In this case we only have one of each of our components, but take the case
where our container had two identical drawers. We would make one single
`GeneratedMechanicalComponent` that describes the physical drawer model that we need to print,
and then create two `AssembledComponent` objects with keys `top_drawer` and `bottom_drawer`.

You can also add arbitrary data to each AssembledComponent. This would allow you to specify
information such as the location of the component.

***My project is very simple, do I need to do this!?***

Unfortunately this is necessary due to how CadOrchestrator works. CadOrchestrator is designed to
help those with very complex modular/customisable projects create consistent documentation.
It may be overkill to use on more simple projects.

### Creating an Assembly

Finally we can now make our `cadorchestrator.components.Assembly` object to return.
```python
main_assembly = Assembly(
    key='container',
    name='Container',
    description='A simple little container',
    output_files=["./assembly.glb"],
    source_files=["../openscad/assembly.scad"],
    application="scad2gltf",
)
main_assembly.add_component(assm_base)
main_assembly.add_component(assm_lid)
```

You will notice that `Assembly` has essentially the same inputs as `GeneratedMechanicalComponent`.
This is because it is a child of the same class. This allows more complex projects to make an 
`Assembly` object for each sub assembly, and then create a top level `Assembly` to return.

Note that the top level assembly should return a `.glb` file. This is because we are currently
using the Google model viewer which only accepts `.glb` files. In the case of OpenSCAD we use
scad2gltf, as a custom program that converts OpenSCAD to a `.glb` (.glb is a binary glTF).

We add our components to the `Assembly` with the `add_component()` method. Our configuration
function can then return the `Assembly` object.

For more complex projects we would need to add a parameters dictionary to the `Assembly` object,
and `data` to the `AssembledComponent` objects. See the documentation for these classes for more
details.

### Adding some renders

Your custom documentation will not really be useful unless readers have images that relate to their
projects.

We can use `assembly.scad` to create an image of the final component
```python
main_render = Render(
    key='full_render',
    name='Complete render',
    description='Complete render of the container',
    output_files=["./tree.png"],
    source_files=["../openscad/assembly.scad"],
    application="openscad",
)
main_assembly.add_render(main_render)
```

Again the same set of parameters are passed into `Render`. In this case we are using OpenSCAD
to create a PNG file. To create step by step images we recommend using parameters in OpenSCAD
(or another CAD program) to explode the model. You can then pass these in with the `parameters`
keyword argument, as we did with the `GeneratedMechanicalComponent`.

### Adding some documentation

For documentation we use [GitBuilding](https://gitbuilding.io).

First we create all the static pages that will not change and we place them in a directory
called `documentation`. In the case of this very simple example, we want the models to change
but not the documentation (as the size of the components does not change how it is assembled).

In some cases, we may need to write custom documentation depending on the parameters. For example, if the
configuration options were used to switch out components, we would need to write a Python
function that creates the correct markdown for the documentation file we need. Let's assume
this function was called `generate_assembly_md(config)`. We would then need to run:

```python
main_assembly.set_documentation(generate_assembly_md(config))
main_assembly.set_documentation_filename('assembly.md')
```

If we did not run `set_documentation_filename` the documentation file name will be set by the key.
So for `main_assembly` it would be`container.md` as `container` is the key.

Any `Assembly` or `GeneratedMechanicalComponent` object can have documentation set.


### Running your project

Once you have written your configuration function you can test it either by running

```
cadorchestrator serve
```
and interacting with the web application, or by passing your configuration as JSON into the
`generate` command line option:

```
cadorchestrator generate '{"width": 45}'
```

### Understanding what CadOrchestrator does.

1. CadOrchestrator will first pass the configuration you have chosen into your configuration
function.
1. Your configuration function returns the top level Assembly object.
1. CadOrchestrator will next generate a list of output files it needs to make. These are the
output files defined when initialising the top-level `Assembly`, and any other `Assembly`
or `GeneratedMechanicalComponents` objects that are included via `add_component`.
It will also add any renders to this list.
1. This list of files to generate (and the information on how to generate them) will be
converted into an `exsource-def.yml` file, in the directory `build`. This is then run by
[ExSource](https://gitlab.com/gitbuilding/exsource-tools) to create all of the output CAD
files and images.
1. Next your `documentation` directory is copied into a directory called `_gb_temp_`.
1. Any documentation set on the Assembly (or any included components/sub-assemblies) will be
added to the `_gb_temp_` directory.
1. GitBuilding is then run on the `_gb_temp_` directory. All final documentation is written
into `build/assembly-docs/`.
1. Finally, if this was called from the web app, a copy of this documentation directory will
be moved to `_cache_`. The name will be `$HASH$_assembly_docs` where `$HASH` is the result
of sha1 hashing the input configuration.

"""
