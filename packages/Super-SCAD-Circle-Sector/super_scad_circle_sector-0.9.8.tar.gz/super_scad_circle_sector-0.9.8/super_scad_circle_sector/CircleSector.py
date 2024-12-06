import math
from typing import Any, Dict, List, Tuple

from super_scad.boolean.Difference import Difference
from super_scad.boolean.Empty import Empty
from super_scad.boolean.Intersection import Intersection
from super_scad.d2.Circle import Circle
from super_scad.d2.Polygon import Polygon
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type.Angle import Angle
from super_scad.type.Vector2 import Vector2


class CircleSector(ScadWidget):
    """
    Widget for creating circle sectors.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 angle: float | None = None,
                 start_angle: float | None = None,
                 end_angle: float | None = None,
                 radius: float | None = None,
                 inner_radius: float | None = None,
                 outer_radius: float | None = None,
                 extend_by_eps_legs: bool | Tuple[bool, bool] | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 fn4n: bool | None = None):
        """
        Object constructor.

        :param angle: The angle of the circle sector (implies the starting angle is 0.0).
        :param start_angle: The start angle of the circle sector.
        :param end_angle: The end angle of the circle sector.
        :param radius: The radius of the circle sector (implies inner radius is 0.0).
        :param inner_radius: The inner radius of the circle sector.
        :param outer_radius: The outer radius of the circle sector.
        :param extend_by_eps_legs: Whether to extend the "legs", i.e., the straight sides of the circle sector, by eps
                                   for a clear overlap.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param fn4n: Whether to create a circle with a multiple of 4 vertices.
        """
        ScadWidget.__init__(self)

        self._angle: float | None = angle
        """
        The angle of the circle sector (implies the starting angle is 0.0).
        """

        self._start_angle: float | None = start_angle
        """
        The start angle of the circle sector.
        """

        self._end_angle: float | None = end_angle
        """
        The end angle of the circle sector.
        """

        self._radius: float | None = radius
        """
        The radius of the circle sector (implies inner radius is 0.0).
        """

        self._inner_radius: float | None = inner_radius
        """
        The inner radius of the circle sector.
        """

        self._outer_radius: float | None = outer_radius
        """
        The outer radius of the circle sector.
        """

        self._extend_by_eps_legs: bool | Tuple[bool, bool] | None = extend_by_eps_legs
        """
        Whether to extend the "legs", i.e., the straight sides of the circle sector.
        """

        self._fa: float | None = fa
        """
        The minimum angle (in degrees) of each fragment.
        """

        self._fs: float | None = fa
        """
        The minimum circumferential length of each fragment.
        """

        self._fn: int | None = fn
        """
        The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        """

        self._fn4n: bool | None = fn4n
        """
        Whether to create a circle with a multiple of 4 vertices.
        """

        self._extend_by_eps_legs: bool | Tuple[bool, bool] | None = extend_by_eps_legs
        """
        Whether to extend the "legs", i.e., the straight sides of the circle sector, by eps for a clear overlap.
        """

        self._validate_arguments(locals())

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _validate_arguments(args: Dict[str, Any]) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.
        """
        validator = ArgumentValidator(args)
        validator.validate_exclusive({'angle'}, {'start_angle', 'end_angle'})
        validator.validate_exclusive({'radius'}, {'inner_radius', 'outer_radius'})
        validator.validate_required({'radius', 'outer_radius'}, {'angle', 'end_angle'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle(self) -> float:
        """
        Returns the angle of the circle sector.
        """
        return Angle.normalize(self.end_angle - self.start_angle)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def start_angle(self) -> float:
        """
        Returns the start angle of the circle sector.
        """
        if self._start_angle is None:
            self._start_angle = Angle.normalize(self._angle) if self._angle < 0.0 else 0.0

        return Angle.normalize(self._start_angle)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def end_angle(self) -> float:
        """
        Returns the end angle of the circle sector.
        """
        if self._end_angle is None:
            self._end_angle = self._angle if self._angle > 0.0 else 0.0

        return Angle.normalize(self._end_angle)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float:
        """
        Returns the outer radius of the circle sector.
        """
        if self._radius is None:
            self._radius = self._outer_radius

        return self._radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_radius(self) -> float:
        """
        Returns the inner radius of this circle sector.
        """
        if self._inner_radius is None:
            self._inner_radius = 0.0

        return self._inner_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_radius(self) -> float:
        """
        Returns the outer radius of this circle sector.
        """
        if self._outer_radius is None:
            self._outer_radius = self._radius

        return self._outer_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_legs(self) -> Tuple[bool, bool]:
        """
        Returns whether to extend the "legs", i.e., the straight sides of the circle sector, by eps for a clear overlap.
        """
        if not isinstance(self._extend_by_eps_legs, Tuple):
            if self._extend_by_eps_legs is None:
                self._extend_by_eps_legs = (False, False)

            elif isinstance(self._extend_by_eps_legs, bool):
                self._extend_by_eps_legs = (self._extend_by_eps_legs, self._extend_by_eps_legs)

            else:
                raise ValueError('Expect extend_by_eps_legs to be a boolean or a tuple of two booleans, '
                                 f'got {type(self._extend_by_eps_legs)}')

        return self._extend_by_eps_legs

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fa(self) -> float | None:
        """
        Returns the minimum angle (in degrees) of each fragment.
        """
        return self._fa

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fs(self) -> float | None:
        """
        Returns the minimum circumferential length of each fragment.
        """
        return self._fs

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn4n(self) -> bool | None:
        """
        Returns whether to create a circle with multiple of 4 vertices.
        """
        return self._fn4n

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn(self) -> int | None:
        """
        Returns the fixed number of fragments in 360 degrees. Values of 3 or more override $fa and $fs.
        """
        return self._fn

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int:
        """
        Returns the convexity of the pie slice.
        """
        return 1 if self.angle < 180.0 else 2

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        angle = self.angle

        if round(self.outer_radius, context.length_digits) <= 0.0 or round(angle, context.angle_digits) == 0.0:
            return Empty()

        if round(self.inner_radius, context.length_digits) == 0.0:
            circles = Circle(radius=self.outer_radius, fa=self.fa, fs=self.fs, fn=self.fn, fn4n=self.fn4n)
        else:
            circles = Difference(children=[Circle(radius=self.outer_radius,
                                                  fa=self.fa,
                                                  fs=self.fs,
                                                  fn=self.fn,
                                                  fn4n=self.fn4n),
                                           Circle(radius=self.inner_radius,
                                                  fa=self.fa,
                                                  fs=self.fs,
                                                  fn=self.fn,
                                                  fn4n=self.fn4n)])

        if round(angle - 360.0, context.angle_digits) == 0.0:
            return circles

        if round(angle - 90.0, context.angle_digits) == 0.0:
            points = self._polygon_is_q1()

        elif round(angle - 180.0, context.angle_digits) == 0.0:
            points = self._polygon_is_q2()

        elif round(angle - 270.0, context.angle_digits) == 0.0:
            points = self._polygon_is_q3()

        elif round(angle - 90.0, context.angle_digits) < 0.0:
            points = self._polygon_in_q1()

        elif round(angle - 180.0, context.angle_digits) < 0.0:
            points = self._polygon_in_q2()

        elif round(angle - 270.0, context.angle_digits) < 0.0:
            points = self._polygon_in_q3()

        elif round(angle - 360.0, context.angle_digits) < 0.0:
            points = self._polygon_in_q4()
        else:
            raise ValueError('Math is broken!')

        extend_by_eps_sides = {index for index in range(len(points))}
        if not self.extend_by_eps_legs[0]:
            extend_by_eps_sides.remove(0)
        if not self.extend_by_eps_legs[1]:
            extend_by_eps_sides.remove(len(points) - 1)

        return Intersection(children=[circles,
                                      Polygon(points=points,
                                              convexity=self.convexity,
                                              extend_by_eps_sides=extend_by_eps_sides)])

    # ----------------------------------------------------------------------------------------------------------------------
    def _polygon_in_q1(self) -> List[Vector2]:
        """
        Returns a masking polygon in one quadrant.
        """
        phi = Angle.normalize(self.angle / 2.0, 90.0)
        start_angle = self.start_angle
        end_angle = self.end_angle

        size2 = self.outer_radius / math.cos(math.radians(phi))

        return [Vector2(0.0, 0.0),
                Vector2.from_polar_coordinates(size2, start_angle),
                Vector2.from_polar_coordinates(size2, end_angle)]

    # ----------------------------------------------------------------------------------------------------------------------
    def _polygon_in_q2(self) -> List[Vector2]:
        """
        Returns a masking polygon in two quadrants.
        """
        start_angle = self.start_angle
        end_angle = self.end_angle
        phi = Angle.normalize((start_angle - end_angle) / 2.0, 90.0)

        size1 = math.sqrt(2.0) * self.outer_radius
        size2 = size1 / (math.cos(math.radians(phi)) + math.sin(math.radians(phi)))

        return [Vector2.origin,
                Vector2.from_polar_coordinates(size2, start_angle),
                Vector2.from_polar_coordinates(size1, start_angle - phi + 90.0),
                Vector2.from_polar_coordinates(size2, end_angle)]

    # ----------------------------------------------------------------------------------------------------------------------
    def _polygon_in_q3(self) -> List[Vector2]:
        """
        Returns a masking polygon in three quadrants.
        """
        start_angle = self.start_angle
        end_angle = self.end_angle
        phi = Angle.normalize((start_angle - end_angle) / 2.0, 90.0)

        size1 = math.sqrt(2.0) * self.outer_radius
        size2 = size1 / (math.cos(math.radians(phi)) + math.sin(math.radians(phi)))

        return [Vector2.origin,
                Vector2.from_polar_coordinates(size2, start_angle),
                Vector2.from_polar_coordinates(size1, start_angle - phi + 90.0),
                Vector2.from_polar_coordinates(size1, start_angle - phi + 180.0),
                Vector2.from_polar_coordinates(size1, start_angle - phi + 270.0),
                Vector2.from_polar_coordinates(size2, end_angle)]

    # ----------------------------------------------------------------------------------------------------------------------
    def _polygon_in_q4(self) -> List[Vector2]:
        """
        Returns a masking polygon in four quadrants.
        """
        return self._polygon_in_q3()

    # ----------------------------------------------------------------------------------------------------------------------
    def _polygon_is_q1(self) -> List[Vector2]:
        """
        Returns a masking polygon that is exactly one quadrant.
        """
        start_angle = self.start_angle
        end_angle = self.end_angle

        size1 = math.sqrt(2.0) * self.outer_radius
        size2 = self.outer_radius

        return [Vector2.origin,
                Vector2.from_polar_coordinates(size2, start_angle),
                Vector2.from_polar_coordinates(size1, start_angle + 45.0),
                Vector2.from_polar_coordinates(size2, end_angle)]

    # ----------------------------------------------------------------------------------------------------------------------
    def _polygon_is_q2(self) -> List[Vector2]:
        """
        Returns a masking polygon that is exactly two quadrants.
        """
        start_angle = self.start_angle
        end_angle = self.end_angle

        size1 = math.sqrt(2.0) * self.outer_radius
        size2 = self.outer_radius

        return [Vector2.from_polar_coordinates(size2, start_angle),
                Vector2.from_polar_coordinates(size1, start_angle + 45.0),
                Vector2.from_polar_coordinates(size1, start_angle + 135.0),
                Vector2.from_polar_coordinates(size2, end_angle)]

    # ----------------------------------------------------------------------------------------------------------------------
    def _polygon_is_q3(self) -> List[Vector2]:
        """
        Returns a masking polygon that is exactly three quadrants.
        """
        start_angle = self.start_angle
        end_angle = self.end_angle

        size1 = math.sqrt(2.0) * self.outer_radius
        size2 = self.outer_radius

        return [Vector2.origin,
                Vector2.from_polar_coordinates(size2, start_angle),
                Vector2.from_polar_coordinates(size1, start_angle + 45.0),
                Vector2.from_polar_coordinates(size1, start_angle + 135.0),
                Vector2.from_polar_coordinates(size1, start_angle + 225.0),
                Vector2.from_polar_coordinates(size2, end_angle)]

# ----------------------------------------------------------------------------------------------------------------------
