from yta_multimedia.video.edition.effect.moviepy.position.objects.base_position_moviepy_effect import BasePositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.objects.video_position import VideoPosition
from yta_multimedia.video.position import Position
from yta_multimedia.video.edition.effect.moviepy.position.utils.position import get_moviepy_position
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionSetPosition
from moviepy import VideoFileClip, CompositeVideoClip, ImageClip, VideoClip, ColorClip
from typing import Union


class CirclesAtPositionMoviepyEffect(BasePositionMoviepyEffect):
    """
    Effect of moving in circles surrounding the specified position.

    TODO: Implement the radius parameter option
    """

    @classmethod
    def apply(cls, video: Union[str, VideoFileClip, VideoClip, CompositeVideoClip, ImageClip, ColorClip], position: Union[Position, VideoPosition] = Position.RANDOM_INSIDE):
        return cls.apply_over_video(video, BasePositionMoviepyEffect.get_black_background_clip(video.duration), position)

    @classmethod
    def apply_over_video(cls, video: Union[str, VideoFileClip, VideoClip, CompositeVideoClip, ImageClip, ColorClip], background_video: Union[str, VideoFileClip, VideoClip, CompositeVideoClip, ImageClip, ColorClip], position: Union[Position, VideoPosition] = Position.RANDOM_INSIDE):
        BasePositionMoviepyEffect.validate_position(position)

        background_video = BasePositionMoviepyEffect.prepare_background_clip(background_video, video)

        position = get_moviepy_position(video, background_video, position)

        effect = video.with_position(lambda t: TFunctionSetPosition.circles_at_position(t, position[0], position[1])).with_start(0).with_duration(video.duration)

        return CompositeVideoClip([
            background_video,
            effect
        ])