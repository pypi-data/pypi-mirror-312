from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.edition.duration import set_video_duration
from moviepy.Clip import Clip
from typing import Union


# TODO: Place this in another module, please. Extracted
# from BasePositionMoviepyEffect that has been removed.
def prepare_background_clip(background_video: Union[str, Clip], video: Union[str, Clip]):
        """
        Prepares the provided 'background_video' by modifying its duration to
        be the same as the provided 'video'. By default, the strategy is 
        looping the 'background_video' if the 'video' duration is longer, or
        cropping it if it is shorter. This method returns the background_clip
        modified according to the provided 'video'.

        This method will raise an Exception if the provided 'video' or the provided
        'background_video' are not valid videos.

        TODO: Add a parameter to be able to customize the extend or enshort
        background strategy.
        """
        VideoParser.to_moviepy(background_video)
        VideoParser.to_moviepy(video)

        background_video = set_video_duration(background_video, video.duration)

        return background_video