from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.frames.video_frame import VideoFrame
from yta_general_utils.programming.parameter_validator import PythonValidator
from moviepy import VideoClip, concatenate_videoclips
from typing import Union


class VideoHandler:
    """
    Class created to simplify and encapsulate the working process
    with moviepy videos.
    """
    @staticmethod
    def invert_video(video: Union[str, VideoClip]):
        """
        Invert the received 'video' (that must be a moviepy 
        mask or normal clip) and return it inverted as a
        VideoClip. If the provided 'video' is a mask, this 
        will be also a mask.

        If the 'clip' provided is a mask clip, remember to
        set it as the new mask of your main clip.

        This inversion is a process in which the numpy array
        values of each frame are inverted by substracting the
        highest value. If the frame is an RGB frame with 
        values between 0 and 255, it will be inverted by 
        doing 255 - X on each frame pixel value. If it is
        normalized and values are between 0 and 1 (it is a 
        mask clip frame), by doing 1 - X on each mask frame
        pixel value.
        """
        video = VideoParser.to_moviepy(video)

        mask_frames = [VideoFrame(frame).inverted() for frame in video.iter_frames()]

        return VideoClip(lambda t: mask_frames[int(t * video.fps)], is_mask = video.is_mask).with_fps(video.fps)
    

# TODO: Maybe this has been solved with the new
# moviepy 2.0.0 version
def concatenate_videos(videos: list[VideoClip]):
    """
    This is a fix for an issue with the moviepy 
    concatenate_videoclips method that seems to be
    failing with the concatenated video duration
    because of the floating point.

    Check this: 
    https://github.com/Zulko/moviepy/issues/646
    """
    if not PythonValidator.is_list(videos):
        videos = [videos]

    videos = [VideoParser.to_moviepy(video) for video in videos]

    # We do the moviepy concatenation
    video = concatenate_videoclips(videos)

    # We make a small substraction due to a float point
    # error when concatenating videos, to make sure we
    # use a value valid to be considered as the last
    # frame. The subclip method uses a (a, b] interval
    # to look for the frame, so as our .duration could
    # be a little greater than b, it would go for the
    # next interval and fail because of no frame 
    # available, we make sure we provide a value in the
    # range.
    video = video.with_subclip(0, video.duration - (1 / video.fps / 100000))

    return video