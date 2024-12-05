import FreeCAD
import Part as FCPart

from typing import List, Optional, Union

from .scene import ExtendedScene
from .three_views import display_vertices, display_edges, display_wire, display_face, display_solid
from nicegui.elements.scene_objects import Group


def display_feature(feature: FCPart.Feature,
                    scene: ExtendedScene
                    ) -> tuple[Group, tuple[float, float, float]]:

    x_height = feature.Shape.BoundBox.XMax
    y_height = feature.Shape.BoundBox.YMax
    z_height = feature.Shape.BoundBox.ZMax

    rgba_string = feature.ShapeMaterial.Properties['AmbientColor']
    rgba_values = rgba_string.strip('()').split(',')
    rgb = [int(float(value.strip()) * 255) for value in rgba_values[:3]]
    black_color = [255, 255, 255]

    with scene.group() as group:
        if hasattr(feature.Shape, 'Vertexes'):
            display_vertices(feature.Shape.Vertexes,
                             scene,
                             str(feature.ID),
                             colors=[black_color] * feature.Shape.Vertexes.__len__()
                             )

        if hasattr(feature.Shape, 'Edges'):
            display_edges(feature.Shape.Edges,
                          scene,
                          str(feature.ID),
                          black_color)

        if hasattr(feature.Shape, 'Wires'):
            for wire in feature.Shape.Wires:
                display_wire(wire,
                             scene,
                             str(feature.ID),
                             black_color)

        if hasattr(feature.Shape, 'Faces'):
            for face in feature.Shape.Faces:
                display_face(face, scene, str(feature.ID), rgb)

        if hasattr(feature.Shape, 'Solids'):
            for solid in feature.Shape.Solids:
                display_solid(solid, scene, str(feature.ID), rgb)

    scene.move_camera(x=x_height, y=-y_height, z=z_height * 2, duration=2)

    return group, (x_height, y_height, z_height)
