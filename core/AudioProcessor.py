import subprocess
from core.CommandBuilder import CommandBuilder
from core.helpers.FFmpegUtils import FFmpegUtils
from .dto.command import Command

class AudioProcessor:
    """Class to handle audio processing using ffmpeg commands built by CommandBuilder."""
    def __init__(self, cmd="ffmpeg"):
        self.command_builder = CommandBuilder(cmd=cmd)

    def compress(self, command: Command, *args, **kwargs):
        """Compress audio file with specified parameters.

        Accepts either a Command DTO or raw Command constructor args.
        """
        if not isinstance(command, Command):
            command = Command(command, *args, **kwargs)
        elif args or kwargs:
            raise ValueError("When passing a Command object, do not pass additional arguments")

        if isinstance(command.bitrate, str) and command.bitrate.endswith('k'):
            try:
                command.bitrate = int(command.bitrate[:-1]) * 1000  # Convert '128k' to 128000
            except ValueError as exc:
                raise ValueError("Bitrate must be an integer followed by 'k', e.g. '128k'") from exc

        built_command = self.command_builder.build(command)
        subprocess.run(built_command, check=True)

    def get_audio_info(self, input_file):
        """Retrieve audio file information using FFmpegUtils."""
        return FFmpegUtils.getAudioInfo(input_file)