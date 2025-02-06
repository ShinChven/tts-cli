import os
import json
import argparse

# For Azure Speech SDK
import azure.cognitiveservices.speech as speechsdk

def load_config():
    config_path = os.path.expanduser("~/.local/tts-cli/config.json")
    with open(config_path, "r") as f:
        return json.load(f)

def read_text_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ['.txt', '.md']:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    elif ext == '.pdf':
        from PyPDF2 import PdfReader
        text = ""
        with open(filepath, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        # Remove wrapped lines to form continuous sentences
        text = text.replace("-\n", "").replace("\n", " ")
        return text
    elif ext == '.doc':
        import subprocess
        result = subprocess.run(["antiword", filepath], stdout=subprocess.PIPE)
        return result.stdout.decode("utf-8")
    elif ext == '.docx':
        import docx
        text = []
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text.append(para.text)
        return "\n".join(text)
    else:
        raise Exception("Unsupported file format!")

def synthesize_azure(text, provider_config, output_file):
    speech_key = provider_config.get("speech_key")
    service_region = provider_config.get("service_region")
    voice_name = provider_config.get("voice")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = voice_name

    # Set output format if mp3 is required
    if provider_config.get("output_format", "wav") == "mp3":
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio16Khz128KBitRateMonoMp3
        )

    # Split text if exceeds max_length instead of truncating
    max_length = provider_config.get("max_text_length", 5000)
    if len(text) > max_length:
        print(f"Text length ({len(text)}) exceeds {max_length}, splitting into chunks.")
        import textwrap
        # Split text into chunks without breaking words
        def chunk_text(text, max_length):
            return textwrap.wrap(text, width=max_length, break_long_words=False, break_on_hyphens=False)
        chunks = chunk_text(text, max_length)
        total = len(chunks)
        base_audio = os.path.splitext(output_file)[0]
        chunk_files = []  # Track individual chunk audio files
        for i, chunk in enumerate(chunks, start=1):
            part_file = output_file.replace(".", f"_part{i}.")
            chunk_files.append(part_file)
            # Output each chunk's text to a file
            chunk_text_file = f"{base_audio}_part{i}-text.txt"
            with open(chunk_text_file, "w", encoding="utf-8") as f:
                f.write(chunk)
            print(f"Chunk {i} text saved to {chunk_text_file}")

            print(f"Synthesizing chunk {i}/{total} to {part_file}")
            audio_config = speechsdk.audio.AudioOutputConfig(filename=part_file)
            chunk_synth = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
            result = chunk_synth.speak_text_async(chunk).get()
            if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
                print(f"Error in chunk {i}: {getattr(result, 'error_details', 'No details available')}")
                raise Exception(f"Speech synthesis failed for chunk {i}")
            print(f"Chunk {i} saved to {part_file}")

        # Merge audio chunks using ffmpeg directly
        if len(chunk_files) > 1:
            import subprocess
            base_audio = os.path.splitext(output_file)[0]
            temp_list = f"{base_audio}_filelist.txt"
            with open(temp_list, "w", encoding="utf-8") as f:
                for file in chunk_files:
                    f.write(f"file '{os.path.abspath(file)}'\n")
            cmd = [
                "ffmpeg",
                "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", temp_list,
                "-c", "copy",
                output_file
            ]
            subprocess.run(cmd, check=True)
            print(f"Merged audio saved to {output_file}")
            os.remove(temp_list)
            # Remove temporary chunk audio files and corresponding text files
            for i, audio_file in enumerate(chunk_files, start=1):
                try:
                    os.remove(audio_file)
                    print(f"Removed temporary file {audio_file}")
                except OSError as e:
                    print(f"Error removing file {audio_file}: {e}")
                text_file = f"{base_audio}_part{i}-text.txt"
                try:
                    os.remove(text_file)
                    print(f"Removed temporary text file {text_file}")
                except OSError as e:
                    print(f"Error removing text file {text_file}: {e}")
    else:
        # Single chunk synthesis
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_text_async(text).get()
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Error details: {getattr(result, 'error_details', 'No details available')}")
            raise Exception("Speech synthesis failed")
        print(f"Audio saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Convert text files to speech audio.")
    parser.add_argument("file", help="Path to the input text file")
    args = parser.parse_args()

    filepath = args.file
    text = read_text_file(filepath)
    config = load_config()
    default_provider_key = config.get("default_provider")
    provider_conf = config.get("providers", {}).get(default_provider_key, {})
    provider_type = provider_conf.get("type")
    output_format = provider_conf.get("output_format", "wav")

    # Log current provider information including provider key
    print(f"Using provider key: {default_provider_key}, type: {provider_type}, output file type: {output_format}")

    base_name = os.path.splitext(filepath)[0]
    output_ext = f".{output_format}"
    output_file = base_name + output_ext

    # Output full text sent to TTS engine
    text_output_file = base_name + "-text.txt"
    with open(text_output_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Text saved to {text_output_file}")

    if provider_type == "azure":
        synthesize_azure(text, provider_conf, output_file)
    else:
        print("Provider not supported yet.")

if __name__ == "__main__":
    main()
