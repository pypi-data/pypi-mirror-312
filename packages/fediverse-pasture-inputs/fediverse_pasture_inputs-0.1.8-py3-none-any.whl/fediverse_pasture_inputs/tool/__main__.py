import asyncio
import click
from pathlib import Path
from fediverse_pasture_inputs import available

from .format import page_from_inputs


async def run_for_path(path):
    for inputs in available.values():
        with open(f"{path}/{inputs.filename}", "w") as fp:
            await page_from_inputs(fp, inputs)


@click.command()
def main():
    path = "docs/inputs/"
    Path(path).mkdir(parents=True, exist_ok=True)
    asyncio.run(run_for_path(path))


if __name__ == "__main__":
    main()
