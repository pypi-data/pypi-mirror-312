from abc import ABC, abstractmethod
from typing import List

from super_scad.scad.Context import Context
from super_scad.type.Vector2 import Vector2

from super_scad_smooth_profile.SmoothProfile2D import SmoothProfile2D
from super_scad_smooth_profile.SmoothProfileParams import SmoothProfileParams


class SmoothProfile3D(SmoothProfile2D, ABC):
    """
    A 3D smooth profile is an abstract base class for 3D smooth profiles. A smooth profile is an object that creates
    smooth profile widgets given the parameters of a node and its two vertices.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def create_polygon(self, *, context: Context, params: SmoothProfileParams) -> List[Vector2]:
        """
        Returns the profile as a polygon.

        :param context: The build context.
        :param params: The parameters for the smooth profile widget.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
