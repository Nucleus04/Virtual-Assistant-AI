import onnxruntime
import jsonlines
import numpy as np
from scipy.io.wavfile import write, read
import subprocess
import json
import io

def save(audio_data): 
    audio_data = np.clip(audio_data, -1, 1)
    scaled_audio_data = np.int16(audio_data * 32767)
    scaled_audio_data = np.squeeze(scaled_audio_data)
    
    # Save as WAV file
    output_file_path = 'output.wav'
    write(output_file_path, 22050, scaled_audio_data)
    
    # Read the WAV file back into memory
    sample_rate, data = read(output_file_path)
    
    # Convert audio data to bytes
    with io.BytesIO() as bytes_io:
        write(bytes_io, sample_rate, data)
        bytes_audio = bytes_io.getvalue()
    
    return bytes_audio

def run_inference(onnx_model_path, json_content, output_dir, session):
    phoneme_ids = [entry['phoneme_ids'] for entry in json_content]
    input_lengths = [len(ids) for ids in phoneme_ids]
    input_data = {
        'input': phoneme_ids,
        'input_lengths': input_lengths,
        'scales': [1.0, 1.0, 1.0]  
    }
    audio_data = session.run(None, input_data)
    bytes_data = save(audio_data)
    return bytes_data
    # return audio_data

def phomenizer(input_text):
    command = f"""lib/piper_phonemize -l en-us --espeak-data lib/espeak-ng-data/ <<EOF
    {input_text}"""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, text=True)
        output_string = result.stdout
        json_line_objects = [json.loads(line) for line in output_string.splitlines()]
        return json_line_objects
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def synthesized(session, input_text, onnx_model_path):
    jsonlineObj = phomenizer(input_text)
    output_directory = 'output.wav'
    audio_data = run_inference(onnx_model_path, jsonlineObj, output_directory, session)

    
    return audio_data


