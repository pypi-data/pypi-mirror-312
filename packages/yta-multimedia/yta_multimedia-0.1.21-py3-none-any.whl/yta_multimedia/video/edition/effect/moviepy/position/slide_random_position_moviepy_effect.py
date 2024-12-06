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