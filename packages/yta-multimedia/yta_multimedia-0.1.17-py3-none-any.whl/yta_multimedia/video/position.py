from yta_multimedia.video.generation.manim.constants import HALF_SCENE_HEIGHT, HALF_SCENE_WIDTH
from yta_multimedia.video.generation.manim.utils.dimensions import ManimDimensions
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_general_utils.random import randrangefloat
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.image.region import NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE
from yta_general_utils.programming.parameter_validator import NumberValidator, PythonValidator
from random import choice as randchoice


class Position(Enum):
    """
    Enum class that represents a position within an specific
    scene. This is used to position a video or an image in that
    scene in an specific position defined by itself. It is
    useful with Manim and Moviepy video positioning and has
    been prepared to work with those engines.

    This position is a static position which means that it can
    be calculated by itself, without the need of any element
    size or similar. The coordinate that represent any of this
    """
    IN_EDGE_TOP = 'in_edge_top'
    """
    Just on the top edge of the scene.
    """
    IN_EDGE_BOTTOM = 'in_edge_bottom'
    IN_EDGE_RIGHT = 'in_edge_right'
    IN_EDGE_LEFT = 'in_edge_left'

    IN_EDGE_TOP_LEFT = 'in_edge_top_left'
    """
    Just on the upper left edge corner of the scene.
    """
    IN_EDGE_TOP_RIGHT = 'in_edge_top_right'
    IN_EDGE_BOTTOM_RIGHT = 'in_edge_bottom_right'
    IN_EDGE_BOTTOM_LEFT = 'in_edge_bottom_left'

    HALF_LEFT = 'half_left'
    """
    Between the left edge and the center of the scene.
    """
    HALF_TOP_LEFT = 'half_top_left'
    HALF_TOP = 'half_top'
    HALF_TOP_RIGHT = 'half_top_right'
    HALF_RIGHT = 'half_right'
    HALF_BOTTOM_RIGHT = 'half_bottom_right'
    HALF_BOTTOM = 'half_bottom'
    HALF_BOTTOM_LEFT = 'half_bottom_left'

    OUT_LEFT = 'out_left'
    """
    Imagine our scene surrounded by another 8 scenes.
    This will be at the center that surrounding scene
    that is on the left of this one.
    """
    OUT_TOP = 'out_top'
    """
    Imagine our scene surrounded by another 8 scenes.
    This will be at the center that surrounding scene
    that is on the top of this one.
    """
    OUT_RIGHT = 'out_right'
    """
    Imagine our scene surrounded by another 8 scenes.
    This will be at the center that surrounding scene
    that is on the right of this one.
    """
    OUT_BOTTOM = 'out_bottom'
    """
    Imagine our scene surrounded by another 8 scenes.
    This will be at the center that surrounding scene
    that is on the bottom of this one.
    """
    OUT_TOP_LEFT = 'out_top_left'
    """
    Imagine our scene surrounded by another 8 scenes.
    This will be at the center that surrounding scene
    that is on the top and left of this one.
    """
    OUT_TOP_RIGHT = 'out_top_right'
    """
    Imagine our scene surrounded by another 8 scenes.
    This will be at the center that surrounding scene
    that is on the top and right of this one.
    """
    OUT_BOTTOM_LEFT = 'out_bottom_left'
    """
    Imagine our scene surrounded by another 8 scenes.
    This will be at the center that surrounding scene
    that is on the bottom and left of this one.
    """
    OUT_BOTTOM_RIGHT = 'out_bottom_right'
    """
    Imagine our scene surrounded by another 8 scenes.
    This will be at the center that surrounding scene
    that is on the bottom and right of this one.
    """

    def get_moviepy_position_center(self, scene_size: tuple = (1920, 1080)):
        """
        Get the position tuple (x, y) of this position according
        to the scene defined by the provided 'scene_size'. That
        position belongs to a coordinate in which you can place
        the center of any element.

        This works considering the upper left corner as the (0, 0)
        coordinate.
        """
        if scene_size is None:
            scene_size = (1920, 1080)
        else:
            validate_size(scene_size, 'scene_size')

        # Alias to simplify :)
        w, h = scene_size

        if self == Position.IN_EDGE_TOP:
            position = (w / 2, 0)
        elif self == Position.IN_EDGE_BOTTOM:
            position = (w / 2, h)
        elif self == Position.IN_EDGE_LEFT:
            position = (0, h / 2)
        elif self == Position.IN_EDGE_RIGHT:
            position = (w, h / 2)
        
        elif self == Position.IN_EDGE_TOP_LEFT:
            position = (0, 0)
        elif self == Position.IN_EDGE_TOP_RIGHT:
            position = (w, 0)
        elif self == Position.IN_EDGE_BOTTOM_RIGHT:
            position = (w, h)
        elif self == Position.IN_EDGE_BOTTOM_LEFT:
            position = (0, h)
        
        elif self == Position.HALF_LEFT:
            position = (w / 4, h / 2)
        elif self == Position.HALF_TOP_LEFT:
            position = (w / 4, h / 4)
        elif self == Position.HALF_TOP:
            position = (w / 2, h / 4)
        elif self == Position.HALF_TOP_RIGHT:
            position = (3 * w / 4, h / 4)
        elif self == Position.HALF_RIGHT:
            position = (3 * w / 4, h / 2)
        elif self == Position.HALF_BOTTOM_RIGHT:
            position = (3 * w / 4, 3 * h / 4)
        elif self == Position.HALF_BOTTOM:
            position = (w / 2, 3 * h / 4)
        elif self == Position.HALF_BOTTOM_LEFT:
            position = (w / 4, 3 * h / 4)

        elif self == Position.OUT_LEFT:
            position = (-w, h / 2)
        elif self == Position.OUT_TOP:
            position = (w / 2, -h / 2)
        elif self == Position.OUT_RIGHT:
            position = (w + w / 2, h / 2)
        elif self == Position.OUT_BOTTOM:
            position = (w / 2, h + h / 2)
        elif self == Position.OUT_TOP_LEFT:
            position = (-w, -h / 2)
        elif self == Position.OUT_TOP_RIGHT:
            position = (w + w / 2, -h / 2)
        elif self == Position.OUT_BOTTOM_LEFT:
            position = (-w, h + h / 2)
        elif self == Position.OUT_BOTTOM_RIGHT:
            position = (w + w / 2, h + h / 2)

        return position
    
    def get_moviepy_position_upper_left_corner(self, video_size: tuple, scene_size: tuple = (1920, 1080)):
        """
        Get the position tuple (x, y) of this position according
        to the scene defined by the provided 'scene_size'. That 
        position belongs to a coordinate in which we need to put
        the moviepy video upper left corner to make its center be
        placed in this position.

        This method is useful to position a video in this desired
        position as it returns the value that can be directly used
        in 'with_position' method.

        This works considering the upper left corner as the (0, 0)
        coordinate.
        """
        if video_size is None:
            raise Exception('No "video_size" provided.')
        
        validate_size(video_size, 'video_size')
        
        # Obtain the position in which the center of the video
        # must be placed
        center_position = self.get_moviepy_position_center(scene_size)
        # TODO: Maybe force integer value (?)

        # Obtain the position in which we should place the video
        # (the upper left corner) to make the center of the video
        # be on that 'position_in_scene' position
        upper_left_corner = (center_position[0] - video_size[0] / 2, center_position[1] - video_size[1] / 2)

        return upper_left_corner
    
    def get_manim_position_center(self):
        """
        Get the position tuple (x, y, z) of this position according
        to the manim scene. That position belongs to a coordinate
        in which we need to put the manim video center to make its
        center be placed in this position.

        The 'z' value is always 0 as this is for a 2D scene.

        This works considering the upper left corner as the 
        (-HALF_SCENE_WIDTH, -HALF_SCENE_HEIGHT) coordinate.
        """
        # Alias to simplify :)
        hw, hh = HALF_SCENE_WIDTH, HALF_SCENE_WIDTH

        if self == Position.IN_EDGE_TOP:
            position = 0, hh, 0
        elif self == Position.IN_EDGE_BOTTOM:
            position = 0, -hh, 0
        elif self == Position.IN_EDGE_LEFT:
            position = -hw, 0, 0
        elif self == Position.IN_EDGE_RIGHT:
            position = hw, 0, 0

        elif self == Position.IN_EDGE_TOP_LEFT:
            position = -hw, hh, 0
        elif self == Position.IN_EDGE_TOP_RIGHT:
            position = hw, hh, 0
        elif self == Position.IN_EDGE_BOTTOM_RIGHT:
            position = hw, -hh, 0
        elif self == Position.IN_EDGE_BOTTOM_LEFT:
            position = -hw, -hh, 0
        
        elif self == Position.HALF_LEFT:
            position = -hw / 2, 0, 0
        elif self == Position.HALF_TOP_LEFT:
            position = -hw / 2, hh / 2, 0
        elif self == Position.HALF_TOP:
            position = 0, hh / 2, 0
        elif self == Position.HALF_TOP_RIGHT:
            position = hw / 2, hh / 2, 0
        elif self == Position.HALF_RIGHT:
            position = hw / 2, 0, 0
        elif self == Position.HALF_BOTTOM_RIGHT:
            position = hw / 2, -hh / 2, 0
        elif self == Position.HALF_BOTTOM:
            position = 0, -hh / 2, 0
        elif self == Position.HALF_BOTTOM_LEFT:
            position = -hw / 2, -hh / 2, 0

        elif self == Position.OUT_LEFT:
            position = 2 * -hw, 0, 0
        elif self == Position.OUT_TOP:
            position = 0, 2 * hh, 0
        elif self == Position.OUT_RIGHT:
            position = 2 * hw, 0, 0
        elif self == Position.OUT_BOTTOM:
            position = 0, 2 * -hh, 0
        elif self == Position.OUT_TOP_LEFT:
            position = 2 * -hw, 2 * hh
        elif self == Position.OUT_TOP_RIGHT:
            position = 2 * hw, 2 * hh
        elif self == Position.OUT_BOTTOM_LEFT:
            position = 2 * -hw, 2 * -hh
        elif self == Position.OUT_BOTTOM_RIGHT:
            position = 2 * hw, 2 * -hh

        return position
    
    # We don't need any upper left for manim because it
    # uses the center of the elements to position them
    
class DependantPosition(Enum):
    """
    Enum class that represents different positions within an
    scene of 1920x1080 that need a calculation because it
    depends on the size of the element we are trying to 
    position.
    """
    # TODO: Avoid the ones in Position that should not
    # be replaced
    TOP = 'top'
    TOP_RIGHT = 'top_right'
    RIGHT = 'right'
    BOTTOM_RIGHT = 'bottom_right'
    BOTTOM = 'bottom'
    BOTTOM_LEFT = 'bottom_left'
    LEFT = 'left'
    TOP_LEFT = 'top_left'

    OUT_TOP = 'out_top'
    OUT_TOP_RIGHT = 'out_top_right'
    OUT_RIGHT = 'out_right'
    OUT_BOTTOM_RIGHT = 'out_bottom_right'
    OUT_BOTTOM = 'out_bottom'
    OUT_BOTTOM_LEFT = 'out_bottom_left'
    OUT_LEFT = 'out_left'
    OUT_TOP_LEFT = 'out_top_left'

    QUADRANT_1_TOP_RIGHT_CORNER = 'quadrant_1_top_right_corner'
    QUADRANT_1_BOTTOM_RIGHT_CORNER = 'quadrant_1_bottom_right_corner'
    QUADRANT_1_BOTTOM_LEFT_CORNER = 'quadrant_1_bottom_left_corner'
    QUADRANT_2_TOP_LEFT_CORNER = 'quadrant_2_top_left_corner'
    QUADRANT_2_BOTTOM_RIGHT_CORNER = 'quadrant_2_bottom_right_corner'
    QUADRANT_2_BOTTOM_LEFT_CORNER = 'quadrant_2_bottom_left_corner'
    QUADRANT_3_TOP_RIGHT_CORNER = 'quadrant_3_top_right_corner'
    QUADRANT_3_TOP_LEFT_CORNER = 'quadrant_3_top_left_corner'
    QUADRANT_3_BOTTOM_LEFT_CORNER = 'quadrant_3_bottom_left_corner'
    QUADRANT_4_TOP_RIGHT_CORNER = 'quadrant_4_top_right_corner'
    QUADRANT_4_TOP_LEFT_CORNER = 'quadrant_4_top_left_corner'
    QUADRANT_4_BOTTOM_RIGHT_CORNER = 'quadrant_4_bottom_right_corner'

    RANDOM_INSIDE = 'random_inside'
    RANDOM_OUTSIDE = 'random_outside'

    @staticmethod
    def _get_outside_items_as_list():
        """
        Get a list of the DependantPosition items that are placed
        outside of the screen limits.
        """
        return [
            DependantPosition.OUT_TOP_LEFT,
            DependantPosition.OUT_TOP,
            DependantPosition.OUT_RIGHT,
            DependantPosition.OUT_BOTTOM_RIGHT,
            DependantPosition.OUT_BOTTOM,
            DependantPosition.OUT_BOTTOM_LEFT,
            DependantPosition.OUT_LEFT
        ]
    
    @staticmethod
    def get_random_outside():
        """
        Get one random DependantPosition element that is placed
        outside of the screen limits.
        """
        return randchoice(DependantPosition._get_outside_items_as_list())

    @staticmethod
    def _get_inside_items_as_list():
        """
        Get a list of the DependantPosition items that are placed
        inside of the screen limits.
        """
        return list(set(DependantPosition.get_all()) - set(DependantPosition._get_outside_items_as_list()) - set([DependantPosition.RANDOM_INSIDE]) - set([DependantPosition.RANDOM_OUTSIDE]))

    @staticmethod
    def get_random_inside():
        """
        Get one random DependantPosition element that is placed
        inside of the screen limits.
        """
        return randchoice(DependantPosition._get_inside_items_as_list())

    def get_moviepy_position_center(self, video_size: tuple = (1920, 1080), scene_size: tuple = (1920, 1080)):
        """
        Get the position tuple (x, y) of this position according
        to the scene defined by the provided 'scene_size'. That 
        position belongs to a coordinate in which we need to put
        the moviepy video center to be placed in the desired
        position.

        This method is useful cannot be used directly to position
        a video as it is returning the coordinate in which the
        center must be placed and moviepy uses the upper left
        corner to be positioned, so consider using the method
        'get_moviepy_position_upper_left_corner' to obtain it.

        This works considering the upper left corner of the scene
        as the (0, 0) coordinate.
        """
        if video_size is None:
            video_size = (1920, 1080)
        else:
            validate_size(video_size, 'video_size')

        if scene_size is None:
            scene_size = (1920, 1080)
        else:
            validate_size(scene_size, 'scene_size')
            
        # Alias to simplify :)
        sw, sh = scene_size
        vw, vh = video_size

        if self == DependantPosition.TOP:
            position = sw / 2, -vh / 2
        elif self == DependantPosition.RIGHT:
            position = sw - vw / 2, sh / 2
        elif self == DependantPosition.BOTTOM:
            position = sw / 2, sh - vh
        elif self == DependantPosition.LEFT:
            position = vw / 2, sh / 2

        elif self == DependantPosition.TOP_RIGHT:
            position = sw - vw / 2, vh / 2
        elif self == DependantPosition.BOTTOM_RIGHT:
            position = sw - vw / 2, sh - vh / 2
        elif self == DependantPosition.BOTTOM_LEFT:
            position = vw / 2, sh - vh / 2
        elif self == DependantPosition.TOP_LEFT:
            position = vw / 2, vh / 2

        elif self == DependantPosition.OUT_TOP:
            position = sw / 2, -vh / 2
        elif self == DependantPosition.OUT_TOP_RIGHT:
            position = sw + vw / 2, -vh / 2
        elif self == DependantPosition.OUT_RIGHT:
            position = sw + vw / 2, sh / 2
        elif self == DependantPosition.OUT_BOTTOM_RIGHT:
            position = sw + vw / 2, sh + vh / 2
        elif self == DependantPosition.OUT_BOTTOM:
            position = sw / 2, sh + vh / 2
        elif self == DependantPosition.OUT_BOTTOM_LEFT:
            position = -vw / 2, sh + vh / 2
        elif self == DependantPosition.OUT_LEFT:
            position = -vw / 2, sh / 2
        elif self == DependantPosition.OUT_TOP_LEFT:
            position = -vw / 2, -vh / 2

        elif self == DependantPosition.QUADRANT_1_TOP_RIGHT_CORNER:
            position = sw / 2 - vw / 2, vh / 2
        elif self == DependantPosition.QUADRANT_1_BOTTOM_RIGHT_CORNER:
            position = sw / 2 - vw / 2, sh / 2 - vh / 2
        elif self == DependantPosition.QUADRANT_1_BOTTOM_LEFT_CORNER:
            position = vw / 2, sh / 2 - vh / 2
        elif self == DependantPosition.QUADRANT_2_TOP_LEFT_CORNER:
            position = sw / 2 + vw / 2, vh / 2
        elif self == DependantPosition.QUADRANT_2_BOTTOM_RIGHT_CORNER:
            position = sw - vw / 2, sh / 2 - vh / 2
        elif self == DependantPosition.QUADRANT_2_BOTTOM_LEFT_CORNER:
            position = sw / 2 + vw / 2, sh / 2 - vh / 2
        elif self == DependantPosition.QUADRANT_3_TOP_RIGHT_CORNER:
            position = sw - vw / 2, sh / 2 + vh / 2
        elif self == DependantPosition.QUADRANT_3_TOP_LEFT_CORNER:
            position = sw / 2 + vw / 2, sh / 2 + vh / 2
        elif self == DependantPosition.QUADRANT_3_BOTTOM_LEFT_CORNER:
            position = sw / 2 + vw / 2, sh - vh / 2
        elif self == DependantPosition.QUADRANT_4_TOP_RIGHT_CORNER:
            position = sw / 2 - vw / 2, sh / 2 + vh / 2
        elif self == DependantPosition.QUADRANT_4_TOP_LEFT_CORNER:
            position = vw / 2, sh / 2 + vh / 2
        elif self == DependantPosition.QUADRANT_4_BOTTOM_RIGHT_CORNER:
            position = sw / 2 - vw / 2, sh - vh / 2

        return position

    def get_moviepy_position_upper_left_corner(self, video_size: tuple, scene_size: tuple = (1920, 1080)):
        """
        Get the position tuple (x, y) of this position according
        to the scene defined by the provided 'scene_size'. That 
        position belongs to a coordinate in which we need to put
        the moviepy video upper left corner to make its center be
        placed in this position.

        This method is useful to position a video in this desired
        position as it returns the value that can be directly used
        in 'with_position' method.

        This works considering the upper left corner as the (0, 0)
        coordinate.
        """
        # Obtain the position in which the center of the video
        # must be placed
        center_position = self.get_moviepy_position_center(video_size, scene_size)
        # TODO: Maybe force integer value (?)

        # Obtain the position in which we should place the video
        # (the upper left corner) to make the center of the video
        # be on that previously obtained 'center_position' position
        upper_left_corner = (center_position[0] - video_size[0] / 2, center_position[1] - video_size[1] / 2)

        return upper_left_corner

    def get_manim_position_center(self, video_size: tuple):
        if video_size is None:
            raise Exception('No "video_size" provided.')
        
        validate_size(video_size, 'video_size')
        
        # Alias to simplify :)
        hsw, hsh = HALF_SCENE_WIDTH, HALF_SCENE_HEIGHT
        vw, vh = video_size

        # TODO: Process
        if self == DependantPosition.TOP:
            position = 0, hsh - vh / 2, 0
        elif self == DependantPosition.TOP_RIGHT:
            position = hsw - vw / 2, hsh - vh / 2, 0
        elif self == DependantPosition.RIGHT:
            position = hsw - vw / 2, 0, 0
        elif self == DependantPosition.BOTTOM_RIGHT:
            position = hsw - vw / 2, -hsh + vh / 2, 0
        elif self == DependantPosition.BOTTOM:
            position = 0, -hsh + vh / 2, 0
        elif self == DependantPosition.BOTTOM_LEFT:
            position = -hsw + vw / 2, -hsh + vh / 2, 0
        elif self == DependantPosition.LEFT:
            position = -hsw + vw / 2, 0, 0
        elif self == DependantPosition.TOP_LEFT:
            position = -hsw + vw / 2, hsh - vh / 2, 0
        elif self == DependantPosition.OUT_TOP_LEFT:
            position = -hsw - vw / 2, hsh + vh / 2, 0
        elif self == DependantPosition.OUT_TOP:
            position = 0, hsh + vh / 2, 0
        elif self == DependantPosition.OUT_TOP_RIGHT:
            position = hsw + vw / 2, hsh + vh / 2, 0
        elif self == DependantPosition.OUT_RIGHT:
            return hsw + vw / 2, 0, 0
        elif self == DependantPosition.OUT_BOTTOM_RIGHT:
            position = hsw + vw / 2, -hsh - vh / 2, 0
        elif self == DependantPosition.OUT_BOTTOM:
            position = 0, -hsh - vh / 2, 0
        elif self == DependantPosition.OUT_BOTTOM_LEFT:
            position = -hsw - vw / 2, -hsh - vh / 2, 0
        elif self == DependantPosition.OUT_LEFT:
            position = -hsw - vh / 2, 0, 0
        elif self == DependantPosition.QUADRANT_1_TOP_RIGHT_CORNER:
            position = -vw / 2, hsh - vh / 2, 0
        elif self == DependantPosition.QUADRANT_1_BOTTOM_RIGHT_CORNER:
            position = -vw / 2, vh / 2, 0
        elif self == DependantPosition.QUADRANT_1_BOTTOM_LEFT_CORNER:
            position = -hsw + vw / 2, vh / 2, 0
        elif self == DependantPosition.QUADRANT_2_TOP_LEFT_CORNER:
            position = vw / 2, hsh - vh / 2, 0
        elif self == DependantPosition.QUADRANT_2_BOTTOM_RIGHT_CORNER:
            position = hsw - vw / 2, vh / 2, 0
        elif self == DependantPosition.QUADRANT_2_BOTTOM_LEFT_CORNER:
            position = vw / 2, vh / 2, 0
        elif self == DependantPosition.QUADRANT_3_TOP_LEFT_CORNER:
            position = vw / 2, -vh / 2, 0
        elif self == DependantPosition.QUADRANT_3_TOP_RIGHT_CORNER:
            position = hsw - vw / 2, -vh / 2, 0
        elif self == DependantPosition.QUADRANT_3_BOTTOM_LEFT_CORNER:
            position = vw / 2, -hsh + vh / 2, 0
        elif self == DependantPosition.QUADRANT_4_TOP_LEFT_CORNER:
            position = -hsw + vw / 2, -vh / 2, 0
        elif self == DependantPosition.QUADRANT_4_TOP_RIGHT_CORNER:
            position = -vw / 2, -vh / 2, 0
        elif self == DependantPosition.QUADRANT_4_BOTTOM_RIGHT_CORNER:
            position = -vw / 2, -hsh + vh / 2, 0
        elif self == DependantPosition.RANDOM_INSIDE:
            position = DependantPosition.get_random_inside().get_manim_position_center((vw, vh))
        elif self == DependantPosition.RANDOM_OUTSIDE:
            position = DependantPosition.get_random_outside().get_manim_position_center((vw, vh))

        return position
    
# TODO: These 2 methods below are similar to the ones in
# yta_multimedia\video\edition\effect\moviepy\position\objects\coordinate.py
def is_size_valid(size: tuple):
    """
    Check if the provided 'size' is a valid value or not.
    """
    if not PythonValidator.is_tuple(size) or len(size) != 2 or not NumberValidator.is_number_between(size[0], 1, NORMALIZATION_MAX_VALUE) or not NumberValidator.is_number_between(size[1], 1, NORMALIZATION_MAX_VALUE):
        return False
    
    return True

def validate_size(size: tuple, parameter_name: str):
    """
    Validate the provided 'size' and raises an Exception if
    not valid.
    """
    if not is_size_valid(size):
        raise Exception(f'The provided {parameter_name} parameter is not a tuple or does not have 2 elements that are numbers between 1 and {str(NORMALIZATION_MAX_VALUE)}.')












# TODO: Remove this below when above code is working


# # TODO: This below has to be removed or refactored
# def get_center(video: Clip, background_video: Clip):
#     """
#     Returns the x,y coords in which the provided 'video' will
#     be centered according to the provided 'background_video' in
#     which it will be overlayed.

#     This method returns two elements, first one is the x and the
#     second one is the y.
#     """
#     # TODO: Ensure 'video' and 'background_video' are valid videos
#     return background_video.w / 2 - video.w / 2, background_video.h / 2 - video.h / 2

# class CalculatedxPosition(Enum):
#     """
#     Enum class that represents different positions within an
#     scene of 1920x1080 that need a calculation because it
#     depends on the size of the element we are trying to 
#     position.
#     """
#     OUT_TOP_LEFT = 'out_top_left'
#     """
#     Out of the screen, on the top left corner, just one pixel
#     out of bounds.
#     """
#     IN_EDGE_TOP_LEFT = 'in_edge_top_left'
#     """
#     The center of the video is on the top left corner, so only
#     the bottom right quarter part of the video is shown (inside
#     the screen).
#     """
#     TOP_LEFT = 'top_left'
#     """
#     The video is completely visible, just at the top left 
#     corner of the screen.
#     """
#     OUT_TOP = 'out_top'
#     IN_EDGE_TOP = 'in_edge_top'
#     TOP = 'top'
#     OUT_TOP_RIGHT = 'out_top_right'
#     IN_EDGE_TOP_RIGHT = 'in_edge_top_right'
#     TOP_RIGHT = 'top_right'
#     CENTER = 'center'
#     OUT_RIGHT = 'out_right'
#     IN_EDGE_RIGHT = 'in_edge_right'
#     RIGHT = 'right'
#     OUT_BOTTOM_RIGHT = 'out_bottom_right'
#     IN_EDGE_BOTTOM_RIGHT = 'in_edge_bottom_right'
#     BOTTOM_RIGHT = 'bottom_right'
#     OUT_BOTTOM = 'out_bottom'
#     IN_EDGE_BOTTOM = 'in_edge_bottom'
#     BOTTOM = 'bottom'
#     OUT_BOTTOM_LEFT = 'out_bottom_left'
#     IN_EDGE_BOTTOM_LEFT = 'in_edge_bottom_left'
#     BOTTOM_LEFT = 'bottom_left'
#     OUT_LEFT = 'out_left'
#     IN_EDGE_LEFT = 'in_edge_left'
#     LEFT = 'left'

#     HALF_TOP = 'half_top'
#     HALF_TOP_RIGHT = 'half_top_right'
#     HALF_RIGHT = 'half_right'
#     HALF_BOTTOM_RIGHT = 'half_bottom_right'
#     HALF_BOTTOM = 'half_bottom'
#     HALF_BOTTOM_LEFT = 'half_bottom_left'
#     HALF_LEFT = 'half_left'
#     HALF_TOP_LEFT = 'half_top_left'

#     QUADRANT_1_TOP_RIGHT_CORNER = 'quadrant_1_top_right_corner'
#     QUADRANT_1_BOTTOM_RIGHT_CORNER = 'quadrant_1_bottom_right_corner'
#     QUADRANT_1_BOTTOM_LEFT_CORNER = 'quadrant_1_bottom_left_corner'
#     QUADRANT_2_TOP_LEFT_CORNER = 'quadrant_2_top_left_corner'
#     QUADRANT_2_BOTTOM_RIGHT_CORNER = 'quadrant_2_bottom_right_corner'
#     QUADRANT_2_BOTTOM_LEFT_CORNER = 'quadrant_2_bottom_left_corner'
#     QUADRANT_3_TOP_RIGHT_CORNER = 'quadrant_3_top_right_corner'
#     QUADRANT_3_TOP_LEFT_CORNER = 'quadrant_3_top_left_corner'
#     QUADRANT_3_BOTTOM_LEFT_CORNER = 'quadrant_3_bottom_left_corner'
#     QUADRANT_4_TOP_RIGHT_CORNER = 'quadrant_4_top_right_corner'
#     QUADRANT_4_TOP_LEFT_CORNER = 'quadrant_4_top_left_corner'
#     QUADRANT_4_BOTTOM_RIGHT_CORNER = 'quadrant_4_bottom_right_corner'

#     RANDOM_INSIDE = 'random_inside'
#     """
#     A random position inside the screen with no pixels out of bounds.
#     It is randomly chosen from one of all the options inside the limits
#     we have.
#     """
#     RANDOM_OUTSIDE = 'random_outside'
#     """
#     A random position out of the screen limits. It is randomly chosen 
#     from one of all the options outside the limits we have.
#     """
#     # TODO: Add more positions maybe (?)

#     @classmethod
#     def outside_positions_as_list(cls):
#         """
#         Returns the Position enums that are located out of
#         the screen limits.
#         """
#         return [
#             cls.OUT_TOP_LEFT,
#             cls.OUT_TOP,
#             cls.OUT_RIGHT,
#             cls.OUT_BOTTOM_RIGHT,
#             cls.OUT_BOTTOM,
#             cls.OUT_BOTTOM_LEFT,
#             cls.OUT_LEFT
#         ]

#     @classmethod
#     def random_outside_position(cls):
#         """
#         Return a position located outside of the screen
#         limits that is chosen randomly from the existing
#         options.
#         """
#         return randchoice(cls.outside_positions_as_list())
    
#     @classmethod
#     def inside_positions_as_list(cls):
#         """
#         Returns the Position enums that are located inside
#         the screen limits.
#         """
#         return list(set(cls.get_all()) - set(cls.outside_positions_as_list()) - set([cls.RANDOM_INSIDE]) - set([cls.RANDOM_OUTSIDE]))
    
#     @classmethod
#     def random_inside_position(cls):
#         """
#         Return a position located inside the screen limits
#         that is chosen randomly from the existing options.
#         """
#         return randchoice(cls.inside_positions_as_list())


#     # TODO: Add a new 'default' method that uses a ColorClip
#     # of 1920x1080 for video and background to make the 
#     # size and position calculations
    
#     def get_manim_limits(self):
#         """
#         Return the left, right, top and bottom limits for this
#         screen position. This edges represent the limits of the
#         region in which the video should be placed to fit this
#         screen position.

#         We consider each screen region as a limited region of
#         half of the scene width and height.

#         Corner limits:
#         [-7-1/9,  4, 0]   [0,  4, 0]   [7+1/9,  4, 0]
#         [-7-1/9,  0, 0]   [0,  0, 0]   [7+1/9,  0, 0]
#         [-7-1/9, -4, 0]   [0, -4, 0]   [7+1/9, -4, 0]
#         """
#         # TODO: I think I should consider regions of 1/8 of width and height
#         # so 1 quadrant is divided into 4 pieces and I build all the positions
#         # for also those quadrants
#         # TODO: I'm missing the QUADRANT_1_HALF_TOP and HALF_TOP_OUT, ...
#         if self == Position.TOP:
#             return -HALF_SCENE_WIDTH / 2, HALF_SCENE_WIDTH / 2, HALF_SCENE_HEIGHT, 0
#         elif self == Position.BOTTOM:
#             return -HALF_SCENE_WIDTH / 2, HALF_SCENE_WIDTH / 2, -HALF_SCENE_HEIGHT, 0
#         elif self == Position.LEFT:
#             return -HALF_SCENE_WIDTH, 0, HALF_SCENE_HEIGHT / 2, -HALF_SCENE_HEIGHT / 2
#         elif self == Position.RIGHT:
#             return 0, HALF_SCENE_WIDTH, HALF_SCENE_HEIGHT / 2, -HALF_SCENE_HEIGHT / 2
#         # TODO: Add missing

#         # TODO: Is this method necessary (?)

#     def get_manim_position(self, video_size: tuple):
#         """
#         Return the position in which the mobject must be placed to
#         be exactly in this position.

#         This method returns a x,y,z position.
#         """
#         if video_size is None:
#             raise Exception('No "video_size" provided.')

#         # TODO: Manim uses another system
#         if not NumberValidator.is_number_between(video_size[0], 1, NORMALIZATION_MAX_VALUE):
#             raise Exception(f'The provided "video_size" parameter first element "{str(video_size[0])}" is not a number between 1 and {str(NORMALIZATION_MAX_VALUE)}.')
            
#         if not NumberValidator.is_number_between(video_size[1], 1, NORMALIZATION_MAX_VALUE):
#             raise Exception(f'The provided "video_size" parameter second element "{str(video_size[1])}" is not a number between 1 and {str(NORMALIZATION_MAX_VALUE)}.')

#         # TODO: 'width' and 'height' must be manim

#         if self == CalculatedPosition.TOP:
#             return 0, HALF_SCENE_HEIGHT - height / 2, 0
#         elif self == Position.TOP_RIGHT:
#             return HALF_SCENE_WIDTH - width / 2, HALF_SCENE_HEIGHT - height / 2, 0
#         elif self == Position.RIGHT:
#             return HALF_SCENE_WIDTH - width / 2, 0, 0
#         elif self == Position.BOTTOM_RIGHT:
#             return HALF_SCENE_WIDTH - width / 2, -HALF_SCENE_HEIGHT + height / 2, 0
#         elif self == Position.BOTTOM:
#             return 0, -HALF_SCENE_HEIGHT + height / 2, 0
#         elif self == Position.BOTTOM_LEFT:
#             return -HALF_SCENE_WIDTH + width / 2, -HALF_SCENE_HEIGHT + height / 2, 0
#         elif self == Position.LEFT:
#             return -HALF_SCENE_WIDTH + width / 2, 0, 0
#         elif self == Position.TOP_LEFT:
#             return -HALF_SCENE_WIDTH + width / 2, HALF_SCENE_HEIGHT - height / 2, 0
#         elif self == Position.CENTER:
#             return 0, 0, 0
#         elif self == Position.IN_EDGE_TOP_LEFT:
#             return -HALF_SCENE_WIDTH, HALF_SCENE_HEIGHT, 0
#         elif self == Position.OUT_TOP_LEFT:
#             return -HALF_SCENE_WIDTH - width / 2, HALF_SCENE_HEIGHT + height / 2, 0
#         elif self == Position.IN_EDGE_TOP:
#             return 0, HALF_SCENE_HEIGHT, 0
#         elif self == Position.OUT_TOP:
#             return 0, HALF_SCENE_HEIGHT + height / 2, 0
#         elif self == Position.IN_EDGE_TOP_RIGHT:
#             return HALF_SCENE_WIDTH, HALF_SCENE_HEIGHT, 0
#         elif self == Position.OUT_TOP_RIGHT:
#             return HALF_SCENE_WIDTH + width / 2, HALF_SCENE_HEIGHT + height / 2, 0
#         elif self == Position.IN_EDGE_RIGHT:
#             return HALF_SCENE_WIDTH, 0, 0
#         elif self == Position.OUT_RIGHT:
#             return HALF_SCENE_WIDTH + width / 2, 0, 0
#         elif self == Position.IN_EDGE_BOTTOM_RIGHT:
#             return HALF_SCENE_WIDTH, -HALF_SCENE_HEIGHT, 0
#         elif self == Position.OUT_BOTTOM_RIGHT:
#             return HALF_SCENE_WIDTH + width / 2, -HALF_SCENE_HEIGHT - height / 2, 0
#         elif self == Position.IN_EDGE_BOTTOM:
#             return 0, -HALF_SCENE_HEIGHT, 0
#         elif self == Position.OUT_BOTTOM:
#             return 0, -HALF_SCENE_HEIGHT - height / 2, 0
#         elif self == Position.IN_EDGE_BOTTOM_LEFT:
#             return -HALF_SCENE_WIDTH, -HALF_SCENE_HEIGHT, 0
#         elif self == Position.OUT_BOTTOM_LEFT:
#             return -HALF_SCENE_WIDTH - width / 2, -HALF_SCENE_HEIGHT - height / 2, 0
#         elif self == Position.IN_EDGE_LEFT:
#             return -HALF_SCENE_WIDTH, 0, 0
#         elif self == Position.OUT_LEFT:
#             return -HALF_SCENE_WIDTH - width / 2, 0, 0
#         elif self == Position.HALF_TOP:
#             return 0, HALF_SCENE_HEIGHT / 2, 0
#         elif self == Position.HALF_TOP_RIGHT:
#             return HALF_SCENE_WIDTH / 2, HALF_SCENE_HEIGHT / 2, 0
#         elif self == Position.HALF_RIGHT:
#             return HALF_SCENE_WIDTH / 2, 0, 0
#         elif self == Position.HALF_BOTTOM_RIGHT:
#             return HALF_SCENE_WIDTH / 2, -HALF_SCENE_HEIGHT / 2, 0
#         elif self == Position.HALF_BOTTOM:
#             return 0, -HALF_SCENE_HEIGHT / 2, 0
#         elif self == Position.HALF_BOTTOM_LEFT:
#             return -HALF_SCENE_WIDTH / 2, -HALF_SCENE_HEIGHT / 2, 0
#         elif self == Position.HALF_LEFT:
#             return -HALF_SCENE_WIDTH / 2, 0, 0
#         elif self == Position.HALF_TOP_LEFT:
#             return -HALF_SCENE_WIDTH / 2, HALF_SCENE_HEIGHT / 2, 0
#         elif self == Position.QUADRANT_1_TOP_RIGHT_CORNER:
#             return -width / 2, HALF_SCENE_HEIGHT - height / 2, 0
#         elif self == Position.QUADRANT_1_BOTTOM_RIGHT_CORNER:
#             return -width / 2, height / 2, 0
#         elif self == Position.QUADRANT_1_BOTTOM_LEFT_CORNER:
#             return -HALF_SCENE_WIDTH + width / 2, height / 2, 0
#         elif self == Position.QUADRANT_2_TOP_LEFT_CORNER:
#             return width / 2, HALF_SCENE_HEIGHT - height / 2, 0
#         elif self == Position.QUADRANT_2_BOTTOM_RIGHT_CORNER:
#             return HALF_SCENE_WIDTH - width / 2, height / 2, 0
#         elif self == Position.QUADRANT_2_BOTTOM_LEFT_CORNER:
#             return width / 2, height / 2, 0
#         elif self == Position.QUADRANT_3_TOP_LEFT_CORNER:
#             return width / 2, -height / 2, 0
#         elif self == Position.QUADRANT_3_TOP_RIGHT_CORNER:
#             return HALF_SCENE_WIDTH - width / 2, -height / 2, 0
#         elif self == Position.QUADRANT_3_BOTTOM_LEFT_CORNER:
#             return width / 2, -HALF_SCENE_HEIGHT + height / 2, 0
#         elif self == Position.QUADRANT_4_TOP_LEFT_CORNER:
#             return -HALF_SCENE_WIDTH + width / 2, -height / 2, 0
#         elif self == Position.QUADRANT_4_TOP_RIGHT_CORNER:
#             return -width / 2, -height / 2, 0
#         elif self == Position.QUADRANT_4_BOTTOM_RIGHT_CORNER:
#             return -width / 2, -HALF_SCENE_HEIGHT + height / 2, 0
#         elif self == Position.RANDOM_INSIDE:
#             return randchoice(Position.inside_positions_as_list()).get_manim_position(width, height)
#         elif self == Position.RANDOM_OUTSIDE:
#             return randchoice(Position.outside_positions_as_list()).get_manim_position(width, height)
        
#     def get_manim_random_position(self, width: float, height: float):
#         """
#         Calculate the position in which the center of the element 
#         with the provided 'width' and 'height' must be placed to
#         obtain this position.

#         The position will be provided as a 3D vector but the z
#         axis will be always 0.

#         The provided 'width' and 'height' must be in pixels.
#         """
#         # TODO: Check if the provided 'width' and 'height' are in
#         # in pixels and valid or if not

#         # TODO: By now I'm just using the limits as numeric limits
#         # for random position that will be used as the center of the
#         # video, but we will need to consider the video dimensions 
#         # in a near future to actually position it well, because the
#         # video can be out of the scene right now with this approach
#         left, right, top, bottom = self.get_manim_limits()

#         x, y = randrangefloat(left, right, ManimDimensions.width_to_manim_width(1)), randrangefloat(top, bottom, ManimDimensions.height_to_manim_height(1))

#         # If video is larger than HALF/2 it won't fit correctly.
#         if width > HALF_SCENE_WIDTH or height > HALF_SCENE_HEIGHT:
#             # TODO: Video is bigger than the region, we cannot make
#             # it fit so... what can we do (?)
#             return x, y

#         if x - width / 2 < left:
#             x += left - (x - width / 2)
#         if x + width / 2 > right:
#             x -= (x + width / 2) - right
#         if y - height / 2 < bottom:
#             y += bottom - (y - height / 2)
#         if y + height / 2 > top:
#             y -= (y + height / 2) - top

#         return x, y, 0
#         # TODO: Is this method necessary (?) I think yes, because
#         # it generates a random position in a region, not a random
#         # choice of our predefined (and always the same) positions

#     def get_moviepy_position(self, video: Clip = None, background_video: Clip = None, do_normalize: bool = False):
#         """
#         This method will calculate the (x, y) tuple position for the provided
#         'video' over the also provided 'background_video' that would be,
#         hypothetically, a 1920x1080 black color background static image. The
#         provided 'position' will be transformed into the (x, y) tuple according
#         to our own definitions.
#         """
#         if not video:
#             video = ClipGenerator.get_default_background_video(is_transparent = False)

#         if not background_video:
#             background_video = ClipGenerator.get_default_background_video()

#         # TODO: Do 'video' and 'background_video' checkings
#         position_tuple = None

#         if self == Position.CENTER:
#             position_tuple = (get_center(video, background_video))

#         #           Edges below
#         # TOP
#         elif self == Position.OUT_TOP:
#             position_tuple = ((background_video.w / 2) - (video.w / 2), -video.h)
#         elif self == Position.IN_EDGE_TOP:
#             position_tuple = ((background_video.w / 2) - (video.w / 2), -(video.h / 2))
#         elif self == Position.TOP:
#             position_tuple = ((background_video.w / 2) - (video.w / 2), 0)
#         # TOP RIGHT
#         elif self == Position.OUT_TOP_RIGHT:
#             position_tuple = (background_video.w, -video.h)
#         elif self == Position.IN_EDGE_TOP_RIGHT:
#             position_tuple = (background_video.w - (video.w / 2), -(video.h / 2))
#         elif self == Position.TOP_RIGHT:
#             position_tuple = (background_video.w - video.w, 0)
#         # RIGHT
#         elif self == Position.OUT_RIGHT:
#             position_tuple = (background_video.w, (background_video.h / 2) - (video.h / 2))
#         elif self == Position.IN_EDGE_RIGHT:
#             position_tuple = (background_video.w - (video.w / 2), (background_video.h / 2) - (video.h / 2))
#         elif self == Position.RIGHT:
#             position_tuple = (background_video.w - video.w, (background_video.h / 2) - (video.h / 2))
#         # BOTTOM RIGHT
#         elif self == Position.OUT_BOTTOM_RIGHT:
#             position_tuple = (background_video.w, background_video.h)
#         elif self == Position.IN_EDGE_BOTTOM_RIGHT:
#             position_tuple = (background_video.w - (video.w / 2), background_video.h - (video.h / 2))
#         elif self == Position.BOTTOM_RIGHT:
#             position_tuple = (background_video.w - video.w, background_video.h - video.h)
#         # BOTTOM
#         elif self == Position.OUT_BOTTOM:
#             position_tuple = ((background_video.w / 2) - (video.w / 2), background_video.h)
#         elif self == Position.IN_EDGE_BOTTOM:
#             position_tuple = ((background_video.w / 2) - (video.w / 2), background_video.h - (video.h / 2))
#         elif self == Position.BOTTOM:
#             position_tuple = ((background_video.w / 2) - (video.w / 2), background_video.h - video.h)
#         # BOTTOM LEFT
#         elif self == Position.OUT_BOTTOM_LEFT:
#             position_tuple = (-video.w, background_video.h)
#         elif self == Position.IN_EDGE_BOTTOM_LEFT:
#             position_tuple = (-(video.w / 2), background_video.h - (video.h / 2))
#         elif self == Position.BOTTOM_LEFT:
#             position_tuple = (0, background_video.h - video.h)
#         # LEFT
#         elif self == Position.OUT_LEFT:
#             position_tuple = (-video.w, (background_video.h / 2) - (video.h / 2))
#         elif self == Position.IN_EDGE_LEFT:
#             position_tuple = (-(video.w / 2), (background_video.h / 2) - (video.h / 2))
#         elif self == Position.LEFT:
#             position_tuple = (0, (background_video.h / 2) - (video.h / 2))
#         # TOP LEFT
#         elif self == Position.OUT_TOP_LEFT:
#             position_tuple = (-video.w, -video.h)
#         elif self == Position.IN_EDGE_TOP_LEFT:
#             position_tuple = (-(video.w / 2), -(video.h / 2))
#         elif self == Position.TOP_LEFT:
#             position_tuple = (0, 0)

#         # HALF POSITIONS
#         elif self == Position.HALF_TOP:
#             position_tuple = (background_video.w / 2 - video.w / 2, background_video.h / 4 - video.h / 2)
#         elif self == Position.HALF_RIGHT:
#             position_tuple = (3 * background_video.w / 4 - video.w / 2, background_video.h / 2 - video.h / 2)
#         elif self == Position.HALF_BOTTOM:
#             position_tuple = (background_video.w / 2 - video.w / 2, 3 * background_video.h / 4 - video.h / 2)
#         elif self == Position.HALF_LEFT:
#             position_tuple = (background_video.w / 4 - video.w / 2, background_video.h / 2 - video.h / 2)
#         elif self == Position.HALF_TOP_RIGHT:
#             position_tuple = (3 * background_video.w / 4 - video.w / 2, background_video.h / 4 - video.h / 2)
#         elif self == Position.HALF_BOTTOM_RIGHT:
#             position_tuple = (3 * background_video.w / 4 - video.w / 2, 3 * background_video.h / 4 - video.h / 2)
#         elif self == Position.HALF_BOTTOM_LEFT:
#             position_tuple = (background_video.w / 4 - video.w / 2, 3 * background_video.h / 4 - video.h / 2)
#         elif self == Position.HALF_TOP_LEFT:
#             position_tuple = (background_video.w / 4 - video.w / 2, background_video.h / 4 - video.h / 2)

#         # QUADRANT CORNERS
#         elif self == Position.QUADRANT_1_TOP_RIGHT_CORNER:
#             position_tuple = (background_video.w / 2 - video.w, 0)
#         elif self == Position.QUADRANT_1_BOTTOM_LEFT_CORNER:
#             position_tuple = (0, background_video.h / 2 - video.h)
#         elif self == Position.QUADRANT_1_BOTTOM_RIGHT_CORNER:
#             position_tuple = (background_video.w / 2 - video.w, background_video.h / 2 - video.h)
#         elif self == Position.QUADRANT_2_BOTTOM_LEFT_CORNER:
#             position_tuple = (background_video.w / 2, background_video.h / 2 - video.h)
#         elif self == Position.QUADRANT_2_BOTTOM_RIGHT_CORNER:
#             position_tuple = (background_video.w - video.w, background_video.h / 2 - video.h)
#         elif self == Position.QUADRANT_2_TOP_LEFT_CORNER:
#             position_tuple = (background_video.w / 2, 0)
#         elif self == Position.QUADRANT_3_BOTTOM_LEFT_CORNER:
#             position_tuple = (background_video.w / 2, background_video.h - video.h)
#         elif self == Position.QUADRANT_3_TOP_LEFT_CORNER:
#             position_tuple = (background_video.w / 2, background_video.h / 2)
#         elif self == Position.QUADRANT_3_TOP_RIGHT_CORNER:
#             position_tuple = (background_video.w - video.w, background_video.h / 2)
#         elif self == Position.QUADRANT_4_BOTTOM_RIGHT_CORNER:
#             position_tuple = (background_video.w / 2 - video.w, background_video.h - video.h)
#         elif self == Position.QUADRANT_4_TOP_LEFT_CORNER:
#             position_tuple = (0, background_video.h / 2)
#         elif self == Position.QUADRANT_4_TOP_RIGHT_CORNER:
#             position_tuple = (background_video.w / 2 - video.w, background_video.h / 2)

#         # RANDOMs
#         elif self == Position.RANDOM_INSIDE:
#             return randchoice(Position.inside_positions_as_list()).get_moviepy_position(video, background_video, do_normalize)
#         elif self == Position.RANDOM_OUTSIDE:
#             return randchoice(Position.outside_positions_as_list()).get_moviepy_position(video, background_video, do_normalize)

#         if do_normalize:
#             position_tuple = (
#                 Math.normalize(position_tuple[0], NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE),
#                 Math.normalize(position_tuple[1], NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE)
#             )

#         return position_tuple
    



#     def as_video_position(self) -> 'VideoPosition':
#         """
#         Turn the provided 'position' to an instance of the
#         VideoPosition class, setting it as a corner type and
#         nor normalized with the coordinate that corresponds
#         to the provided 'position' in a default scenario of
#         1920x1080 dimensions.
#         """
#         return Position.to_video_position(self)
    
#     @staticmethod
#     def to_moviepy_position(position: 'Position'):
#         """
#         Turn the provided 'position' to a real moviepy position
#         by applying a default scenario of 1920x1080 dimensions.
#         """
#         position = Position.to_enum(position)

#         return position.get_moviepy_position()
    
#     @staticmethod
#     def to_video_position(position: 'Position') -> 'VideoPosition':
#         """
#         Turn the provided 'position' to an instance of the
#         VideoPosition class, setting it as a corner type and
#         nor normalized with the coordinate that corresponds
#         to the provided 'position' in a default scenario of
#         1920x1080 dimensions.
#         """
#         # Do not move import (cyclic import issue)
#         from yta_multimedia.video.edition.effect.moviepy.position.objects.video_position import VideoPosition, CoordinateType

#         position = Position.to_moviepy_position(position)

#         return VideoPosition(position[0], position[1], CoordinateType.CORNER)
    
#     # TODO: What about the other methods to get normalized
#     # values to be able to work with GraphicRateFunction (?)