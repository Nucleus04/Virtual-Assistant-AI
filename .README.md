## Getting Started

### Setting up Speech-to-Text and Main on Windows

1. Create a virtual environment using Conda (recommended) or Python's venv module.
2. Install dependencies by running `pip install -r requirements.txt`.
3. Open a new terminal and navigate to the `stt` directory.
4. Run `python coqui.py -m "your model" -s "your scorer - optional"` to start the speech-to-text module. You can download the model and scorer from Coqui AI's GitHub releases.
5. Leave the speech-to-text module running and waiting for a connection.


## Setting up Text-to-Speech on Ubuntu

1. Create a Python virtual environment.
2. Install dependencies by running `pip install -r requirements.txt`.
3. Navigate to the `tts` directory.
4. Download the desired model (.onnx) and config (`onnx.json`) from Rhasspy's Piper `VOICES.md`.
5. Run `python3 server.py` to start the text-to-speech module.


**Note:** If you encounter issues with `lib.phonemize` or files in `/lib`, download the `libpiper_phonemize-amd64.tar` file from Rhasspy's Piper Phonemize releases, extract it, and replace the `lib` folder in your `tts` directory.


## Running the Main Module

1. Open a new Windows terminal and navigate to the root directory of the repository.
2. Activate your created Conda environment.
3. Run `python main.py` to start the main module, which will connect to the speech-to-text and text-to-speech modules and start catching speech.


## LLM Model

Currently, the project uses Groq as the LLM model. To add an LLM API, navigate to the `llm` directory. Obtain an API key from Groq's website if you wish to use their service.


