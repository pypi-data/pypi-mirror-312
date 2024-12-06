import os
import argparse
import subprocess
import asyncio
from transcribe_zh_en.audio_to_text import transcribe_english_audio, transcribe_chinese_audio
from concurrent.futures import ThreadPoolExecutor


# Check if the video has subtitles
def has_subtitles(video_path):
    try:
        probe = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 's', '-show_entries', 'stream=index', '-of', 'csv=p=0', video_path],
            capture_output=True, text=True
        )
        return bool(probe.stdout.strip())
    except subprocess.CalledProcessError:
        return False


# Detach subtitles from video
def detach_subtitles(input_video, output_subtitles):
    if has_subtitles(input_video):
        command = ['ffmpeg', '-i', input_video, '-map', '0:s:0', '-c', 'copy', output_subtitles]
        subprocess.run(command, check=True)
        print(f"Subtitles extracted to {output_subtitles}")
    else:
        print(f"No subtitles found in {input_video}")


# Detach audio from video
def detach_audio(input_video, output_audio, output_video_no_audio):
    try:
        # Extract audio and create video without audio
        subprocess.run(['ffmpeg', '-i', input_video, '-vn', '-acodec', 'libmp3lame', output_audio], check=True)
        subprocess.run(['ffmpeg', '-i', input_video, '-an', '-vcodec', 'copy', output_video_no_audio], check=True)
        print(f"Audio detached to {output_audio}")
        print(f"Video (without audio) saved to {output_video_no_audio}")
    except subprocess.CalledProcessError as e:
        print(f"Error during audio detachment: {e}")


# Transcribe audio to text with concurrency control
async def transcribe_audio(audio_paths, video_output_dir, stt_zh_flag, stt_en_flag, device, model_size, max_workers=1):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        tasks = [
            loop.run_in_executor(executor, transcribe_audio_single, audio_path, video_output_dir, stt_zh_flag, stt_en_flag, device, model_size)
            for audio_path in audio_paths
        ]
        await asyncio.gather(*tasks)


# Transcribe a single audio file
def transcribe_audio_single(audio_path, video_output_dir, stt_zh_flag, stt_en_flag, device, model_size):
    output_audio = os.path.join(video_output_dir, os.path.basename(audio_path))
    
    if os.path.exists(output_audio):
        if stt_zh_flag:
            output_stt_zh = os.path.join(video_output_dir, f"{os.path.basename(audio_path)}_zh.srt")
            asyncio.run(transcribe_chinese_audio(output_audio, output_stt_zh, model_size, device))

        if stt_en_flag:
            output_stt_en = os.path.join(video_output_dir, f"{os.path.basename(audio_path)}_en.srt")
            asyncio.run(transcribe_english_audio(output_audio, output_stt_en, model_size, device))


# Process each video
def process_video(video_path, processed_dir, detach_subtitles_flag, detach_audio_flag, stt_zh_flag, stt_en_flag, device="cpu", model_size="small", max_workers=5):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_output_dir = os.path.join(processed_dir, video_name)

    os.makedirs(video_output_dir, exist_ok=True)

    output_subtitles = os.path.join(video_output_dir, f"{video_name}_subtitles.srt")
    output_audio = os.path.join(video_output_dir, f"{video_name}_audio.mp3")
    output_video_no_audio = os.path.join(video_output_dir, f"{video_name}_no_audio.mp4")

    # Detach subtitles if flag is set
    if detach_subtitles_flag:
        detach_subtitles(video_path, output_subtitles)

    # Detach audio if flag is set
    if detach_audio_flag:
        detach_audio(video_path, output_audio, output_video_no_audio)

    # Handle transcription if audio exists
    if os.path.exists(output_audio):
        audio_paths = [output_audio]
        asyncio.run(transcribe_audio(audio_paths, video_output_dir, stt_zh_flag, stt_en_flag, device, model_size, max_workers))
    else:
        print(f"Audio file {output_audio} not found. Skipping transcription.")


def main():
    parser = argparse.ArgumentParser(description="Process videos with subtitles, audio detachment, and speech-to-text conversion.")
    
    parser.add_argument('--input-dir', required=True, help='Path to the directory containing original videos.')
    parser.add_argument('--output-dir', help='Path to the directory where processed videos will be saved.')
    parser.add_argument('--detach-subtitles', action='store_true', help='Detach subtitles from videos.')
    parser.add_argument('--detach-audio', action='store_true', help='Detach audio from videos.')

    parser.add_argument('--device', default='cpu', help='Device to use for inference (cpu or cuda).')
    parser.add_argument('--model-size', default='small', help='Model size for Faster-Whisper (small or large).')
    parser.add_argument('--max-workers', type=int, default=1, choices=range(1, 6), help='Number of concurrent transcription workers (1-5).')
    parser.add_argument('--speech-to-text-zh', action='store_true', help='Perform speech-to-text in Chinese.')
    parser.add_argument('--speech-to-text-en', action='store_true', help='Perform speech-to-text in English.')
    
    args = parser.parse_args()

    # If output directory is not provided, use the parent directory of input directory
    if not args.output_dir:
        args.output_dir = os.path.dirname(os.path.abspath(args.input_dir))
    
    # Process each video in the input directory
    for video_file in os.listdir(args.input_dir):
        video_path = os.path.join(args.input_dir, video_file)

        if video_file.lower().endswith('.mp4'):
            print(f"Processing video: {video_path}")
            process_video(video_path, args.output_dir, args.detach_subtitles, args.detach_audio, 
                          args.speech_to_text_zh, args.speech_to_text_en, args.device, args.model_size)


if __name__ == '__main__':
    main()