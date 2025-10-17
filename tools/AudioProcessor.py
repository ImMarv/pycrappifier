import subprocess
from tools.CommandBuilder import CommandBuilder
from tools.helpers.FFmpegUtils import FFmpegUtils

class AudioProcessor:
    """Class to handle audio processing using ffmpeg commands built by CommandBuilder."""
    def __init__(self, cmd="ffmpeg"):
        self.command_builder = CommandBuilder(cmd=cmd)

    def compress(self, input_file, output_file, bitrate=None, sample_rate=None, mono=False, overwrite=True):
        if isinstance(bitrate, str) and bitrate.endswith('k'):
            try:
                bitrate = int(bitrate[:-1]) * 1000  # Convert '128k' to 128000
            except ValueError as exc:
                raise ValueError("Bitrate must be an integer followed by 'k', e.g. '128k'") from exc
        command = self.command_builder.build(
            input_file,
            output_file,
            bitrate=bitrate,
            sample_rate=sample_rate,
            mono=mono,
            overwrite=overwrite
        )
        subprocess.run(command, check=True)

    def get_audio_info(self, input_file):
        return FFmpegUtils.getAudioInfo(input_file)