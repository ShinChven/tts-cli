# tts-cli

A command-line utility to convert text files to speech audio using the Azure Speech SDK.

## Installation

1. Ensure [Python 3](https://www.python.org) is installed.
2. Install dependencies:
   ```bash
   pip install azure-cognitiveservices-speech PyPDF2 python-docx
   ```
3. Install the CLI tool:
   ```bash
   pip install -e .
   ```
4. Clone this repository and navigate to the project directory.

## Configuration

Create a config file at `~/.local/tts-cli/config.json` with provider settings:

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
        }
    }
}
```

## Usage

Convert a file (supported formats: .txt, .md, .pdf, .doc, .docx) to speech audio:

```bash
python tts_cli/main.py path/to/your/file.txt
```

The audio file will be saved with the same base name and an appropriate extension.

## Troubleshooting

- Verify that the configuration file exists and is properly set up.
- Confirm all required dependencies are installed.
- Check your Azure Speech credentials if you encounter errors.
