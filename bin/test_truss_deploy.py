import os
import re
import subprocess
import time
from datetime import datetime

import requests
import yaml



def truss_push():
    API_KEY = os.environ["API_KEY"]
    print("Pushing model...")
    with open("/home/runner/.trussrc", "w") as config_file:
        config_file.write(
            f"""[baseten]
        remote_provider = baseten
        api_key = {API_KEY}
        remote_url = https://app.staging.baseten.co"""
                )

    result = subprocess.run(["truss", "push", "--trusted"], capture_output=True)
    match = re.search(
        r"View logs for your deployment at \n?https://app\.staging\.baseten\.co/models/(\w+)/logs/(\w+)",
        result.stdout.decode(),
    )
    if not match:
        raise Exception(
            f"Failed to push model:\n\nSTDOUT: {result.stdout.decode()}\nSTDERR: {result.stderr.decode()}"
        )
    model_id = match.group(1)
    deployment_id = match.group(2)
    print(
        f"Model pushed successfully. model-id: {model_id}. deployment-id: {deployment_id}"
    )
    return model_id, deployment_id


if __name__ == "__main__":
    model_id, deployment_id = truss_push()
    print(model_id, deployment_id)
  