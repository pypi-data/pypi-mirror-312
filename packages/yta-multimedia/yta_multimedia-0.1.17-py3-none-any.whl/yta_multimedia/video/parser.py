from yta_general_utils.file.checker import FileValidator
from yta_general_utils.file.enums import FileType
from yta_general_utils.file.filename import filename_is_type
from yta_general_utils.programming.parameter_validator import PythonValidator
from moviepy import VideoFileClip, CompositeVideoClip, ColorClip, ImageClip, ImageSequenceClip, VideoClip, AudioClip, concatenate_audioclips
from moviepy.Clip import Clip
from typing import Union


class VideoParser:
    """
    Class to simplify the way we parse video parameters.
    """
    @classmethod
    def to_moviepy(cls, video: Union[str, VideoFileClip, CompositeVideoClip, ColorClip, ImageClip], do_include_mask: bool = False, do_check_duration: bool = False, size: Union[tuple, None] = (1920, 1080)):
        """
        This method is a helper to turn the provided 'video' to a moviepy
        video type. If it is any of the moviepy video types specified in
        method declaration, it will be returned like that. If not, it will
        be load as a VideoFileClip if possible, or will raise an Exception
        if not.

        The 'do_include_mask' parameter includes the mask in the video if
        True value provided. The 'do_check_duration' parameter checks and
        updates the real video duration to fix a bug in moviepy lib.
        """
        if not video:
            raise Exception('No "video" provided.')
        
        # TODO: Maybe check if subclass of VideoClip
        if not PythonValidator.is_string(video) and not PythonValidator.is_instance(video, [VideoFileClip, CompositeVideoClip, ColorClip, ImageClip, ImageSequenceClip, VideoClip]):
            raise Exception('The "video" parameter provided is not a valid type. Check valid types in method declaration.')
        
        if PythonValidator.is_string(video):
            if not filename_is_type(video, FileType.VIDEO):
                raise Exception('The "video" parameter provided is not a valid video filename.')
            
            if not FileValidator.file_is_video_file(video):
                raise Exception('The "video" parameter is not a valid video file.')
            
            video = VideoFileClip(video, has_mask = do_include_mask)

        if do_check_duration:
            # We need to fix an existing bug in moviepy lib
            # see https://github.com/Zulko/moviepy/issues/1826
            video = verify_and_update_duration(video)

        # TODO: This below just adds a mask attribute but
        # without fps and empty, so it doesn't make sense
        # if do_include_mask and not video.mask:
        #     video = video.add_mask()

        # TODO: This should not be done here as it is unexpected
        # but also something needed as we need to make sure any
        # video has the expected size
        # if size:
        #     # This is here because of cyclic import
        #     from yta_multimedia.video.edition.resize import resize_video

        #     if not PythonValidator.is_tuple(size) or len(size) != 2:
        #         raise Exception(f'The provided "size" parameter "{str(size)}" is not a valid size.')
            
        #     # Adjust the strategy if needed
        #     video = resize_video(video, size)
        
        return video

# TODO: Maybe this has been solved with the new
# moviepy 2.0.0 version, I'm not sure but I will
# be using it not during the next weeks to check
# TODO: Very important method here below
def verify_and_update_duration(video: VideoClip):
    """
    Try to subclip the provided 'video' with the last
    frames detected by moviepy and check if the duration
    is the real one and updates it if not. This method
    returns the video updated to the its new duration.

    Moviepy has a bug in which some videos are detected
    larger than they actually are, and that makes the 
    software fails when trying to work with all those 
    wrong detected videos.

    When trying to subclip a moviepy video, the system
    will fail when the 't_start' parameter is larger or
    equal to the actual video duration (not the one
    detected by moviepy), so we are using that slow
    function to detect the real duration and updating
    the video accordingly.
    """
    frame_time = 1 / video.fps

    for frame_number in reversed(range(video.n_frames)):
        try:
            # Could I found the issue that the 'concatenate_videos'
            # method solves (?) Maybe I have to make a small
            # substraction, but here I am working with the 't_start'
            # not the 't_end'. I keep this comment here as an
            # advice. I hope it is not needed.
            real_duration = frame_number * frame_time
            video.with_subclip(real_duration, 9999)
            # 't_start' can't be the last frame but the penultimate
            # so the real duration is one 'frame_time' later
            real_duration += frame_time
            break
        except:
            pass

    video = video.with_subclip(0, real_duration)
    # Fix audio that can be problematic also
    video = video.with_audio(verify_and_update_audio_duration(video.audio))

    return video

# TODO: Move this to a better place
# TODO: This below is needed but it is apparently not
# working at all, because I still have the problem 
# when trying to combine two videos and the bugged 
# one (and fixed by this method) is one of them.
# Maybe new moviepy version fixes this (?)
def verify_and_update_audio_duration(audio: AudioClip):
    from yta_multimedia.audio.parser import AudioParser
    from yta_multimedia.audio.sound.generation.sound_generator import SoundGenerator

    audio = AudioParser.to_audiofileclip(audio)

    expected_duration = audio.duration

    cont = 0
    try:
        # TODO: Simplify this, it is too slow, maybe second
        # by second and later, when found the error, retry
        # frame by frame but in shorter range
        for _ in audio.iter_frames():
            cont += 1
    except:
        #print(f'Exception when {str(cont)} index.')
        actual_duration = cont / audio.fps
        rest_duration = expected_duration - actual_duration

        print(f'fixed audio with {str(rest_duration)} silence')
        
        audio = concatenate_audioclips([audio.with_subclip(0, cont), SoundGenerator.create_silence_audio(rest_duration)])

    return audio
