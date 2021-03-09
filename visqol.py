import argparse
import os


def run_visqol(in_file="input.wav", out_file="output.wav"):
    res = os.popen(
        f"docker run -it -v {os.getcwd()}:/data jonashaag/visqol:v3 --degraded_file /data/{in_file} --reference_file "
        f"/data/{out_file} --verbose"
    ).read()
    print(res)
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, help="Input file")
    parser.add_argument(
        "--output", "-o", type=str, help="Output file", default="output.wav"
    )
    args = parser.parse_args()

    run_visqol(args.input, args.output)
