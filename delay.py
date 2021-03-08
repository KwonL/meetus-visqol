from scipy.io.wavfile import read
from scipy import fftpack
import numpy as np
import argparse


def get_delay_for_inout(in_file, out_file):
    a = read(in_file)
    sample_rate = a[0]
    a = np.array(a[1], dtype=float)
    b = read(out_file)
    if len(b[1].shape) >= 2:
        b = np.array(b[1][:, 0], dtype=float)
    else:
        b = np.array(b[1], dtype=float)

    a = np.pad(a, (0, len(b) - len(a)), "constant", constant_values=0)

    af = fftpack.fft(a)
    bf = fftpack.fft(b)
    Ar = -af.conjugate()
    return np.argmax(np.abs(fftpack.ifft(Ar * bf))) / sample_rate


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, help="Input file")
    parser.add_argument("--output", "-o", type=str, help="Output file")
    args = parser.parse_args()
    print(get_delay_for_inout(args.input, args.output))
