import os
import re

from flask import Blueprint, jsonify

from delay import get_delay_for_inout
from main import record_testing, WAVE_OUTPUT_FILENAME
from visqol import run_visqol

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def health_check():
    return {"msg": "I'm running! don't worry!"}


@main_bp.route("/run-test")
def run_test():
    record_testing()
    visqol_res = run_visqol(os.getenv("WAVE_INPUT_FILENAME"))
    score: str = re.findall(r"MOS-LQO:.*[0-9]+", visqol_res)[0]
    score: float = float(re.findall(r"[0-9]+\.[0-9]+", score)[0])

    return jsonify(
        [
            {"name": "MOS", "score": score},
            {
                "name": "DELAY",
                "score": get_delay_for_inout(
                    os.getenv("WAVE_INPUT_FILENAME"), WAVE_OUTPUT_FILENAME
                ),
            },
        ]
    )
