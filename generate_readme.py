import prefect
from prefect_meemoo import mediahaven
from prefect_meemoo import rdf
from prefect_meemoo import rdf_parse

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

    readme_file.write(f"# RDF\n")
    readme_file.write(f"## Tasks\n")
    for name, val in rdf.__dict__.items():
        if isinstance(val, prefect.Task):
            readme_file.write(f"- [{name}](#{name})\n")
    for name, val in rdf.__dict__.items():
        if isinstance(val, prefect.Task):
            readme_file.write(f"### {name}\n")
            readme_file.write(f"{name}{val.fn.__code__.co_varnames[:val.fn.__code__.co_argcount]}\n")
            readme_file.write(f"{val.__doc__}\n")
            val.fn.__code__.co_varnames

    readme_file.write(f"# RDF Parse\n")
    readme_file.write(f"## Tasks\n")
    for name, val in rdf_parse.__dict__.items():
        if isinstance(val, prefect.Task):
            readme_file.write(f"- [{name}](#{name})\n")
    for name, val in rdf_parse.__dict__.items():
        if isinstance(val, prefect.Task):
            readme_file.write(f"### {name}\n")
            readme_file.write(f"{name}{val.fn.__code__.co_varnames[:val.fn.__code__.co_argcount]}\n")
            readme_file.write(f"{val.__doc__}\n")
            val.fn.__code__.co_varnames
