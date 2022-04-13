import os
import subprocess
import tempfile

class ffmpegError(Exception):
    pass

class alacconvertError(Exception):
    pass

def convert(fp: str):
    """Convert a single track to ALAC using alacconvert and ffmpeg"""
    name, ext = os.path.splitext(os.path.basename(fp))
    src_dir = os.path.dirname(fp)
    with tempfile.TemporaryDirectory() as tmpd:
        wavfile = os.path.join(tmpd, name + ".wav")

        # create ffmpeg process
        args = ["ffmpeg", "-i", fp, "-f", "wav", wavfile]
        ffmpeg = subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # wait for ffmpeg and check it succeeded
        ffmpeg.wait()
        if ffmpeg.returncode != 0:
            raise ffmpegError("ffmpeg returned non-zero return code")

        # convert with alacconvert to caf
        alacconvertPath = os.path.join(
            os.path.dirname(__file__), "alacconvert"
        )
        caffile = os.path.join(tmpd, name + ".caf")
        args = [alacconvertPath, wavfile, caffile]
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

        # convert back via ffmpeg
        m4afile = os.path.join(src_dir, name + ".m4a")
        # TODO: check if exists
        args = [
            "ffmpeg", "-i", fp, "-i", caffile, "-map", "1", "-acodec",
            "copy", "-map_metadata", "0", "-map_metadata:s:a", "0:s:a",
            m4afile
        ]
        ffmpeg = subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        ffmpeg.wait()
        if ffmpeg.returncode != 0:
            raise ffmpegError("ffmpeg returned non-zero return code")
