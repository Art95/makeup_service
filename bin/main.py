import argparse
import makeup_service


def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('--video-source', default=0)
    parse.add_argument('--flip-image', default=True)
    parse.add_argument('--hair-color', nargs="*", type=int, default=[230, 50, 20])
    parse.add_argument('--upper-lip-color', nargs="*", type=int, default=[20, 70, 180])
    parse.add_argument('--lower-lip-color', nargs="*", type=int, default=[20, 70, 180])

    return parse.parse_args()


def main():
    args = parse_args()

    video_source = args.video_source
    colors = [args.hair_color, args.upper_lip_color, args.lower_lip_color]
    flip = args.flip_image

    makeup_service.apply_makeup(video_source=video_source, colors=colors, flip=flip)


if __name__ == '__main__':
    main()
