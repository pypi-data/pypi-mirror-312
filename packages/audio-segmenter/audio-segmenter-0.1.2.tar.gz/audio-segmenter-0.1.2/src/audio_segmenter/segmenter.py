import os
import json
import logging
import numpy as np
from pydub import AudioSegment
from typing import List, Dict, Optional, Union

class AudioSegmenter:
    def __init__(self, logs_dir: Optional[str] = None):
        """
        Initialize AudioSegmenter with logging configuration.
        
        :param logs_dir: Directory for log files. If None, creates a 'logs' directory in the current script's directory.
        """
        self.logs_dir = logs_dir or os.path.join(os.path.dirname(__file__), 'logs')
        
        # Create logs directory if it doesn't exist
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
        
        # Configure logging
        logging.basicConfig(
            filename=os.path.join(self.logs_dir, 'audio_segmenter.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def _log_message(self, level: str, message: str):
        """
        Log messages to the log file.
        
        :param level: Log level (info, error, warning, debug)
        :param message: Message to log
        """
        if level == "info":
            logging.info(message)
        elif level == "error":
            logging.error(message)
        elif level == "warning":
            logging.warning(message)
        else:
            logging.debug(message)
    
    def load_audio(self, input_path: str) -> AudioSegment:
        """
        Load an audio file.
        
        :param input_path: Path to the audio file
        :return: Loaded AudioSegment
        """
        try:
            self._log_message("info", f"Audio file loading started: {input_path}")
            audio = AudioSegment.from_file(input_path)
            self._log_message("info", f"Audio file successfully loaded: {input_path}")
            return audio
        except FileNotFoundError:
            self._log_message("error", f"Audio file not found: {input_path}")
            raise
        except Exception as e:
            self._log_message("error", f"Error loading audio file: {str(e)}")
            raise
    
    def time_based_segmentation(self, audio: AudioSegment, duration: int) -> List[Dict[str, Union[str, float]]]:
        """
        Segment audio based on fixed time intervals.
        
        :param audio: Loaded AudioSegment
        :param duration: Segment duration in seconds
        :return: List of segment metadata
        """
        try:
            segments = []
            for i in range(0, len(audio), duration * 1000):
                start_time = i / 1000
                end_time = min((i + duration * 1000) / 1000, len(audio) / 1000)
                segments.append({
                    "segment_id": f"segment_{len(segments) + 1}",
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration": end_time - start_time,
                    "file_path": f"segment_{len(segments) + 1}.mp3"
                })
            
            self._log_message("info", f"Time-based segmentation completed with {len(segments)} segments.")
            return segments
        except Exception as e:
            self._log_message("error", f"Error during time-based segmentation: {str(e)}")
            raise
    
    def _detect_silence(self, audio_data: np.ndarray, frame_rate: int, silence_ratio: float, silence_duration: float) -> List[tuple]:
        """
        Detect silent regions in the audio.
        
        :param audio_data: Audio data as numpy array
        :param frame_rate: Audio frame rate
        :param silence_ratio: Silence threshold ratio
        :param silence_duration: Minimum silence duration
        :return: List of silent points
        """
        try:
            mean_amplitude = np.mean(np.abs(audio_data))
            silence_threshold = mean_amplitude * silence_ratio
            min_silence_length = int(silence_duration * frame_rate)
            silent_points = np.where(np.abs(audio_data) < silence_threshold)[0]
            
            split_points = []
            current_silence_length = 0

            for i in range(1, len(silent_points)):
                if silent_points[i] == silent_points[i - 1] + 1:
                    current_silence_length += 1
                else:
                    if current_silence_length >= min_silence_length:
                        split_points.append((silent_points[i - current_silence_length], silent_points[i - 1]))
                    current_silence_length = 0

            if current_silence_length >= min_silence_length:
                split_points.append((silent_points[-current_silence_length], silent_points[-1]))

            self._log_message("info", "Silence detection completed.")
            return split_points
        except Exception as e:
            self._log_message("error", f"Error during silence detection: {str(e)}")
            raise
    
    def silence_based_segmentation(self, audio: AudioSegment, silence_ratio: float, silence_duration: float, min_duration: float = 0.2) -> List[Dict[str, Union[str, float]]]:
        """
        Segment audio based on silence detection.
        
        :param audio: Loaded AudioSegment
        :param silence_ratio: Silence threshold ratio
        :param silence_duration: Minimum silence duration
        :param min_duration: Minimum segment duration
        :return: List of segment metadata
        """
        try:
            segments = []
            frame_rate = audio.frame_rate
            n_channels = audio.channels
            audio_data = np.array(audio.get_array_of_samples())

            if n_channels == 2:
                audio_data = audio_data[::2]

            split_points = self._detect_silence(audio_data, frame_rate, silence_ratio, silence_duration)
            
            voice_segments = self._get_voice_segments(split_points, frame_rate, audio_data)
            
            for i, segment in enumerate(voice_segments):
                start_time, end_time = segment
                segment_duration = end_time - start_time
                
                if segment_duration >= min_duration:
                    segments.append({
                        "segment_id": f"segment_{len(segments) + 1}",
                        "start_time": start_time,
                        "end_time": end_time,
                        "duration": segment_duration,
                        "file_path": f"segment_{len(segments) + 1}.mp3"
                    })

            self._log_message("info", "Silence-based segmentation completed.")
            return segments
        except Exception as e:
            self._log_message("error", f"Error during silence-based segmentation: {str(e)}")
            raise
    
    def _get_voice_segments(self, split_points: List[tuple], frame_rate: int, audio_data: np.ndarray) -> List[tuple]:
        """
        Extract voice segments from detected silence points.
        
        :param split_points: Silence points
        :param frame_rate: Audio frame rate
        :param audio_data: Audio data as numpy array
        :return: List of voice segment time ranges
        """
        try:
            voice_segments = []
            if split_points:
                if split_points[0][0] != 0:
                    voice_segments.append((0, split_points[0][0]))
                for i in range(len(split_points) - 1):
                    voice_segments.append((split_points[i][1], split_points[i + 1][0]))
                if split_points[-1][1] != len(audio_data):
                    voice_segments.append((split_points[-1][1], len(audio_data)))
            else:
                voice_segments.append((0, len(audio_data)))

            self._log_message("info", "Voice segments extraction completed.")
            return [(start / frame_rate, end / frame_rate) for start, end in voice_segments]
        except Exception as e:
            self._log_message("error", f"Error during voice segment extraction: {str(e)}")
            raise
    
    def validate_segments(self, segments: List[Dict[str, Union[str, float]]]) -> bool:
        """
        Validate segment start and end times.
        
        :param segments: List of segment metadata
        :return: Whether segments are valid
        """
        try:
            for segment in segments:
                if segment["start_time"] >= segment["end_time"]:
                    self._log_message("warning", f"Invalid segment: {segment['segment_id']}")
                    return False
            self._log_message("info", "All segments validated successfully.")
            return True
        except Exception as e:
            self._log_message("error", f"Error during segment validation: {str(e)}")
            raise
    
    def save_segments(self, audio: AudioSegment, segments: List[Dict[str, Union[str, float]]], output_folder: str):
        """
        Save audio segments to files.
        
        :param audio: Original AudioSegment
        :param segments: List of segment metadata
        :param output_folder: Path to save segment files
        """
        try:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
                self._log_message("info", f"Output folder created: {output_folder}")

            for segment in segments:
                segment_path = os.path.join(output_folder, segment['file_path'])
                start_time = segment['start_time'] * 1000
                end_time = segment['end_time'] * 1000
                audio_segment = audio[start_time:end_time]
                audio_segment.export(segment_path, format="mp3")
                self._log_message("info", f"Segment saved: {segment_path}")
        except Exception as e:
            self._log_message("error", f"Unexpected error saving segments: {str(e)}")
            raise
    
    def generate_metadata(self, input_path: str, segments: List[Dict[str, Union[str, float]]]) -> Dict:
        """
        Generate metadata for audio segments.
        
        :param input_path: Original audio file path
        :param segments: List of segment metadata
        :return: Metadata dictionary
        """
        try:
            metadata = {
                "audio_file": os.path.basename(input_path),
                "duration_seconds": sum([seg['duration'] for seg in segments]),
                "segments": segments
            }
            self._log_message("info", "Segment metadata generated.")
            return metadata
        except Exception as e:
            self._log_message("error", f"Error generating metadata: {str(e)}")
            raise
    
    def segment_audio(
        self, 
        audio_file_path: str, 
        method: str = 'time', 
        algorithm: str = 'silence-based',
        duration: int = 30, 
        silence_ratio: float = 0.2, 
        silence_duration: float = 0.2, 
        min_duration: float = 0.2, 
        output_folder: str = "output_segments", 
        metadata_file_path: str = "segments_metadata.json"
    ):
        """
        Main method to segment audio files with flexible options.
        
        :param audio_file_path: Path to the audio file
        :param method: Segmentation method ('time' or 'auto')
        :param algorithm: Auto segmentation algorithm
        :param duration: Time-based segment duration
        :param silence_ratio: Silence detection threshold
        :param silence_duration: Minimum silence duration
        :param min_duration: Minimum segment duration
        :param output_folder: Output folder for segments
        :param metadata_file_path: Path to save metadata JSON
        """
        try:
            # Load audio file
            audio = self.load_audio(audio_file_path)

            # Perform segmentation
            if method == "time":
                segments = self.time_based_segmentation(audio, duration)
            elif method == "auto" and algorithm == 'silence-based':
                segments = self.silence_based_segmentation(
                    audio, 
                    silence_ratio=silence_ratio, 
                    silence_duration=silence_duration,
                    min_duration=min_duration
                )
            else:
                raise ValueError("Invalid segmentation method or parameters.")

            # Validate segments
            if not self.validate_segments(segments):
                raise ValueError("Invalid segment assets.")

            # Generate metadata
            metadata = self.generate_metadata(audio_file_path, segments)

            # Save segments
            self.save_segments(audio, segments, output_folder)

            # Save metadata to JSON
            with open(metadata_file_path, "w") as metadata_file:
                json.dump(metadata, metadata_file, indent=4)
                self._log_message("info", f"Segment metadata saved to {metadata_file_path}")

            print(f"Segmentation completed successfully. Metadata: {metadata_file_path}")

        except Exception as e:
            self._log_message("error", f"An error occurred: {str(e)}")
            print(f"An error occurred: {str(e)}")