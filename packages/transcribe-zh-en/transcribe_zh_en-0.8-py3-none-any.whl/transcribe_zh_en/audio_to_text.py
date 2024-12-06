from faster_whisper import WhisperModel, BatchedInferencePipeline

# Function to transcribe English audio
async def transcribe_english_audio(audio_path, output_srt_path, model_size="Large-v2", device="cpu"):
    model = WhisperModel(model_size, device=device, compute_type="float16")
    batched_model = BatchedInferencePipeline(model=model)
    
    segments, _ = batched_model.transcribe(audio_path, batch_size=16, word_timestamps=True, vad_filter=True)

    with open(output_srt_path, 'w') as srt_file:
        srt_counter = 1
        for segment in segments:
            for word in segment.words:
                srt_file.write(f"{srt_counter}\n")
                srt_file.write(f"{word.start:.2f} --> {word.end:.2f}\n")
                srt_file.write(f"{word.word}\n\n")
                srt_counter += 1

# Function to transcribe Chinese audio
async def transcribe_chinese_audio(audio_path, output_srt_path, model_size="Large-v2", device="cpu"):
    model = WhisperModel(model_size, device=device, compute_type="float16")
    batched_model = BatchedInferencePipeline(model=model)
    
    segments, _ = batched_model.transcribe(audio_path, batch_size=16, word_timestamps=True, vad_filter=True)

    with open(output_srt_path, 'w') as srt_file:
        srt_counter = 1
        for segment in segments:
            for word in segment.words:
                srt_file.write(f"{srt_counter}\n")
                srt_file.write(f"{word.start:.2f} --> {word.end:.2f}\n")
                srt_file.write(f"{word.word}\n\n")
                srt_counter += 1