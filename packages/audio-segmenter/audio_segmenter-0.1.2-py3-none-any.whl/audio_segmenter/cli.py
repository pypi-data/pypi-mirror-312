import argparse
import sys
from .segmenter import AudioSegmenter

def main():
    """
    Command-line interface for AudioSegmenter
    """
    parser = argparse.ArgumentParser(description='Advanced Audio Segmentation Tool')
    
    # Required argument
    parser.add_argument('input_file', type=str, help='Path to input audio file')
    
    # Optional arguments with defaults
    parser.add_argument('-m', '--method', 
                        choices=['time', 'auto'], 
                        default='time', 
                        help='Segmentation method (default: time)')
    
    parser.add_argument('-a', '--algorithm', 
                        choices=['silence-based'], 
                        default='silence-based', 
                        help='Segmentation algorithm for auto method (default: silence-based)')
    
    parser.add_argument('-d', '--duration', 
                        type=int, 
                        default=30, 
                        help='Segment duration for time-based method (default: 30 seconds)')
    
    parser.add_argument('-sr', '--silence-ratio', 
                        type=float, 
                        default=0.2, 
                        help='Silence detection threshold (default: 0.2)')
    
    parser.add_argument('-sd', '--silence-duration', 
                        type=float, 
                        default=0.2, 
                        help='Minimum silence duration (default: 0.2 seconds)')
    
    parser.add_argument('-min', '--min-duration', 
                        type=float, 
                        default=0.2, 
                        help='Minimum segment duration (default: 0.2 seconds)')
    
    parser.add_argument('-o', '--output-folder', 
                        type=str, 
                        default='output_segments', 
                        help='Output folder for segments (default: output_segments)')
    
    parser.add_argument('-j', '--json-path', 
                        type=str, 
                        default='segments_metadata.json', 
                        help='Path to save metadata JSON (default: segments_metadata.json)')

    # Parse arguments
    args = parser.parse_args()

    # Create AudioSegmenter instance
    segmenter = AudioSegmenter()

    try:
        # Call segment_audio method with parsed arguments
        segmenter.segment_audio(
            audio_file_path=args.input_file,
            method=args.method,
            algorithm=args.algorithm,
            duration=args.duration,
            silence_ratio=args.silence_ratio,
            silence_duration=args.silence_duration,
            min_duration=args.min_duration,
            output_folder=args.output_folder,
            metadata_file_path=args.json_path
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()