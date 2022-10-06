from os import read
import prefect
from prefect_meemoo import mediahaven

with open("README.md", "w") as readme_file:
    readme_file.write(f"# Mediahaven\n")
    readme_file.write(f"## Tasks\n")
    for name, val in mediahaven.__dict__.items():
        if isinstance(val, prefect.Task):
            readme_file.write(f"- [{name}](#{name})\n")
    for name, val in mediahaven.__dict__.items():
        if isinstance(val, prefect.Task):
            readme_file.write(f"### {name}\n")
            readme_file.write(f"{name}{val.fn.__code__.co_varnames[:val.fn.__code__.co_argcount]}\n")
            readme_file.write(f"{val.__doc__}\n")
            val.fn.__code__.co_varnames
            # print("###" + name)
            # print(val.__doc__)