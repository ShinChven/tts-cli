# tts-cli

A CLI tool to synthesize voice from a text file or a URL using an AI API.

## Features
- Converts text files (.txt, .md, .pdf, .doc, .docx, .ppt, .pptx) into audio.
- Supports HTTP/HTTPS URLs for text extraction.
- Splits long texts into manageable chunks.
- Uses Azure Speech SDK for synthesis.
- Merges audio chunks seamlessly.

## Installation

Install directly from GitHub:
```bash
pip install git+https://github.com/ShinChven/tts-cli.git
```

## Upgrade

Upgrade the CLI using pip:
```bash
pip install --upgrade git+https://github.com/ShinChven/tts-cli.git
```

## Configuration

Create a configuration file at `~/.local/tts-cli/config.json`. Example:
```json
{
    "default_provider": "azure",
    "providers": {
        "azure": {
            "type": "azure",
            "speech_key": "YOUR_AZURE_SPEECH_KEY",
            "service_region": "YOUR_SERVICE_REGION",
            "voice": "YOUR_VOICE_NAME",
            "output_format": "wav"  // or "mp3"
        },
        "google": {
            "type": "google",
            "credentials_json": "path/to/your/google-credentials.json",
            "voice": "en-US-Journey-F",
            "output_format": "wav"  // or "mp3"
        }
    }
}
```

## Google Cloud Credentials Setup

To enable authentication for Google Cloud Text-to-Speech, use the Google Cloud CLI. Simply run:
```bash
gcloud init
gcloud auth application-default login
```
These commands will generate a credentials.json file and print out its file path. Add this path to your configuration file under the `credentials_json` field for the Google provider.

You can also switch the active Google Cloud project before generating credentials using:
```bash
gcloud config set project <project_id>
```
For more details, see [Google Cloud Authentication Documentation](https://cloud.google.com/text-to-speech/docs/authentication#client-libs).

## Usage

Supported input types:
- Local files: .txt, .md, .pdf, .doc, .docx, .ppt, .pptx
- Web URLs: Supports http and https URLs for text extraction.

Run the CLI with:
```bash
tts path/to/your/file.txt
```
Or directly via Python:
```bash
python -m tts_cli.main path/to/your/file.txt
```

### Additional Details

- When a URL is provided, the tool fetches the page content and automatically extracts the main article text.
- For long texts, the tool splits the content into chunks and merges the audio segments.
- Use the `-f` or `--force` flag to bypass confirmation prompts during multi-chunk synthesis.
- Use the `-t` or `--threads` flag to specify the number of threads for Google Cloud Text-to-Speech concurrent synthesis.
- Requires ffmpeg to merge audio chunks. Please install ffmpeg and ensure it is in your system PATH.
- Google Cloud Text-to-Speech also supports text chunking for long texts.
- Google Cloud Text-to-Speech supports batching and continuing from the last processed chunk.

## Troubleshooting

- Ensure your configuration file (`config.json`) is correctly formatted and placed in `~/.local/tts-cli/`.
- Verify that all required dependencies are installed (e.g., PyPDF2, python-pptx).
- If using URLs, make sure the URL is accessible and returns valid HTML content.
- If you encounter errors with speech synthesis, check your Azure Speech credentials.

## Repository

https://github.com/ShinChven/tts-cli.git

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
