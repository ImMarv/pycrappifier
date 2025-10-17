import shlex
import pytest
import os
import sys
# Ensure the project root is on sys.path so 'tools' can be imported when running tests directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.CommandBuilder import CommandBuilder

BASE_AUDIO = "base_audio.wav"

def testBuild_requires_input_file_raises_on_empty_string():
    cb = CommandBuilder()
    with pytest.raises(ValueError):
        cb.build("", "out.mp3")

def testBuild_requires_input_file_raises_on_none():
    cb = CommandBuilder()
    with pytest.raises(ValueError):
        cb.build(None, "out.mp3")

def testBuild_output_extension_appended_when_missing():
    cb = CommandBuilder()
    cmd = cb.build(BASE_AUDIO, "output_no_ext")
    assert cmd[-1] == "output_no_ext.mp3"

def testBuild_output_extension_not_appended_when_already_mp3_case_insensitive():
    cb = CommandBuilder()
    cmd = cb.build(BASE_AUDIO, "Song.MP3")
    assert cmd[-1] == "Song.MP3"

def testBuild_overwrite_flag_default_and_false():
    cb = CommandBuilder()
    cmd_default = cb.build(BASE_AUDIO, "out.mp3")
    assert cmd_default[1] == "-y"

    cmd_no_overwrite = cb.build(BASE_AUDIO, "out.mp3", overwrite=False)
    assert cmd_no_overwrite[1] == "-n"

def testBuild_bitrate_sample_rate_and_mono_flags_included_when_set():
    cb = CommandBuilder()
    cmd = cb.build(BASE_AUDIO, "out.mp3", bitrate=128, sample_rate=44100, mono=True)
    # expected sequence: cmd, overwrite, -i, input, (options...), output
    assert "-b:a" in cmd and "128" in cmd
    assert "-ar" in cmd and "44100" in cmd
    assert "-ac" in cmd and "1" in cmd

def testBuild_order_and_contents_exact():
    cb = CommandBuilder(cmd="ffmpeg")
    expected = [
        "ffmpeg",
        "-y",
        "-i",
        BASE_AUDIO,
        "-b:a",
        "192",
        "-ar",
        "48000",
        "-ac",
        "1",
        "final.mp3",
    ]
    actual = cb.build(BASE_AUDIO, "final", bitrate=192, sample_rate=48000, mono=True)
    assert actual == expected

def testBuild_str_returns_properly_quoted_command():
    cb = CommandBuilder()
    in_name = "in file.wav"
    out_name = "out file"
    cmd_list = cb.build(in_name, out_name, bitrate=64)
    cmd_str = cb.build_str(in_name, out_name, bitrate=64)
    # Build expected quoted string using shlex.quote on each part
    expected_str = " ".join(shlex.quote(str(p)) for p in cmd_list)
    assert cmd_str == expected_str
