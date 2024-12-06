from yta_multimedia.video.edition.effect.moviepy.position.objects.base_position_moviepy_effect import BasePositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.objects.video_position import VideoPosition
from yta_multimedia.video.position import Position
from yta_multimedia.video.edition.effect.moviepy.position.utils.position import get_moviepy_position
from yta_multimedia.video.edition.effect.moviepy.position.utils.shake import shake_movement
from yta_general_utils.file.checker import FileValidator
from moviepy import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, VideoClip
from typing import Union


class ShakeAtPositionMoviepyEffect(BasePositionMoviepyEffect):
    """
    Effect of shaking the given 'video' when initialized in a specific
    position given (if given as parameter when applying) or randomly
    generated (inside the bounds according to the also provided
    'background_video' dimensions).
    """
    @classmethod
    def apply(cls, video: VideoClip, position: Union[Position, VideoPosition] = Position.RANDOM_INSIDE):
        """
        Applies the effect to the 'video' provided when initializing this
        effect class, and puts the video over a static black background
        image of 1920x1080.
        """
        return cls.apply_over_video(video, BasePositionMoviepyEffect.get_black_background_clip(video.duration), position)

    @classmethod
    def apply_over_video(cls, video: VideoClip, background_video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip], position: Union[Position, VideoPosition] = Position.RANDOM_INSIDE):
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
        #background_video = super().prepare_background_clip(background_video)
        background_video = BasePositionMoviepyEffect.prepare_background_clip(background_video)

        BasePositionMoviepyEffect.validate_position(position)

        position = get_moviepy_position(video, background_video, position)

        # TODO: I could modify this to accept the 'rate_func' and apply it
        effect = video.with_position(lambda t: shake_movement(t, position[0], position[1])).with_start(0).with_duration(video.duration)
        
        return CompositeVideoClip([
            background_video,
            effect
        ])