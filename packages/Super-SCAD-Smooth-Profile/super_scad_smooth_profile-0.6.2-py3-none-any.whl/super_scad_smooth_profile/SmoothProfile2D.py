from abc import ABC, abstractmethod
from typing import Tuple

from super_scad.scad.ScadWidget import ScadWidget

from super_scad_smooth_profile.SmoothProfileParams import SmoothProfileParams


class SmoothProfile2D(ABC):
    """
    A 2D smooth profile is an abstract base class for 2D smooth profiles. A smooth profile is an object that creates
    smooth profile widgets given the parameters of a node and its two vertices.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def create_smooth_profiles(self, *, params: SmoothProfileParams) -> Tuple[ScadWidget | None, ScadWidget | None]:
        """
        Returns, optionally, two widgets. The first widget must be subtracted, and the second widget must be added to
        the widget at the position of the node where the smooth profile must be applied.

        :param params: The parameters for the smooth profile widget.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    @abstractmethod
    def is_external(self) -> bool:
        """
        Returns whether the profile is an external profile.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    @abstractmethod
    def is_internal(self) -> bool:
        """
        Returns whether the profile is an internal profile.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    @abstractmethod
    def convexity(self) -> int | None:
        """
        Return the convexity of the profile.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def offset1(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the first vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def offset2(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the second vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def side(self) -> int | None:
        """
        Returns the edge on which the exterior fillet must be applied. Returns None for non-exterior profiles.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
