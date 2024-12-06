from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.position import Position
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate import Coordinate
from yta_multimedia.video.edition.effect.moviepy.position.move.move_linear_position_effect import MoveLinearPositionEffect
from moviepy.Clip import Clip
from moviepy import concatenate_videoclips
from typing import Union
from random import randrange


class SlideRandomlyEffect(Effect):
    """
    Slides from outside the screen to the specified position
    (which is the center by default), stays there and goes
    away through the opposite side.
    """
    def apply(self, video: Clip, position: Union[Position, Coordinate, tuple] = Position.CENTER) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlurEffect.apply, locals(), ['video'])
        background_video = ClipGenerator.get_default_background_video()

        return self.apply_over_video(video, background_video, position)
    
    def apply_over_video(self, video: Clip, background_video: Clip, position: Union[Position, Coordinate] = Position.CENTER) -> Clip:
        random_position = get_in_and_out_positions_as_list()

        movement_time = background_video.duration / 6
        stay_time = background_video.duration / 6 * 4

        effect = concatenate_videoclips([   
            MoveLinearPositionEffect().apply_over_video(
                video.with_subclip(0, movement_time),
                background_video.with_subclip(0, movement_time),
                random_position[0],
                position
            ),
            # TODO: This can be replaced by a StayAtPositionEffect
            # but the result is the same actually
            MoveLinearPositionEffect().apply_over_video(
                video.with_subclip(movement_time, movement_time + stay_time),
                background_video.with_subclip(movement_time, movement_time + stay_time),
                position,
                position
            ),
            MoveLinearPositionEffect().apply_over_video(
                video.with_subclip(movement_time + stay_time, video.duration),
                background_video.with_subclip(movement_time + stay_time, video.duration),
                position,
                random_position[1]
            )
        ])

        return effect


def get_in_and_out_positions_as_list():
    """
    Returns a list of 2 elements containing the out edge from which
    the video will come into the screen, and the opposite edge to get
    out of the screen. This has been created to animate a random slide
    transition effect. The possibilities are horizontal, diagonal and
    vertical linear sliding transitions. The first element in the list
    is the initial position and the second one, the final position. 
    """
    rnd = randrange(0, 8)
    
    if rnd == 0:
        positions = [Position.OUT_RIGHT, Position.OUT_LEFT]
    elif rnd == 1:
        positions = [Position.OUT_TOP, Position.OUT_BOTTOM]
    elif rnd == 2:
        positions = [Position.OUT_BOTTOM, Position.OUT_TOP]
    elif rnd == 3:
        positions = [Position.OUT_TOP_LEFT, Position.OUT_BOTTOM_RIGHT] 
    elif rnd == 4:
        positions = [Position.OUT_TOP_RIGHT, Position.OUT_BOTTOM_LEFT]
    elif rnd == 5:
        positions = [Position.OUT_BOTTOM_LEFT, Position.OUT_TOP_RIGHT]
    elif rnd == 6:
        positions = [Position.OUT_BOTTOM_RIGHT, Position.OUT_TOP_LEFT]
    elif rnd == 7:
        positions = [Position.OUT_LEFT, Position.OUT_RIGHT]

    return positions


# from yta_multimedia.video.edition.effect.moviepy.position.move.move_linear_position_effect import MoveLinearPositionEffect
# from yta_multimedia.video.edition.effect.moviepy.position.static.stay_at_position_moviey_effect import StayAtPositionMoviepyEffect
# from yta_multimedia.video.position import Position
# from yta_multimedia.video.edition.effect.moviepy.position.objects.moviepy_slide import MoviepySlide
# from yta_multimedia.video import concatenate_videos
# from moviepy import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, VideoClip
# from typing import Union


# class SlideRandomPositionMoviepyEffect(BasePositionMoviepyEffect):
#     """
#     Effect of appearing from TOP, TOP_LEFT, BOTTOM, RIGHT, etc. 
#     staying at the center, and dissapearing from the opposite 
#     edge. This animation will spend 1/6 of the time in the 
#     entrance, 4/6 of the time staying at the center, and 1/6 of 
#     the time in the exit.
#     """

#     @classmethod
#     def apply(cls, video: Union[str, VideoFileClip, VideoClip, CompositeVideoClip, ImageClip, ColorClip]):
#         return cls.apply_over_video(video, BasePositionMoviepyEffect.get_black_background_clip(video.duration))

#     @classmethod
#     def apply_over_video(cls, video: Union[str, VideoFileClip, VideoClip, CompositeVideoClip, ImageClip, ColorClip], background_video: Union[str, VideoFileClip, VideoClip, CompositeVideoClip, ImageClip, ColorClip]):
#         background_video = BasePositionMoviepyEffect.prepare_background_clip(background_video, video)

#         random_position = MoviepySlide.get_in_and_out_positions_as_list()

#         movement_time = background_video.duration / 6
#         stay_time = background_video.duration / 6 * 4

#         effect = concatenate_videos([   
#             MoveLinearPositionEffect().apply_over_video(video.with_subclip(0, movement_time), background_video.with_subclip(0, movement_time), random_position[0], Position.CENTER),
#             StayAtPositionMoviepyEffect(video.with_subclip(movement_time, movement_time + stay_time)).apply_over_video(background_video.with_subclip(movement_time, movement_time + stay_time), Position.CENTER),
#             MoveLinearPositionEffect().apply_over_video(video.with_subclip(movement_time + stay_time, video.duration), background_video.with_subclip(movement_time + stay_time, video.duration), Position.CENTER, random_position[1])
#         ])

#         return effect