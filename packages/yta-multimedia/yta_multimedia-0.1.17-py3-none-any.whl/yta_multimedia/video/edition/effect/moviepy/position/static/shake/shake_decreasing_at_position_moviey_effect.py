from yta_multimedia.video.edition.effect.moviepy.position.objects.base_position_moviepy_effect import BasePositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.objects.video_position import VideoPosition
from yta_multimedia.video.position import Position
from yta_multimedia.video.edition.effect.moviepy.position.utils.position import get_moviepy_position
from yta_multimedia.video.edition.effect.moviepy.position.utils.shake import shake_decreasing_movement
from yta_general_utils.file.checker import FileValidator
from yta_general_utils.programming.parameter_validator import PythonValidator
from moviepy import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip
from typing import Union


class ShakeDecreasingAtPositionMoviepyEffect(BasePositionMoviepyEffect):
    """
    Effect of shaking the given 'video' when initialized in a specific
    position given (if given as parameter when applying) or randomly
    generated (inside the bounds according to the also provided
    'background_video' dimensions). The shaking process is increasing
    by time.
    """
    def apply(self, position: Union[Position, VideoPosition] = Position.RANDOM_INSIDE):
        """
        Applies the effect to the 'video' provided when initializing this
        effect class, and puts the video over a static black background
        image of 1920x1080.
        """
        background_video = ColorClip((1920, 1080), [0, 0, 0], duration = self.video.duration)

        return self.apply_over_video(background_video, position)

    def apply_over_video(self, background_video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip], position: Union[Position, VideoPosition] = Position.RANDOM_INSIDE):
        """
        This effect will make the 'self.video' shake in the 
        provided 'position' (or in a random one in the screen).

        Applies the effect on the video used when instantiating the
        effect, but applies the effect by placing it over the 
        'background_video' provided in this method (the 
        'background_video' will act as a background video for the 
        effect applied on the initial video).

        This method will set the video used when instantiating the
        effect as the most important, and its duration will be 
        considered as that. If the 'background_video' provided 
        has a duration lower than the original video, we will
        loop it to reach that duration. If the video is shorter
        than the 'background_video', we will crop the last one
        to fit the original video duration.
        """
        if not background_video:
            raise Exception('No "background_video" provided.')
        
        if isinstance(background_video, str):
            if not FileValidator.file_is_video_file:
                raise Exception('Provided "background_video" is not a valid video file.')
            
            background_video = VideoFileClip(background_video)

        if not PythonValidator.is_instance(position, [Position, VideoPosition]):
            raise Exception('Provided "position" is not a valid Position or VideoPosition instance.')

        background_video = super().process_background_video(background_video)

        position = get_moviepy_position(self.video, background_video, position)

        effect = self.video.with_position(lambda t: shake_decreasing_movement(t, position[0], position[1])).with_start(0).with_duration(self.video.duration)

        return CompositeVideoClip([
            background_video,
            effect
        ])