import logging
from itertools import islice
from pathlib import Path
from typing import Iterable

from nos.common.io import VideoReader
from PIL import Image
from pytube import Playlist, YouTube

logger = logging.getLogger(__name__)


DEFAULT_DOWNLOAD_DIR = Path.home() / "data"
DEFAULT_DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


def yt_playlist(playlist_url: str, start: int = 0, end: int = 100) -> list:
    """Get all URLs from a YouTube playlist"""
    playlist = Playlist(playlist_url)
    # This forces pytube to fetch all the video URLs in the playlist
    playlist._video_regex = None
    return list(playlist.video_urls)[start:end]


def yt_download(url: str, output_directory: str = DEFAULT_DOWNLOAD_DIR, height: int = 720):
    # Convert output directory to Path object and ensure it exists
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)

    # Create YouTube object
    yt = YouTube(url)

    # Filter the streams to mp4 and sort by resolution
    stream = yt.streams.filter(file_extension="mp4", progressive=True).order_by("resolution").desc().first()

    # If a specific height is requested, try to honor that, but fall back to the highest available if not found
    if height:
        preferred_stream = yt.streams.filter(res=f"{height}p", file_extension="mp4", progressive=True).first()
        if preferred_stream:
            stream = preferred_stream

    # Prepare filename
    path = output_directory / f"{yt.video_id}.mp4"

    # Download video if file does not exist
    if not path.exists():
        logger.info(f"Downloading '{yt.title}' to '{path}'")
        stream.download(output_path=output_directory, filename=path.name)
    else:
        logger.info(f"File '{path}' already exists, skipping download.")

    return str(path)


def yt_sample_video(url: str, start: int = 0, end: int = None, skip: int = 300) -> Iterable[Image.Image]:
    # Download the video
    logger.info(f"Downloading video ... [url={url}]")
    path = yt_download(url)

    # Extract frames from the video
    video = VideoReader(path)
    assert len(video) > 0, f"Invalid video length: {len(video)}"
    frames = islice(VideoReader(path), start, end, skip)
    logger.info(f"Processing video ... [video={video}]")
    for frame in frames:
        yield Image.fromarray(frame).convert("RGB")
