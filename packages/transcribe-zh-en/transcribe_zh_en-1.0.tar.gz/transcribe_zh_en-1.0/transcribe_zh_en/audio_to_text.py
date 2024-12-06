import logging
import subprocess
import os
from paddlespeech.cli.asr.infer import ASRExecutor

# Initialize logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Function to get the duration of an audio file in seconds using ffprobe
def get_audio_duration(audio_file: str) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_file,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stderr = result.stderr.decode()
    if stderr:
        logger.error(f"FFprobe stderr: {stderr}")
    try:
        return float(result.stdout.decode().strip())
    except ValueError:
        logger.error("Could not convert FFprobe output to float")
        return 0.0

# Function to split audio based on the maximum duration (180 seconds)
def split_audio(audio_file, max_duration=180):
    total_duration = get_audio_duration(audio_file)
    
    # If the audio is longer than the maximum allowed duration, split it
    if total_duration > max_duration:
        num_chunks = int(total_duration // max_duration) + 1
        chunk_files = []
        for i in range(num_chunks):
            start_time = i * max_duration
            chunk_file = f"{audio_file}_part_{i}.wav"
            subprocess.run([ 
                "ffmpeg", "-i", audio_file, "-ss", str(start_time),
                "-t", str(max_duration), "-ac", "1", "-ar", "16000", "-acodec", "pcm_s16le", chunk_file
            ])
            chunk_files.append(chunk_file)
        return chunk_files
    else:
        # If the audio is short enough, no need to split
        return [audio_file]

# Function to process each audio chunk with ASR and return transcribed text
def asr_to_zh(audio_path, lang, device="cpu"):
    # First split based on duration (180 seconds max)
    audio_chunks = split_audio(audio_path)

    full_text = ""
    for audio_chunk in audio_chunks:
        try:
            # Process each chunk with ASR
            asr_executor = ASRExecutor()
            result = asr_executor(audio_file=audio_chunk, lang=lang, device=device, sample_rate=16000)
            full_text += result.strip() + " "
            
            # Clean up chunk after processing
            os.remove(audio_chunk)
        except Exception as e:
            logger.error(f"Error processing chunk {audio_chunk}: {e}")
    
    return full_text