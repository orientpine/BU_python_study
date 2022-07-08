import argparse


def makeArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        "-mo",
        required=False,
        default="CHK",
        type=str,
        help="mode: CHK | PP | EXP",
    )
    return parser.parse_args()
