from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.frames.video_frame import VideoFrame
from yta_multimedia.video.edition.duration import set_video_duration
from yta_general_utils.programming.parameter_validator import NumberValidator
from typing import Union
from moviepy import VideoClip
from moviepy.Clip import Clip

import numpy as np


class VideoHandler:
    """
    Class created to simplify and encapsulate some basic
    calculations related to a video, its frames and more
    properties.
    """
    video: Clip = None
    """
    The video to handle.
    """
    _frames_number: int = None
    _frame_duration: float = None
    _frame_time_moments: list = None

    def __init__(self, video: Clip):
        video = VideoParser.to_moviepy(video)

        self.video = video

    @property
    def frames_number(self):
        """
        The number of frames of the video, calculated with 
        this formula:

        frames_number = fps * duration + frame_duration * 0.1

        We make the final addition to make sure the number is
        exact due to integer parsing of floating points.
        """
        if self._frames_number is None:
            self._frames_number = int(self.video.fps * self.video.duration + self.frame_duration * 0.1)

        return self._frames_number
    
    @property
    def frame_duration(self):
        """
        The frame duration of the video, calculated with this
        formula:

        frame_duration = duration / (duration * fps)
        """
        if self._frame_duration is None:
            self._frame_duration = self.video.duration / (self.video.duration * self.video.fps)

        return self._frame_duration
    
    @property
    def frame_time_moments(self):
        """
        The list of frame time moments (ts) to build the clip
        frame by frame. This can be used to precalculate video
        positions, resizes or rotations, in order to apply them
        later one by one, frame by frame, reading directly form
        an array.

        You can access to an specific time moment by using the
        'get_frame_time_moment' method.
        """
        if self._frame_time_moments is None:
            self._frame_time_moments = np.linspace(0, self.video.duration, int(self.video.duration * self.video.fps))

        return self._frame_time_moments
    
        """
        Remember to access to each frame using the next operaiton:
        rotations[int((t + frame_duration * 0.1) // frame_duration)]
        """
    
    def get_frame_number_by_time_moment(self, t: float):
        """
        Return the frame number (from 0 to the last one)
        according to the frame time moment 't' provided.

        The frame number is calculated with the next formula:

        rotations[int((t + frame_duration * 0.1) // frame_duration)]

        The '+ frame_duration * 0.1' part is needed to make sure
        each frame access is different (due to floating points
        errors)
        """
        if not NumberValidator.is_positive_number(t):
            raise Exception(f'The provided "t" parameter "{str(t)}" is not a valid frame time moment.')
        
        return int((t + self.frame_duration * 0.1) // self.frame_duration)
        # TODO: What about looking for in in the array (?)
        # Maybe I don't find it because of floating points (?)

    # TODO: Maybe move this method to a VideoMaskInverter
    # class...
    def invert(self):
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
        mask_frames = [VideoFrame(frame).inverted() for frame in self.video.iter_frames()]

        return VideoClip(lambda t: mask_frames[int(t * self.video.fps)], is_mask = self.video.is_mask).with_fps(self.video.fps)
    
    def prepare_background_clip(self, background_video: Union[str, Clip]):
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
        background_video = VideoParser.to_moviepy(background_video)

        background_video = set_video_duration(background_video, self.video.duration)

        return background_video