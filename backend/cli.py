from pathlib import Path

import typer


def main(millennium_falcon_file_path: Path, empire_file_path: Path):
    typer.echo(f"Hello {millennium_falcon_file_path}, {empire_file_path}")


if __name__ == "__main__":
    typer.run(main)