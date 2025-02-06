# tts-cli

A CLI tool to synthesize voice from a text file using an AI API.

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
        }
    }
}
```

## Usage

Supported file types:
- .txt
- .md
- .pdf
- .doc
- .docx

Run the CLI with:
```bash
tts path/to/your/file.txt
```
Or directly via Python:
```bash
python -m tts_cli.main path/to/your/file.txt
```

### Arguments

- file: The path to the input text file.
- -f, --force: Force multi-chunk synthesis without confirmation.

The tool will save the synthesized audio file with the same basename as the input file and the appropriate extension.

## Repository

https://github.com/ShinChven/tts-cli.git
