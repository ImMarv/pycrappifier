# Enshittify

This project is a simple Python application for compressing audio files using ffmpeg. It features a basic graphical user interface (GUI) built with PyQt and a main Python file for core operations.

## Features
- Select audio files to compress
- Choose compression settings
- Start compression using ffmpeg
- Simple and intuitive PyQt-based UI

## Requirements
- Python 3.8+
- ffmpeg (must be installed and available in PATH)
- PyQt5

## Setup
1. Install Python 3.8 or newer.
2. Install dependencies:
   ```sh
   pip install PyQt5
   ```
3. Ensure ffmpeg is installed and accessible from the command line.

## Usage
- Run `main.py` to start the application:
  ```sh
  python main.py
  ```

## File Structure
- `main.py` - Self-explanatory
- `ui.py` - PyQt UI code
- `ffmpeg_bitrate.py` - Main logic of the program.

