import argparse
import io
import os
from pathlib import Path
import subprocess as sp
import sys
import zipfile
from progressbar import ProgressBar, Bar, Percentage, ETA
import ffmpeg  

def find_files(in_path: str, extensions: list) -> list:
    out = []
    for file in Path(in_path).iterdir():
        if file.suffix.lower().lstrip(".") in extensions:
            out.append(file)
    return out

def copy_process_streams(process: sp.Popen):
    p_stdout, p_stderr = process.stdout, process.stderr
    streams = [p_stdout, p_stderr]
    buffers = [b"", b""]
    while True:
        readable, _, _ = select.select(streams, [], [], 0.1)
        for idx, stream in enumerate(streams):
            if stream in readable:
                data = os.read(stream.fileno(), 4096)
                if not data:
                    streams.remove(stream)
                else:
                    sys.stdout.buffer.write(data)
                    sys.stdout.flush()

def separate(inp: str, outp: str, model: str, two_stems: str, mp3: bool, mp3_rate: int, float32: bool, int24: bool):
    cmd = ["python", "-m", "demucs.separate", "-o", outp, "-n", model, "--device", "cuda"]
    if mp3:
        cmd += ["--mp3", f"--mp3-bitrate={mp3_rate}"]
    if float32:
        cmd += ["--float32"]
    if int24:
        cmd += ["--int24"]
    if two_stems:
        cmd += [f"--two-stems={two_stems}"]
    files = [str(f) for f in find_files(inp, ["mp3", "wav", "ogg", "flac"])]
    if not files:
        print(f"No valid audio files in {inp}")
        return
    print("Going to separate the files:")
    print('\n'.join(files))
    print("With command: ", " ".join(cmd))
    
    widgets = [Percentage(), Bar(), ETA()]
    pbar = ProgressBar(widgets=widgets, maxval=len(files))
    pbar.start()

    for idx, file in enumerate(files):
        p = sp.Popen(cmd + [file], stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            print(f"Separation failed for {file}")
        pbar.update(idx + 1)
    
    pbar.finish()

    zip_stems(outp)

def zip_stems(outp: str):
    stem_files = [f for f in os.listdir(outp) if os.path.isfile(os.path.join(outp, f))]
    with zipfile.ZipFile(os.path.join(outp, "separated_stems.zip"), 'w') as zip_file:
        for stem in stem_files:
            zip_file.write(os.path.join(outp, stem), stem)

def convert_to_mp3(input_file: str, output_file: str, bitrate: int):
    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_file, audio_bitrate=f'{bitrate}k')
            .run()
        )
    except ffmpeg.Error as e:
        print(f"Failed to convert to MP3: {e}")
        print(e.stderr.decode())

def parse_args():
    parser = argparse.ArgumentParser(description='Hybrid Demucs Music Source Separation')
    parser.add_argument('--input', '-i', type=str, default='..\in', help='Input directory containing audio files')
    parser.add_argument('--output', '-o', type=str, default='..\out', help='Output directory for separated audio files')
    parser.add_argument('--model', '-m', type=str, default='htdemucs', help='Model to use for separation')
    parser.add_argument('--two-stems', '-t', type=str, default=None, help='Specify stems to separate')
    parser.add_argument('--mp3', action='store_true', help='Enable MP3 output format')
    parser.add_argument('--mp3-rate', type=int, default=320, help='Bitrate for MP3 output')
    parser.add_argument('--float32', action='store_true', help='Output as float 32 wavs')
    parser.add_argument('--int24', action='store_true', help='Output as int24 wavs')
    return parser.parse_args()

def main():
    args = parse_args()
    separate(args.input, args.output, args.model, args.two_stems, args.mp3, args.mp3_rate, args.float32, args.int24)
    if args.mp3:
        stem_files = [f for f in os.listdir(args.output) if os.path.isfile(os.path.join(args.output, f))]
        for stem in stem_files:
            stem_path = os.path.join(args.output, stem)
            if stem.endswith('.wav'):
                mp3_output = os.path.splitext(stem_path)[0] + '.mp3'
                convert_to_mp3(stem_path, mp3_output, args.mp3_rate)

if __name__ == "__main__":
    main()
