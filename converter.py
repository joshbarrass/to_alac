import logging
import os
import subprocess
import tempfile

class ffmpegError(Exception):
    pass

class alacconvertError(Exception):
    pass

logger = logging.getLogger("to_alac.converter")

def convert(fp: str, out_dir: str = None, overwrite: bool = False):
    """Convert a single track to ALAC using alacconvert and ffmpeg"""
    if not os.path.isfile(fp):
        raise FileNotFoundError

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    if not os.path.isdir(out_dir):
        raise NotADirectoryError

    name, ext = os.path.splitext(os.path.basename(fp))
    src_dir = os.path.dirname(fp)
    if out_dir is None:
        out_dir = src_dir

    m4afile = os.path.join(out_dir, name + ".m4a")
    if not overwrite and os.path.exists(m4afile):
        raise FileExistsError

    with tempfile.TemporaryDirectory() as tmpd:
        wavfile = os.path.join(tmpd, name + ".wav")
        # create ffmpeg process
        args = ["ffmpeg", "-n", "-i", fp, "-f", "wav", wavfile]
        logger.debug("Converting to WAV")
        logger.debug(
            "ffmpeg command: \"{}\"".format("\" \"".join(args))
        )
        ffmpeg = subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # wait for ffmpeg and check it succeeded
        ffmpeg.wait()
        if ffmpeg.returncode != 0:
            raise ffmpegError("ffmpeg returned non-zero return code")
        logger.debug("ffmpeg exited normally")

        # convert with alacconvert to caf
        alacconvertPath = os.path.join(
            os.path.dirname(__file__), "alacconvert"
        )
        caffile = os.path.join(tmpd, name + ".caf")
        args = [alacconvertPath, wavfile, caffile]
        logger.debug("Converting to ALAC")
        logger.debug(
            "alacconvert command: \"{}\"".format("\" \"".join(args))
        )
        alacconvert = subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # wait for alacconvert
        alacconvert.wait()
        if alacconvert.returncode != 0:
            raise alacconvertError(
                "alacconvert returned non-zero return code"
            )
        logger.debug("alacconvert exited normally")

        # convert back via ffmpeg
        args = [
            "ffmpeg", "-y", "-i", fp, "-i", caffile, "-map", "1",
            "-acodec", "copy", "-map_metadata", "0",
            "-map_metadata:s:a", "0:s:a", m4afile
        ]
        logger.debug("Changing container to M4A")
        logger.debug(
            "ffmpeg command: \"{}\"".format("\" \"".join(args))
        )
        ffmpeg = subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        ffmpeg.wait()
        if ffmpeg.returncode != 0:
            raise ffmpegError("ffmpeg returned non-zero return code")
        logger.debug("ffmpeg exited normally")
