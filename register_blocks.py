import subprocess

import yaml

with open("./.openshift/blocks.yaml") as f:
    blocks = yaml.safe_load(f)

for block in blocks["blocks"]:
    subprocess.run([
        "prefect",
        "blocks",
        "register",
        "-f",
        block["path"],
    ])