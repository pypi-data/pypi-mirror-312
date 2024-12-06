from typing import List, Tuple

from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type.Vector2 import Vector2

from super_scad_smooth_profile.SmoothProfile3D import SmoothProfile3D
from super_scad_smooth_profile.SmoothProfileParams import SmoothProfileParams


class Rough(SmoothProfile3D):
    """
    A profile that produces rough smoothing profile widgets.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def create_smooth_profiles(self, *, params: SmoothProfileParams) -> Tuple[ScadWidget | None, ScadWidget | None]:
        """
        Returns a smooth profile widget.

        :param params: The parameters for the smooth profile widget.
        """
        return None, None

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def is_external(self) -> bool:
        """
        Returns whether the fillet is an external fillet.
        """
        return False

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def is_internal(self) -> bool:
        """
        Returns whether the fillet is an internal fillet.
        """
        return False

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def side(self) -> int | None:
        """
        Returns None.
        """
        return None

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int | None:
        """
        Return the convexity of the profile.
        """
        return None

    # ------------------------------------------------------------------------------------------------------------------
    def offset1(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the first vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        return 0.0

    # ------------------------------------------------------------------------------------------------------------------
    def offset2(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the second vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        return 0.0

    # ------------------------------------------------------------------------------------------------------------------
    def create_polygon(self, *, context: Context, params: SmoothProfileParams) -> List[Vector2]:
        """
        Returns the profile as a polygon.

        :param context: The build context.
        :param params: The parameters for the smooth profile widget.
        """
        return [params.position]

# ----------------------------------------------------------------------------------------------------------------------
