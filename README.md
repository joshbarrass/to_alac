# to_alac

to_alac is a helper script for converting to Apple Lossless Audio Codec (ALAC) using Apple's implementation of the codec. This is the reference encoder for the format, and has the widest media player compatibility. This script uses the reference encoder as-is, compiling it to a standalone binary and calling this binary from a helper script to provide its functionality. However, this encoder outputs CAF files, which are not as widely-supported. This script uses ffmpeg to copy the ALAC audio from this container into an M4A file, which is more widely-used.

# Installation

W.I.P.

# Usage

W.I.P.

# FAQ

## Why not just use ffmpeg?

It's true, ffmpeg does have its own ALAC implementation. In many cases, this implementation is perfectly fine and does not cause any problems. However, there are some cases where this implementation produces incorrect files. Many media players are able to play these without any problems, but some have problems. This can present in a number of different ways. One error I have encountered in the past is music playback on an iDevice stopping if the device was locked whilst playing one of ffmpeg's ALAC files. Another example occurs in Spotify for Desktop on Linux, which will not play FLAC files but will play ALAC files with the .m4a file extension. Many ALAC files created by ffmpeg show an incorrect duration and will refuse to play, whilst files created by Apple's encoder play without issue.

At the time of writing, ffmpeg does not include Apple's implementation as an encoder.

## Why not make use of the codec library instead of calling the binary?

This is something I am working on! The intention of this script is to provide a convenient method of encoding data to fill the void until I have a better encoder to replace it.
