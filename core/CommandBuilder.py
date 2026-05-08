from .dto.command import Command


class CommandBuilder:
    """A class to build the ffmpeg command with specified parameters."""
    def __init__(self, cmd="ffmpeg"):
        self.cmd = cmd

    def build(self, command: Command):
        # Ensure there is an input file
        if not command.input_file:
            raise ValueError("Input file must be specified.")
        # Ensure output_file ends with .mp3
        output_file = command.output_file
        if not output_file.lower().endswith('.mp3'):
            output_file += ".mp3"
        overwrite_flag = "-y" if command.overwrite else "-n"

        built_cmd = [self.cmd]

        # Add overwrite flag
        built_cmd.append(overwrite_flag)

        # Add input file
        built_cmd.extend(["-i", command.input_file])

        # Include all audio options
        if command.bitrate > 0:
            built_cmd.extend(["-b:a", str(command.bitrate)])
        if command.sample_Rate > 0:
            built_cmd.extend(["-ar", str(command.sample_Rate)])
        if command.mono:
            built_cmd.extend(["-ac", "1"])
        if command.has_bitcrush:
            built_cmd.extend(["-af", "acrusher"])
        # Add bitcrush parameters if applicable
        if command.has_bitcrush:
            bitcrush_values = self._build_bitcrush_values(command)
            built_cmd[-1] += "=" + "".join(bitcrush_values)
        # Add output file
        built_cmd.append(output_file)
        print(built_cmd)
        return built_cmd

    def build_str(self, *args, **kwargs):
        import shlex
        # safe, quoted string for logging/debugging
        cmd = self.build(*args, **kwargs)
        # ensure each part is a str (avoid TypeError on bytes/None)
        return " ".join(shlex.quote(str(part)) for part in cmd)

    def _build_bitcrush_values(self, param: Command):
        return [
            str(param.level_in),
            ":",
            str(param.level_out),
            ":",
            str(param.bits),
            ":",
            str(param.mix),
            ":",
            str(param.sampling),
        ]
