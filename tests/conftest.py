import os


def pytest_sessionstart(session):
    path = os.path.join(os.getcwd(), "tests/etl")
    output = os.popen(f"cd {path}; yarn install; yarn tsc")

    while True:
        line = output.readline()

        if line:
            print(line, end="")
        else:
            break

    output.close()
