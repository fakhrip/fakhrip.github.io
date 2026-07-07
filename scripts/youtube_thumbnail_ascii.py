#!/usr/bin/env python3
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path


DEFAULT_WIDTH = 33
DEFAULT_ROWS = 7
FRAME_CHAR = "█"
PIXEL_CHAR = "▀"


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Generate a fixed-size colored HTML thumbnail block for contents/youtube.html."
        ),
        epilog=(
            "examples:\n"
            "  python3 scripts/youtube_thumbnail_ascii.py _fva7bxc0dk\n"
            "  python3 scripts/youtube_thumbnail_ascii.py https://youtu.be/_fva7bxc0dk -o /tmp/thumb.html\n"
            "  python3 scripts/youtube_thumbnail_ascii.py thumbnail.jpg --crop 1200:700:40:10"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "source",
        help="YouTube video id, YouTube URL, or local image path.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Write output to this file instead of stdout.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_WIDTH,
        help=f"Visible thumbnail width inside the border. Default: {DEFAULT_WIDTH}.",
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=DEFAULT_ROWS,
        help=f"Visible thumbnail height inside the border. Default: {DEFAULT_ROWS}.",
    )
    parser.add_argument(
        "--crop",
        help=(
            "Optional ffmpeg crop expression, for example 1200:700:40:10. "
            "By default the full thumbnail is used."
        ),
    )
    parser.add_argument(
        "--no-frame",
        action="store_true",
        help="Print only the colored thumbnail body, without the █ border.",
    )
    return parser.parse_args()


def extract_video_id(source):
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", source):
        return source

    patterns = [
        r"(?:youtube\.com/watch\?v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/embed/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/shorts/)([A-Za-z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, source)
        if match:
            return match.group(1)

    return None


def download_thumbnail(video_id, destination):
    urls = [
        f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
        f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
    ]

    last_error = None

    for url in urls:
        try:
            urllib.request.urlretrieve(url, destination)
            return destination
        except Exception as error:
            last_error = error

    raise RuntimeError(f"failed to download thumbnail for {video_id}: {last_error}")


def resolve_source(source, temp_dir):
    path = Path(source)

    if path.exists():
        return path

    video_id = extract_video_id(source)

    if not video_id:
        raise ValueError(
            "source must be an existing image path, a YouTube video id, or a YouTube URL"
        )

    return download_thumbnail(video_id, temp_dir / f"{video_id}.jpg")


def build_filter(width, rows, crop):
    filters = []

    if crop:
        filters.append(f"crop={crop}")

    filters.extend([f"scale={width}:{rows * 2}:flags=lanczos", "format=rgb24"])

    return ",".join(filters)


def read_rgb_pixels(image_path, width, rows, crop):
    ffmpeg = shutil.which("ffmpeg")

    if not ffmpeg:
        raise RuntimeError("ffmpeg is required but was not found in PATH")

    command = [
        ffmpeg,
        "-v",
        "error",
        "-i",
        str(image_path),
        "-vf",
        build_filter(width, rows, crop),
        "-f",
        "rawvideo",
        "-",
    ]

    return subprocess.check_output(command)


def pixel_at(rgb, width, x, y):
    index = (y * width + x) * 3
    return rgb[index], rgb[index + 1], rgb[index + 2]


def hex_color(pixel):
    red, green, blue = pixel
    return f"#{red:02x}{green:02x}{blue:02x}"


def render_thumbnail(rgb, width, rows, with_frame):
    lines = []
    border = FRAME_CHAR * (width + 4)

    if with_frame:
        lines.append(border)

    for row in range(rows):
        cells = []

        for column in range(width):
            top = pixel_at(rgb, width, column, row * 2)
            bottom = pixel_at(rgb, width, column, row * 2 + 1)
            cells.append(
                f'<span style="color:{hex_color(top)};'
                f'background-color:{hex_color(bottom)}">{PIXEL_CHAR}</span>'
            )

        line = "".join(cells)

        if with_frame:
            line = f"{FRAME_CHAR * 2}{line}{FRAME_CHAR * 2}"

        lines.append(line)

    if with_frame:
        lines.append(border)

    return "\n".join(lines)


def main():
    args = parse_args()

    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        source = resolve_source(args.source, temp_dir)
        rgb = read_rgb_pixels(source, args.width, args.rows, args.crop)
        output = render_thumbnail(rgb, args.width, args.rows, not args.no_frame)

    if args.output:
        Path(args.output).write_text(f"{output}\n")
    else:
        print(output)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
