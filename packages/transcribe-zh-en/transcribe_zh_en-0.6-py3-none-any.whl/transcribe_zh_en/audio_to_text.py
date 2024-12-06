from faster_whisper import WhisperModel

async def transcribe_english_audio(audio_path, output_srt_path, model_size="small", device="cpu"):
    """
    Transcribe audio to English text using the Faster-Whisper model and save as SRT.
    """
    model = WhisperModel(model_size, device, compute_type="float32")

    segments, _ = model.transcribe(audio_path, language="en", beam_size=5)

    with open(output_srt_path, 'a', encoding='utf-8') as f:
        for segment in segments:
            f.write(f"{segment.start} --> {segment.end}\n")
            f.write(f"{segment.text}\n\n")

    print(f"Transcription saved to {output_srt_path}")


async def transcribe_chinese_audio(audio_path, output_srt_path, model_size="small", device="cpu"):
    """
    Transcribe audio to Chinese text using the Faster-Whisper model and save as SRT.
    """
    model = WhisperModel(model_size, device, compute_type="float32")

    segments, _ = model.transcribe(audio_path, language="zh", beam_size=5)

    with open(output_srt_path, 'a', encoding='utf-8') as f:
        for segment in segments:
            f.write(f"{segment.start} --> {segment.end}\n")
            f.write(f"{segment.text}\n\n")

    print(f"Transcription saved to {output_srt_path}")