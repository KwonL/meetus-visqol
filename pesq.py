import argparse

import numpy as np
from pypesq import pesq
from scipy.io.wavfile import read


def pesq_by_inout(in_file, out_file):
    sr, ref = read(in_file)
    sr, deg = read(out_file)

    if len(ref.shape) >= 2:
        ref = ref[:, 0]
    if len(deg.shape) >= 2:
        deg = deg[:, 0]
    ref = np.pad(ref, (0, len(deg) - len(ref)), "constant", constant_values=0)
    return pesq(ref, deg, sr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", "-i", type=str, help="Input file", default="input.wav"
    )
    parser.add_argument(
        "--output", "-o", type=str, help="Output file", default="output.wav"
    )
    args = parser.parse_args()
    print(pesq_by_inout(args.input, args.output))
