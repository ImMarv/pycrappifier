import subprocess
import json
import os

class FFmpegUtils:
    @staticmethod
    def getAudioInfo(inputFile):
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=filename,duration,bit_rate",
            "-show_entries", "stream=sample_rate,channels",
            "-of", "json",
            inputFile
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        info = json.loads(result.stdout)

        return {
                "filename": os.path.basename(info["format"]["filename"]),
                "duration": float(info["format"]["duration"]),
                "bitrate": int(info["format"]["bit_rate"]),
                "sample_rate": int(info["streams"][0]["sample_rate"]),
                "channels": int(info["streams"][0]["channels"]),
            }
    