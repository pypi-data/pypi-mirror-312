from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from yta_multimedia.video.edition.effect.moviepy.objects import MoviepyArgument
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionResize
from yta_multimedia.video.edition.effect.moviepy.video_effect import MoviepyVideoEffect
from yta_general_utils.math.rate_functions import RateFunction
from moviepy import CompositeVideoClip, VideoFileClip, ImageClip, VideoClip, ColorClip
from typing import Union


# TODO: The use of this method must be by using the
# new MoviepyWith, not VideoEffect that will be
# removed in a near future version.
# TODO: Rename it, as it is making zoom but in an
# specific an static position, so it should be
# something like ZoomInPlaceEffect
class ZoomVideoEffect(VideoEffect):
    """
    Creates a Zoom effect in the provided video.
    """
    @classmethod
    def apply(cls, video: Union[str, VideoFileClip, VideoClip, CompositeVideoClip, ImageClip, ColorClip], zoom_start: float, zoom_end: float, rate_func: type = RateFunction.linear):
        """
        Apply the effect on the provided 'video'.

        :param float zoom_start: The zoom at the start of the video, where a 1 is no zoom, a 0.8 is a zoom out of 20% and 1.1 is a zoom in of a 10%.

        :param float zoom_end: The zoom at the end of the video, where a 1 is no zoom, a 0.8 is a zoom out of 20% and 1.1 is a zoom in of a 10%.

        :param type rate_func: The rate function to apply in the animation effect. Must be one of the methods available in the RateFunction class.
        """
        return MoviepyVideoEffect.apply(video, MoviepyArgument(zoom_start, zoom_end, TFunctionResize.resize_from_to, rate_func))

    # TODO: 'apply_over_video' here (?)