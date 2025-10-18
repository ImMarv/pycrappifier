import importlib
import json
import subprocess
from types import SimpleNamespace

import pytest


def _load_module():
    for name in ("pycrappifier.core.helpers.FFmpegUtils", "core.helpers.FFmpegUtils", "FFmpegUtils"):
        try:
            return importlib.import_module(name)
        except Exception:
            continue
    raise RuntimeError("Unable to import FFmpegUtils module")


def _proc(stdout):
    return SimpleNamespace(stdout=stdout, stderr="", returncode=0)


def test_get_audio_info_basic(monkeypatch):
    mod = _load_module()
    sample = {
        "format": {"filename": "C:/music/album/track.mp3", "duration": "123.45", "bit_rate": "128000"},
        "streams": [{"sample_rate": "44100", "channels": 2}],
    }
    monkeypatch.setattr(mod.subprocess, "run", lambda *a, **k: _proc(json.dumps(sample)))
    info = mod.FFmpegUtils.getAudioInfo("C:/music/album/track.mp3")
    assert info["filename"] == "track.mp3"
    assert info["duration"] == 123.45
    assert info["bitrate"] == 128000
    assert info["sample_rate"] == 44100
    assert info["channels"] == 2


def test_get_audio_info_handles_full_path_filename(monkeypatch):
    mod = _load_module()
    sample = {
        "format": {"filename": "/some/long/path/song.wav", "duration": "10", "bit_rate": "64000"},
        "streams": [{"sample_rate": "22050", "channels": 1}],
    }
    monkeypatch.setattr(mod.subprocess, "run", lambda *a, **k: _proc(json.dumps(sample)))
    info = mod.FFmpegUtils.getAudioInfo("/some/long/path/song.wav")
    assert info["filename"] == "song.wav"
    assert info["duration"] == 10.0
    assert info["bitrate"] == 64000
    assert info["sample_rate"] == 22050
    assert info["channels"] == 1


def test_get_audio_info_invalid_json_raises(monkeypatch):
    mod = _load_module()
    monkeypatch.setattr(mod.subprocess, "run", lambda *a, **k: _proc("not a json"))
    with pytest.raises(json.JSONDecodeError):
        mod.FFmpegUtils.getAudioInfo("anyfile")


def test_get_audio_info_subprocess_raises(monkeypatch):
    mod = _load_module()

    def _raise(*a, **k):
        raise subprocess.CalledProcessError(returncode=1, cmd="ffprobe")

    monkeypatch.setattr(mod.subprocess, "run", _raise)
    with pytest.raises(subprocess.CalledProcessError):
        mod.FFmpegUtils.getAudioInfo("anyfile")


def test_get_audio_info_missing_format_fields_raises(monkeypatch):
    mod = _load_module()
    # missing duration and bit_rate
    sample = {"format": {"filename": "a.mp3"}, "streams": [{"sample_rate": "48000", "channels": 2}]}
    monkeypatch.setattr(mod.subprocess, "run", lambda *a, **k: _proc(json.dumps(sample)))
    with pytest.raises(KeyError):
        mod.FFmpegUtils.getAudioInfo("a.mp3")


def test_get_audio_info_missing_stream_fields_raises(monkeypatch):
    mod = _load_module()
    # streams[0] missing sample_rate / channels
    sample = {"format": {"filename": "a.mp3", "duration": "1", "bit_rate": "1000"}, "streams": [{}]}
    monkeypatch.setattr(mod.subprocess, "run", lambda *a, **k: _proc(json.dumps(sample)))
    with pytest.raises(KeyError):
        mod.FFmpegUtils.getAudioInfo("a.mp3")