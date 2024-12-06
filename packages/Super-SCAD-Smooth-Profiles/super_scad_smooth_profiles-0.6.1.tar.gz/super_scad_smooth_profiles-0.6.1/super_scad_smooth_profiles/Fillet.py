import math
from typing import List, Tuple

from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2
from super_scad.type.Angle import Angle
from super_scad.util.Radius2Sides4n import Radius2Sides4n
from super_scad_smooth_profile.SmoothProfile3D import SmoothProfile3D
from super_scad_smooth_profile.SmoothProfileParams import SmoothProfileParams

from super_scad_smooth_profiles.ExteriorFilletWidget import ExteriorFilletWidget
from super_scad_smooth_profiles.InteriorFilletWidget import InteriorFilletWidget


class Fillet(SmoothProfile3D):
    """
    A profile that produces fillet smoothing profile widgets.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, radius: float, side: int | None = None):
        """
        Object constructor.

        :param radius: The radius of the fillet.
        :param side: The edge on which the exterior fillet must be applied.
        """

        self._radius: float = radius
        """
        The radius of the fillet.
        """

        self._side: int | None = side
        """
        The edge on which the exterior fillet must be applied. 
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def is_external(self) -> bool:
        """
        Returns whether the fillet is an external fillet.
        """
        return self._side is not None

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def is_internal(self) -> bool:
        """
        Returns whether the fillet is an internal fillet.
        """
        return self._side is None

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def side(self) -> int | None:
        """
        Returns the edge on which the exterior fillet must be applied.
        """
        return self._side

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int | None:
        """
        Return the convexity of the profile.
        """
        return 2

    # ------------------------------------------------------------------------------------------------------------------
    def offset1(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the first vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        if self._side is None:
            if self._radius > 0.0 and inner_angle < 180.0:
                # The corner is convex.
                alpha = math.radians(inner_angle) / 2.0

                return self._radius * math.cos(alpha) / math.sin(alpha)

            if self._radius > 0.0 and inner_angle > 180.0:
                # The corner is concave.
                alpha = math.radians(360.0 - inner_angle) / 2.0

                return self._radius * math.cos(alpha) / math.sin(alpha)

            if self._radius < 0.0:
                # Negative radius.
                return -self._radius

            return 0.0

        if self._side == 1:
            # The corner is convex.
            if self._radius > 0.0 and inner_angle < 180.0:
                # The corner is convex.
                alpha = math.radians(inner_angle) / 2.0

                return self._radius * math.cos(alpha) / math.sin(alpha)

            if self._radius > 0.0 and inner_angle > 180.0:
                # The corner is concave.
                print('Warning: Not possible to apply an exterior fillet on a concave corner.')

                return 0.0

            if self._radius < 0.0:
                # Negative radius.
                return -self._radius

            return 0.0

        if self._side == 2:
            return 0.0

        raise ValueError(f'Side must be 1 or 2, got {self._side}.')

    # ------------------------------------------------------------------------------------------------------------------
    def offset2(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the second vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        if self._side is None:
            if self._radius > 0.0 and inner_angle < 180.0:
                # The corner is convex.
                alpha = math.radians(inner_angle) / 2.0

                return self._radius * math.cos(alpha) / math.sin(alpha)

            if self._radius > 0.0 and inner_angle > 180.0:
                # The corner is concave.
                alpha = math.radians(360.0 - inner_angle) / 2.0

                return self._radius * math.cos(alpha) / math.sin(alpha)

            if self._radius < 0.0:
                # Negative radius.
                return -self._radius

            return 0.0

        if self._side == 2:
            if self._radius > 0.0 and inner_angle < 180.0:
                # The corner is convex.
                alpha = math.radians(inner_angle) / 2.0

                return self._radius * math.cos(alpha) / math.sin(alpha)

            if self._radius > 0.0 and inner_angle > 180.0:
                # The corner is concave.
                print('Warning: Not possible to apply an exterior fillet on a concave corner.')

                return 0.0

            if self._radius < 0.0:
                # Negative radius.
                return -self._radius

            return 0.0

        if self._side == 1:
            return 0.0

        raise ValueError(f'Side must be 1 or 2, got {self._side}.')

    # ------------------------------------------------------------------------------------------------------------------
    def create_smooth_profiles(self, *, params: SmoothProfileParams) -> Tuple[ScadWidget | None, ScadWidget | None]:
        """
        Creates widget for creating fillet on an edge.

        :param params: The parameters for the smooth profile widget.
        """
        if self._radius == 0.0 or self._radius > 0.0 and params.inner_angle == 180.0:
            negative, positive = None, None

        elif self._side is None:
            # Interior profile between both edges.
            widget = InteriorFilletWidget(radius=self._radius,
                                          inner_angle=params.inner_angle,
                                          normal_angle=params.normal_angle,
                                          position=params.position)

            if params.inner_angle < 180.0:
                # Convex corner.
                if self._radius > 0.0:
                    negative, positive = widget, None
                else:
                    negative, positive = None, widget
            else:
                # Concave corner.
                negative, positive = None, widget

        else:
            # Exterior profile on one edge.
            widget = ExteriorFilletWidget(radius=self._radius,
                                          side=self._side,
                                          inner_angle=params.inner_angle,
                                          normal_angle=params.normal_angle,
                                          position=params.position,
                                          edge1_is_extended_by_eps=params.edge1_is_extended_by_eps,
                                          edge2_is_extended_by_eps=params.edge2_is_extended_by_eps)

            negative, positive = None, widget

        return negative, positive

    # ------------------------------------------------------------------------------------------------------------------
    def create_polygon(self, *, context: Context, params: SmoothProfileParams) -> List[Vector2]:
        """
        Returns the profile as a polygon.

        :param context: The build context.
        :param params: The parameters for the smooth profile widget.
        """
        if self._radius == 0.0 or self._radius > 0.0 and params.inner_angle == 180.0:
            return [params.position]

        if params.inner_angle < 180.0:
            if self._side is None:
                return self._create_polygon(context, params.inner_angle, params.normal_angle, params.position)

            if self._side == 1:
                return self._create_polygon(context,
                                            180.0 - params.inner_angle,
                                            params.normal_angle - 90.0,
                                            params.position)

            if self._side == 2:
                return self._create_polygon(context,
                                            180.0 - params.inner_angle,
                                            params.normal_angle + 90.0,
                                            params.position)

        if params.inner_angle > 180.0:
            return list(reversed(self._create_polygon(context,
                                                      360.0 - params.inner_angle,
                                                      params.normal_angle - 180.0,
                                                      params.position)))

    # ------------------------------------------------------------------------------------------------------------------
    def _create_polygon(self,
                        context: Context,
                        inner_angle: float,
                        normal_angle: float,
                        position: Vector2) -> List[Vector2]:
        """
        Returns the profile as a polygon.

        :param context: The build context.
        :param inner_angle: The inner angle of the node.
        :param normal_angle: The normal angle of the node.
        :param position: The position of the node.
        """
        nodes = []

        inner_angle = Angle.normalize(inner_angle)
        normal_angle = Angle.normalize(normal_angle)
        rotation = Angle.normalize(180.0 - inner_angle)

        # Carefully align nodes with fn4n=True in InteriorFilletWidget._build_fillet_pos()
        fn = math.floor(Radius2Sides4n.r2sides4n(context, self._radius))
        steps = int(fn * rotation / 360.0)
        step_angle = 360.0 / fn

        alpha = math.radians(0.5 * inner_angle)
        center = position + Vector2.from_polar_coordinates(self._radius / math.sin(alpha), normal_angle)

        nodes.append(center + Vector2.from_polar_coordinates(-self._radius, normal_angle + 0.5 * rotation))
        if steps % 2 == 0:
            angle = normal_angle - 180.0 + 0.5 * steps * step_angle
            n = steps + 1
        else:
            angle = normal_angle - 180.0 + 0.5 * (steps - 1) * step_angle
            n = steps
        for i in range(n):
            nodes.append(center + Vector2.from_polar_coordinates(self._radius, angle))
            angle -= step_angle
        nodes.append(center + Vector2.from_polar_coordinates(-self._radius, normal_angle - 0.5 * rotation))

        return nodes

# ----------------------------------------------------------------------------------------------------------------------
