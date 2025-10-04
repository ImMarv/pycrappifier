# This will include most of the logic behind the appplication
# There are two ways to do this, one involves using bash scripts and replacing them with python subprocess calls
# The other involves using python libraries (python-ffmpeg) to do the same thing without any boilerplate.
# I think I'll go with the first one.

import os
import subprocess
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from CommandBuilder import CommandBuilder

import ui

# Function to get the bitrate of an audio file using ffprobe
def get_bitrate(input_file):
    # Provide the full path to ffprobe if it's not in PATH, e.g. r"C:\ffmpeg\bin\ffprobe.exe"
    ffprobe_cmd = "ffprobe"
    cmd = [
        ffprobe_cmd,
        "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=bit_rate",
        "-of", "default=noprint_wrappers=1:nokey=1",
        input_file
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return int(result.stdout.strip())
    except FileNotFoundError:
        print("Error: ffprobe not found. Please ensure ffprobe is installed and in your PATH.")
        return None

# Function that gets the sample of an audio file using ffprobe
def get_sampleRate(inputFile):
    ffprobe_cmd = "ffprobe"
    cmd = [
        ffprobe_cmd,
        "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=sample_rate",
        "-of", "default=noprint_wrappers=1:nokey=1",
        inputFile
    ]

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return int(result.stdout.strip())
    except FileNotFoundError:
        print("Error: ffprobe not found. Please ensure ffprobe is installed and in your PATH.")
        return None

def getAudioInfo(inputFile):
    import json
    ffprobe_cmd = "ffprobe"
    cmd = [
        ffprobe_cmd,
        "-v", "error",
        "-show_entries", "format=filename,duration,bit_rate",
        "-show_entries", "stream=sample_rate,channels",
        "-of", "json",
        inputFile
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        info = json.loads(result.stdout)
        filename = info["format"]["filename"]
        duration = float(info["format"]["duration"])
        bitrate = int(info["format"]["bit_rate"])
        sampleRate = int(info["streams"][0]["sample_rate"])
        channels = int(info["streams"][0]["channels"])
        
        # Format duration as mm:ss
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        duration_str = f"{minutes}:{seconds:02d} min"
        
        # Format bitrate as kbps
        bitrate_kbps = bitrate // 1000
        
        # Format sample rate as kHz
        sample_rate_khz = sampleRate / 1000
        sample_rate_str = f"{sample_rate_khz:.1f} kHz"

        # Format filename to only include audio file name
        filename_str = os.path.basename(filename)
        
        return filename_str, duration_str, bitrate_kbps, sample_rate_str, channels
    except FileNotFoundError:
        print("Error: ffprobe not found. Please ensure ffprobe is installed and in your PATH.")
        return None
    except Exception as e:
        print(f"Error getting audio info: {e}")
        return None

def compress_audio(ui, input_file, output_file, bitrate=0, sample_rate=0, mono=False, overwrite=True):
    ffmpeg_cmd = "ffmpeg"

    # Set mono flag from UI
    mono = ui.stereoSwitch.isChecked()

    # Accept bitrate as string with 'k' suffix
    if isinstance(bitrate, str) and bitrate.endswith('k'):
        try:
            bitrate = int(bitrate[:-1]) * 1000  # Convert '128k' to 128000
        except ValueError:
            raise ValueError("Bitrate must be an integer followed by 'k', e.g. '128k'")
    elif isinstance(bitrate, int):
        if bitrate <= 0:
            raise ValueError("Bitrate must be a positive integer or a string like '128k'")
    else:
        raise ValueError("Bitrate must be a positive integer or a string like '128k'")
    
    sample_rate_arg = sample_rate if sample_rate and int(sample_rate) > 0 else None

    cmd = CommandBuilder().build(
        input_file=input_file,
        output_file=output_file,
        bitrate=bitrate,
        sample_rate=sample_rate,
        mono=mono,
        overwrite=overwrite
    )
    print("Running command:", CommandBuilder().build_str(
        input_file=input_file,
        output_file=output_file,
        bitrate=bitrate,
        sample_rate=sample_rate,
        mono=mono,
        overwrite=overwrite
    ))
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please ensure ffmpeg is installed and in your PATH.")
        raise
    except subprocess.CalledProcessError as e:
        print("Error compressing audio:", e.stderr)
        raise

# Connect UI signals to logic functions
def connect_signals(ui):
    ui.browse_btn.clicked.connect(lambda: browse_file(ui))
    ui.export_btn.clicked.connect(lambda: export_audio(ui))
    ui.bitrateSlider.valueChanged.connect(lambda: update_bitrate_label(ui))


# This should particularly get the file path.
def browse_file(ui):
    options = QFileDialog.Options()
    file_name, _ = QFileDialog.getOpenFileName(ui, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.flac);;All Files (*)", options=options)
    if file_name:
        ui.file_label.setText(file_name)
        ui.browse_btn.setEnabled(True)
        update_audio_settings(ui)

def update_audio_settings(ui):
    """Called when a file is selected"""
    audioInfo = None
    if ui.file_label.text():
        audioInfo = getAudioInfo(ui.file_label.text())
    else:
        ui.bitrateSlider.setMaximum(320)  # Max MP3 bitrate

    # Update labels based on file info
    if audioInfo:
        filename, duration, bitrate, sample_rate, channels = audioInfo

        # set slider max based on file bitrate
        ui.bitrateSlider.setMaximum(bitrate if bitrate else 320)

        # Update checkbox label based on channels
        if channels == 1:
            channels = "Mono"
            ui.stereoSwitch.setChecked(True)
        elif channels == 2:
            channels = "Stereo"
            ui.stereoSwitch.setChecked(False)

        details = f"{filename} - {duration} | {bitrate} kbps, {sample_rate} | {channels} channels"
        ui.audioDetailsLabel.setText(details)
    else:
        ui.audioDetailsLabel.setText("No file selected.")

    # Sample rate label always reflects dropdown selection
    ui.sample_rate_label.setText(f"Sample Rate: {ui.sampleRateCombo.currentText()} Hz")

    print(f"Bitrate slider value: {ui.bitrateSlider.value()} | Sample rate: {ui.sampleRateCombo.currentText()}")


def update_bitrate_label(ui):
    """Called whenever the bitrate slider value changes"""
    ui.bitrate_label.setText(f"Bitrate: {ui.bitrateSlider.value()}k")


def export_audio(ui):
    input_file = ui.file_label.text()
    if not input_file or input_file == "":
        print("No file selected")
        return

    setBitrate = ui.bitrateSlider.value()
    processed_file = input_file.rsplit('.', 1)[0] + "_processed.mp3"
    sample_rate = int(ui.sampleRateCombo.currentText())

    # Check if output file exists
    overwrite = True
    if os.path.exists(processed_file):
        msg = QMessageBox.question(
            ui,
            "File Exists",
            "Output file already exists. Overwrite?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if msg != QMessageBox.Yes:
            return QMessageBox.information(ui, "Not Exported", "The audio was not exported", QMessageBox.Ok)
        else:
            os.remove(processed_file if processed_file else None)

    try:
        # single compression pass — repeat removed
        compress_audio(ui, input_file, processed_file, f"{setBitrate}k", sample_rate, overwrite=overwrite)
        QMessageBox.information(ui, "Exported", "Audio exported successfully!", QMessageBox.Ok)
    except Exception as e:
        QMessageBox.critical(ui, "Error", f"Failed to export audio: {e}", QMessageBox.Ok)