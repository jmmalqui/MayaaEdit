import time
import pygame as pg
from typing import Union
import math


def ease_in_sine(x):
    return 1 - math.cos((x * math.pi) / 2)


def ease_out_sine(x):
    return math.sin((x * math.pi) / 2)


def ease_in_out_sine(x):
    return -1 * (math.cos(math.pi * x) - 1) / 2


def ease_in_quad(x):
    return x * x


def ease_out_quad(x):
    return 1 - (1 - x) * (1 - x)


def ease_in_out_quad(x):
    if x < 0.5:
        return 2 * x * x
    else:
        return 1 - math.pow(-2 * x + 2, 2) / 2


def ease_in_cubic(x):
    return x * x * x


def ease_out_cubic(x):
    return 1 - math.pow(1 - x, 3)


def ease_in_out_cubic(x):
    if x < 0.5:
        return 4 * x * x * x
    else:
        return 1 - math.pow(-2 * x + 2, 3) / 2


def ease_in_quart(x):
    return x * x * x * x


def ease_out_quart(x):
    return 1 - math.pow(1 - x, 4)


def ease_in_out_quart(x):
    if x < 0.5:
        return 8 * x * x * x * x
    else:
        return 1 - math.pow(-2 * x + 2, 4) / 2


def ease_in_quint(x):
    return x * x * x * x * x


def ease_out_quint(x):
    return 1 - math.pow(1 - x, 5)


def ease_in_out_quint(x):
    if x < 0.5:
        return 16 * x * x * x * x * x
    else:
        return 1 - math.pow(-2 * x + 2, 5) / 2


def ease_in_expo(x):
    return 0 if x == 0 else math.pow(2, 10 * x - 10)


def ease_out_expo(x):
    return 1 if x == 1 else 1 - math.pow(2, -10 * x)


def ease_in_out_expo(x):
    if x == 0:
        return 0
    if x == 1:
        return 1
    if x < 0.5:
        return math.pow(2, 20 * x - 10) / 2
    else:
        return (2 - math.pow(2, -20 * x + 10)) / 2


def ease_in_circ(x):
    return 1 - math.sqrt(1 - math.pow(x, 2))


def ease_out_circ(x):
    return math.sqrt(1 - math.pow(x - 1, 2))


def ease_in_out_circ(x):
    if x < 0.5:
        return (1 - math.sqrt(1 - math.pow(2 * x, 2))) / 2
    else:
        return (math.sqrt(1 - math.pow(-2 * x + 2, 2)) + 1) / 2


def ease_in_back(x):
    c1 = 1.70158
    c2 = c1 + 1
    return c2 * x * x * x - c1 * x * x


def ease_out_back(x):
    c1 = 1.70158
    c2 = c1 + 1
    return 1 + c2 * math.pow(x - 1, 3) + c1 * math.pow(x - 1, 2)


def ease_in_out_back(x):
    c1 = 1.70158
    c2 = c1 * 1.525

    return (
        (math.pow(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2
        if x < 0.5
        else (math.pow(2 * x - 2, 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2
    )


def ease_in_elastic(x):
    c1 = (2 * math.pi) / 3
    if x == 0:
        return 0
    if x == 1:
        return 1
    else:
        return math.pow(2, 10 * x - 10) * math.sin((x * 10 - 0.75) * c1)


def ease_out_elastic(x):
    c1 = (2 * math.pi) / 3
    if x == 0:
        return 0
    if x == 1:
        return 1
    else:
        return math.pow(2, -10 * x) * math.sin((x * 10 - 0.75) * c1) + 1


class EasingFunctions:
    EASE_IN_SINE = ease_in_sine
    EASE_OUT_SINE = ease_out_sine
    EASE_IN_OUT_SINE = ease_in_out_sine
    EASE_IN_QUAD = ease_in_quad
    EASE_OUT_QUAD = ease_out_quad
    EASE_IN_OUT_QUAD = ease_in_out_quad
    EASE_IN_CUBIC = ease_in_cubic
    EASE_OUT_CUBIC = ease_out_cubic
    EASE_IN_OUT_CUBIC = ease_in_out_cubic
    EASE_IN_QUART = ease_in_quart
    EASE_OUT_QUART = ease_out_quart
    EASE_IN_OUT_QUART = ease_in_out_quart
    EASE_IN_QUINT = ease_in_quint
    EASE_OUT_QUINT = ease_out_quint
    EASE_IN_OUT_QUINT = ease_in_out_quint
    EASE_IN_OUT_QUINT = ease_in_expo
    EASE_OUT_EXPO = ease_out_expo
    EASE_IN_OUT_EXPO = ease_in_out_expo
    EASE_IN_CIRC = ease_in_circ
    EASE_OUT_CIRC = ease_out_circ
    EASE_IN_OUT_CIRC = ease_in_out_circ
    EASE_IN_BACK = ease_in_back
    EASE_OUT_BACK = ease_out_back
    EASE_IN_OUT_BACK = ease_in_out_back
    EASE_IN_ELASTIC = ease_in_elastic
    EASE_OUT_ELASTIC = ease_out_elastic


class Animation:
    def __init__(self):
        self.dynamic_objects: list[DynamicObject] = []

    def update(self):
        for dynamic_object in self.dynamic_objects:
            dynamic_object.update()


class AnimationTypes:
    UNIDIRECTIONAL = 1
    PULSE = 2


class DynamicObject:
    def __init__(
        self,
        animation_manager: Animation,
        animation_object: Union[float, pg.Vector2, pg.Vector3],
    ):
        self.linear_interpolation_position = None
        self.animation_manager = animation_manager
        self.animation_object = animation_object
        self.begin_animation_object = None
        self.animation_manager.dynamic_objects.append(self)
        self.begin_timestamp = time.time()
        self.current_timestamp = time.time()
        self.animation_object_difference = None
        self.animation_function = None
        self.animation_duration = 0
        self.target_animation_object = None
        self.animation_fired = False
        self.animation_type = None
        self.forward_time = 0
        self.back_time = 0
        self.forward_animation = None
        self.back_animation = None
        self.pulse_begin_anim_obj = None
        self.pulse_end_anim_obj = None
        self.going_forward = True
        self.middle_timestamp = None

    def get_value(self):
        return self.animation_object

    def begin_pulsating_movement(self):
        if self.target_animation_object is None:
            return
        if self.current_timestamp >= self.forward_time + self.back_time:
            if (
                type(self.pulse_end_anim_obj) == pg.Vector2
                or type(self.pulse_end_anim_obj) == pg.Vector3
            ):
                self.animation_object = self.pulse_end_anim_obj.copy()
            else:
                self.animation_object = self.pulse_end_anim_obj
            self.animation_fired = False
            self.pulse_end_anim_obj = None
            self.pulse_begin_anim_obj = None
            self.forward_animation = None
            self.back_animation = None
            self.forward_animation = 0
            self.back_animation = 0
            self.animation_type = None

        if (
            self.current_timestamp >= self.forward_time
            and self.going_forward
            and self.animation_fired
        ):
            if (
                type(self.target_animation_object) == pg.Vector2
                or type(self.target_animation_object) == pg.Vector3
            ):
                self.animation_object = self.target_animation_object.copy()

            else:
                self.animation_object = self.target_animation_object
            self.animation_object_difference = (
                self.pulse_end_anim_obj - self.animation_object
            )
            self.middle_timestamp = time.time()
            self.going_forward = False

        if self.going_forward:
            if self.animation_fired:
                if self.forward_time:
                    self.linear_interpolation_position = self.forward_animation(
                        self.current_timestamp / self.forward_time
                    )
                    self.animation_object = (
                        self.pulse_begin_anim_obj
                        + self.linear_interpolation_position
                        * self.animation_object_difference
                    )
        if self.going_forward == False:
            elapsed_time_back = (time.time() - self.middle_timestamp) * 100
            if self.animation_fired:
                if self.back_time:
                    self.linear_interpolation_position = self.back_animation(
                        elapsed_time_back / self.back_time
                    )
                    self.animation_object = (
                        self.target_animation_object
                        + self.linear_interpolation_position
                        * self.animation_object_difference
                    )

    def begin_unidirectional_movement(self):
        if self.target_animation_object is None:
            return
        if self.current_timestamp >= self.animation_duration:
            if (
                type(self.target_animation_object) == pg.Vector2
                or type(self.target_animation_object) == pg.Vector3
            ):
                self.animation_object = self.target_animation_object.copy()
            else:
                self.animation_object = self.target_animation_object
            self.animation_fired = False

        if self.animation_function:
            if self.animation_fired:
                self.linear_interpolation_position = self.animation_function(
                    self.current_timestamp / self.animation_duration
                )
                self.animation_object = (
                    self.begin_animation_object
                    + self.linear_interpolation_position
                    * self.animation_object_difference
                )
        else:
            raise ValueError(
                f"No Animation Function was given.,{self.__class__.__name__}"
            )

    def is_moving(self):
        return self.animation_fired

    def pulse(
        self,
        begin: Union[float, pg.Vector2, pg.Vector3],
        target: Union[float, pg.Vector2, pg.Vector3],
        end: Union[float, pg.Vector2, pg.Vector3],
        forward_t,
        back_t,
        forward_anim_func,
        back_anim_func,
    ):
        self.animation_fired = True
        self.animation_type = AnimationTypes.PULSE
        self.begin_timestamp = time.time()
        self.going_forward = True
        if isinstance(begin, pg.Vector2) or isinstance(begin, pg.Vector3):
            self.animation_object = begin.copy()
            self.pulse_begin_anim_obj = begin.copy()
            self.target_animation_object = target.copy()
            self.pulse_end_anim_obj = end
        else:
            self.animation_object = begin
            self.pulse_begin_anim_obj = begin
            self.target_animation_object = target
            self.pulse_end_anim_obj = end
        self.forward_time = forward_t
        self.back_time = back_t
        self.forward_animation = forward_anim_func
        self.back_animation = back_anim_func
        self.animation_object_difference = target - begin

    def go_to(
        self,
        target: Union[float, pg.Vector2, pg.Vector3],
        duration: float,
        animation_function,
    ):
        self.animation_fired = True
        self.animation_type = AnimationTypes.UNIDIRECTIONAL
        self.begin_timestamp = time.time()
        if type(target) != type(self.animation_object):
            if type(target) not in [int, float] or type(self.animation_object) not in [
                int,
                float,
            ]:
                raise TypeError(
                    f"Data types mismatch. {target} != {self.animation_object}"
                )
        if isinstance(self.animation_object, Union[pg.Vector2, pg.Vector3]):
            self.begin_animation_object = self.animation_object.copy()
            self.target_animation_object = target.copy()
        else:
            self.begin_animation_object = self.animation_object
            self.target_animation_object = target
        self.animation_duration = duration
        self.animation_function = animation_function
        self.animation_object_difference = target - self.animation_object

    def update(self):
        if self.animation_fired:
            self.current_timestamp = (time.time() - self.begin_timestamp) * 100

            if self.animation_type == AnimationTypes.UNIDIRECTIONAL:
                self.begin_unidirectional_movement()
            if self.animation_type == AnimationTypes.PULSE:
                self.begin_pulsating_movement()
