from makeup_service.server.face_makeup_facade import FaceMakeupFacade


def run(video_source, colors, save_to_file=False, out_file_path='transformed.avi', flip=True):
    face_makeup = FaceMakeupFacade()
    face_makeup.apply_makeup_on_video(video_source, colors, save_to_file, out_file_path, flip)
