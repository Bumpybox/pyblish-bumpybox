# Maya

From Maya you can publish various output formats. To publish an output format, you'll need to setup the scene first. Different output formats has different workflows for setting up the scene:

Output Format | Section
--- | ---
Alembic | [Set](#set)
MayaAscii | [Set](#set)
MayaBinary | [Set](#set)
Movie | [Playblast](#playblast)
Image Sequence | [Renderlayer (legacy)](#renderlayer-legacy)


## Set

To publish any objects in the scene (DAG nodes), you first have to collect what you want to publish in a set. The name of the set will determine the name of the output.

Once you have collected some nodes in a set, you can publish and choose what output format you want published.

<iframe width="560" height="315" src="https://www.youtube.com/embed/F6_4sVSxHGg" frameborder="0" allowfullscreen></iframe>

Which output format you decide on, is stored in the scene so you don't have to setup the scene again. This data is stored as attributes on the set.

## Playblast

To publish a movie of the viewport, you'll need to have a non-default camera in the scene. The default cameras; ```persp```, ```front```, ```side``` and ```top```, will not be considered for publishing.

<iframe width="560" height="315" src="https://www.youtube.com/embed/uXaxpw9XuQU" frameborder="0" allowfullscreen></iframe>

## RenderLayer (Legacy)

To publish any renderlayer's output, you have to create a renderlayer. The default ```masterLayer``` will not be considered for publishing.

The renderable state of a renderlayer determines whether it gets published or not. The enabled/disabled state in the UI reflects into the scene, so you can save the scene and be sure its the same publish next time you open it.

Currently you can only render a single camera per renderlayer. You will be prompted to change this while publishing.

<iframe width="560" height="315" src="https://www.youtube.com/embed/lC0IJKjP3iw" frameborder="0" allowfullscreen></iframe>

## Remote Rendering/Processing

To send instances off to remote machines for processing like rendering on a farm or in the cloud, you'll need to setup the scene.

For renderlayers you add the renderlayer to a set starting with ```remote```.

<iframe width="560" height="315" src="https://www.youtube.com/embed/-_MbOSqJKMs" frameborder="0" allowfullscreen></iframe>

You can read more about the supported remote processing solutions [here](remote.md)

# [BACK](index.md)
