import subprocess
import threading
import os
import re
import time
from typing import Callable, Optional
from app.utils.ffmpeg_check import get_ffmpeg_path, check_ffprobe

class MediaConverter:
    def __init__(self):
        self.ffmpeg = get_ffmpeg_path()
        self.ffprobe = "ffprobe" if check_ffprobe() else None
        self.stop_event = threading.Event()
        self.current_process = None

    def get_duration(self, file_path):
        if not self.ffprobe:
            return 0
        try:
            cmd = [
                self.ffprobe,
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                file_path
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            return float(res.stdout.strip())
        except:
            return 0

    def convert(self, input_path, output_path, options, progress_callback: Optional[Callable[[float, str], None]] = None):
        """
        Convert media file.
        options: dict with 'format', 'args' (string of extra args)
        """
        if not self.ffmpeg:
            raise FileNotFoundError("FFmpeg not found")

        self.stop_event.clear()

        # Build Command
        cmd = [self.ffmpeg, "-y", "-i", input_path]

        # Add options
        # E.g. format is handled by output filename extension usually, but we can force codecs
        # If options has 'args', split and add
        if options.get('args'):
            cmd.extend(options['args'].split())

        cmd.append(output_path)

        duration = self.get_duration(input_path)

        # Run
        try:
            # We need to capture stderr to parse progress
            self.current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace' # Handle potential encoding issues
            )

            # Read stderr for progress
            while True:
                if self.stop_event.is_set():
                    self.current_process.kill()
                    break

                line = self.current_process.stderr.readline()
                if not line and self.current_process.poll() is not None:
                    break

                if line:
                    # Parse time=HH:MM:SS.ms
                    # Example: time=00:00:05.12
                    match = re.search(r"time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})", line)
                    if match and duration > 0:
                        h, m, s, ms = map(int, match.groups())
                        current_sec = h*3600 + m*60 + s + ms/100
                        percent = min(0.99, current_sec / duration)
                        if progress_callback:
                            progress_callback(percent, f"Converting... {int(percent*100)}%")

            if self.current_process.returncode == 0:
                if progress_callback: progress_callback(1.0, "Conversion Complete")
                return True
            else:
                if not self.stop_event.is_set():
                    # Only raise if not manually stopped
                    raise Exception("FFmpeg error")
                return False

        except Exception as e:
            if progress_callback: progress_callback(0, f"Error: {e}")
            raise e
        finally:
            self.current_process = None

    def cancel(self):
        self.stop_event.set()
        if self.current_process:
            self.current_process.terminate()
