from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_general_utils.image.region import Coordinate as BaseCoordinate
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.programming.parameter_validator import PythonValidator
from moviepy import VideoClip


class CoordinateType(Enum):
    """
    Enum class to represent a coordinate type that 
    defines the way to make the calculations.
    """
    CORNER = 'corner'
    """
    The type of coordinate that represents the upper
    left corner of the object that uses the coordinate
    with this type.
    """
    CENTER = 'center'
    """
    The type of coordinate that represents the center of
    the object that uses the coordinate with this type.
    """

class Coordinate(BaseCoordinate):
    """
    Class to simplify the way to create a Coordinate
    instance by providing one of our pre-defined
    scene positions.
    """
    @staticmethod
    def from_position(position: 'Position'):
        """
        Initialize a VideoPosition with the given 'position' that
        will be computed according to our hypothetical default
        scenario of 1920x1080.
        """
        # Do not move import (cyclic import issue)
        from yta_multimedia.video.position import Position

        position: Position = Position.to_enum(position)

        position: VideoPosition = position.as_video_position(position)

        return BaseCoordinate(position.coordinate.x, position.coordinate.y)

class VideoPosition:
    """
    Coordinate to represent a the position in which we
    want to place a video. According to its 'type',
    we maybe want to put the center of the video in that
    position, or maybe the upper left corner.

    This is used to make easier the way we handle
    position parameters when trying to place a video
    in a specific place within a scene.

    TODO: Explain this better, please.
    """
    coordinate: Coordinate = None
    """
    The position (x, y) in which we want to position
    a video accoding to the 'type'.
    """
    type: CoordinateType = None
    """
    The type of the coordinate to be able to work
    properly with the 'x' and 'y' value and says
    what kind of representation is done by the
    coordinate.
    """

    @property
    def x(self):
        """
        Return the coordinate.x value.
        """
        return self.coordinate.x
    
    @property
    def y(self):
        """
        Return the coordinate.y value.
        """
        return self.coordinate.y

    def __init__(self, x: float, y: float, type: CoordinateType = CoordinateType.CORNER, is_normalized: bool = False):
        """
        Initialize a VideoPosition intance with raw values. If you
        have a Coordinate instance you can use the 
        'init_from_coordinate' method.
        """
        coordinate = Coordinate(x, y, is_normalized = is_normalized)

        self.coordinate = coordinate
        self.type = type

    def as_tuple(self):
        """
        Return the VideoPosition coordinate as a tuple (x, y).
        """
        return self.coordinate.as_tuple()
    
    def as_array(self):
        """
        Return the VideoPosition coordinate as an array [x, y].
        """
        return self.coordinate.as_array()
    
    @staticmethod
    def init_from_coordinate(coordinate: Coordinate, type: CoordinateType = CoordinateType.CORNER):
        """
        Initialize a VideoPosition instance by using a Coordinate
        instance.
        """
        if not PythonValidator.is_instance(coordinate, Coordinate):
            raise Exception('The provided "coordinate" parameter is not an instance of the Coordinate class.')
        
        type = CoordinateType.to_enum(type)

        return VideoPosition(coordinate.x, coordinate.y, type, coordinate.is_normalized)

    def get_position(self, video: VideoClip, background_video: VideoClip):
        """
        Translate the coordinate from our hypothetical
        1920x1080 scenario to the real one in which we
        are trying to place the provided 'video' in the
        also provided 'background_video' that could be
        different to our hypothetical scene.

        This method will return the coords (x, y) in
        which we need to place the 'video' to have its
        center in the desired ('x', 'y') position over
        the also provided 'background_video' by making
        some calculations as below.

        The coordinate is representing a specific 'x'
        and 'y' in a hypothetical scene of 1920x1080
        that could be pointing to the upper left corner
        or the center of a video according to the 'type'
        that has been set. With the provided 'video' and
        'background_video' we calculate the coord in 
        which the 'video' need to be positioned to
        actually fit the desired position as if it was
        the hypotethical 1920x1080 scenario.

        If we were representing the (100, 100) in that
        1920x1080 scenario and the new 'background_video'
        is 960x540, the new position would be (50, 50)
        because the scenario changed.
        """
        video = VideoParser.to_moviepy(video)
        background_video = VideoParser.to_moviepy(background_video)
        # The VideoPosition represents the position in a 1920x1080
        # scenario, so we need to translate this into reality
        default_background_video = ClipGenerator.get_default_background_video()

        x = (int) (background_video.w * self.coordinate.x / default_background_video.w)
        y = (int) (background_video.h * self.coordinate.y / default_background_video.h)

        if self.type == CoordinateType.CENTER:
            # The video is pretended to be centered in that
            # position so we recalculate it to fit that
            # condition
            x -= int(video.w / 2)
            y -= int(video.h / 2)

        return (x, y)