class CommandBuilder:
    """A class to build the ffmpeg command with specified parameters."""
    def __init__(self, cmd="ffmpeg"):
        self.cmd = cmd

    def build(self, input_file, output_file, bitrate=0, sample_rate=0, mono=False, overwrite=True):
        # Ensure there is an input file
        if not input_file:
            raise ValueError("Input file must be specified.")
        
        # Ensure output_file ends with .mp3
        if not output_file.lower().endswith('.mp3'):
            output_file += ".mp3"
        overwrite_flag = "-y" if overwrite else "-n"

        built_cmd = [self.cmd]

        # Add overwrite flag
        built_cmd.append(overwrite_flag)

        # Add input file
        built_cmd.extend(["-i", input_file])

        # Include all audio options
        if bitrate > 0:
            built_cmd.extend(["-b:a", str(bitrate)])
        if sample_rate > 0:
            built_cmd.extend(["-ar", str(sample_rate)])
        if mono:
            built_cmd.extend(["-ac", "1"])
        
        # Add output file
        built_cmd.append(output_file)
        return built_cmd
    
    def build_str(self, *args, **kwargs):
        import shlex
        # safe, quoted string for logging/debugging
        cmd = self.build(*args, **kwargs)
        # ensure each part is a str (avoid TypeError on bytes/None)
        return " ".join(shlex.quote(str(part)) for part in cmd)