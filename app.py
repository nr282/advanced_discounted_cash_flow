# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import signal
import sys
from types import FrameType

from flask import Flask, request, jsonify

from utils.logging import logger
from variational_framework.daily_cash_flow import calculate_daily_cash_flow
import pandas as pd
app = Flask(__name__)


def _validate(dates, cashflows):
    return True

@app.route("/")
def calculate_cash_flows() -> str:
    # Use basic logging with custom fields
    logger.info(logField="custom-entry", arbitraryField="custom-entry")

    # Use request.args.get() to safely pull values (returns None if missing)
    values = request.args.get('values')
    start_quarter = request.args.get('start_quarter')

    print("Values are provided by")
    print(values)

    print("Begin Quarter: ")
    print(start_quarter)

    quarters = pd.period_range(start=start_quarter, periods=20, freq="Q-DEC")
    dates = quarters.to_timestamp()
    values = [20 for quarter in dates]
    data = pd.DataFrame.from_dict({"Date": dates, "Quarters": quarters, "Value": values})

    result = calculate_daily_cash_flow(data)

    res = result.to_dict()
    return res


def shutdown_handler(signal_int: int, frame: FrameType) -> None:
    logger.info(f"Caught Signal {signal.strsignal(signal_int)}")

    from utils.logging import flush

    flush()

    # Safely exit program
    sys.exit(0)


if __name__ == "__main__":
    # Running application locally, outside of a Google Cloud Environment

    # handles Ctrl-C termination
    signal.signal(signal.SIGINT, shutdown_handler)

    app.run(host="localhost", port=8080, debug=True)
else:
    # handles Cloud Run container termination
    signal.signal(signal.SIGTERM, shutdown_handler)
