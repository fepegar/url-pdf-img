#!/usr/bin/env python3

"""
Adapted from https://stackoverflow.com/a/37573701/3956024
"""

import math
from pathlib import Path
from subprocess import call

import click
import requests
from tqdm import tqdm


@click.command()
@click.argument('url', type=str)
@click.argument('output_dir', type=click.Path(resolve_path=True))
def cli(url, output_dir):
    output_dir = Path(output_dir)
    filename = Path(url).name
    pdf_path = output_dir / filename
    images_dir = output_dir / 'images'
    prefix = images_dir / 'image'
    output_dir.mkdir(exist_ok=True, parents=True)
    images_dir.mkdir(exist_ok=True, parents=True)

    # Streaming, so we can iterate over the response.
    r = requests.get(url, stream=True)

    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024
    wrote = 0
    progress = tqdm(
        r.iter_content(block_size),
        total=math.ceil(total_size // block_size),
        unit='kB',
        unit_scale=True,
    )

    click.echo('Downloading PDF...')
    with open(pdf_path, 'wb') as f:
        for data in progress:
            wrote += f.write(data)

    if total_size not in (0, wrote):
        print('ERROR, something went wrong')

    command = [
        'pdfimages',
        '-all',
        str(pdf_path),
        str(prefix),
    ]
    click.echo('Extracting images...')
    call(command)


if __name__ == "__main__":
    cli()

