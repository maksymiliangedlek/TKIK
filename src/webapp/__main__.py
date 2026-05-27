import argparse

from .server import run


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the DSL web UI.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    run(args.host, args.port)
