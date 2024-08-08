from argparse import ArgumentParser
from pathlib import Path
from functools import partial
from concurrent.futures import ThreadPoolExecutor

from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

def valid_file_suffix(suffix):
    if suffix.startswith('.'):
        return suffix
    return f'.{suffix}'

def convert_image(path, suffix):
    image = Image.open(path)
    return image.save(path.with_suffix(suffix), exact=True)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('to_convert', nargs='+', type=Path)
    parser.add_argument('--suffix', type=valid_file_suffix, default='png')
    parser.add_argument('--jobs', type=int, default=1)

    args = parser.parse_args()
    converter = partial(convert_image, suffix=args.suffix)

    with ThreadPoolExecutor(args.jobs) as executor:
        executor.map(converter, args.to_convert)
