from argparse import ArgumentParser
from functools import partial
from pathlib import Path
from shutil import copytree

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from livereload import Server, shell
from textwrap import dedent

here = Path(__file__).parent

def insert_active_nav(path, soup):
    nav_link = soup.select_one(f'li a[href="{path}"]')
    if nav_link is not None:
        nav_link['aria-current'] = 'page'
        nav_link['class'].append('active')

    return soup

# def insert_active_nav(path, soup): # TODO: surround header tags in anchors
#     nav_link = soup.select_one(f'li a[href="{path}"]')
#     if nav_link is not None:
#         pass


def build(input_path, site_dir, output_dir, env):
    if isinstance(input_path, list):
        return [build(p, site_dir, output_dir, env) for p in input_path]

    input_path = Path(input_path)

    if not {'templates', 'components'}.isdisjoint(input_path.parts):
        return rebuild_all(site_dir, output_dir, env)

    relpath = input_path.relative_to(site_dir)
    outpath = output_dir / relpath

    if not {'images', 'css', '_images'}.isdisjoint(input_path.parts):
        # images in a symlinked folder
        # .css files are symlinked, .scss is rebuild via sass.
        return

    if input_path.suffix == '.j2':
        outpath = outpath.with_suffix('') # remove .j2 suffix

        template_path = input_path.relative_to(site_dir.parent)
        template = env.get_template(str(template_path))
        text = template.render()

        if outpath.suffix == '.html':
            soup = BeautifulSoup(text, features='lxml')
            if soup.select('nav') is not None:
                soup = insert_active_nav(outpath.relative_to(output_dir), soup)
            text = soup.prettify()

    else:
        text = input_path.read_text()

    outpath.write_text(text)

def rebuild_all(site_dir, output_dir, env):
    for path in site_dir.rglob('*'):
        relpath = path.relative_to(site_dir)
        outpath = output_dir / relpath
        if path.is_dir():
            outpath.mkdir(parents=True, exist_ok=True)

    for path in site_dir.rglob('*'):
        build(path, site_dir, output_dir, env=env)

if __name__ == '__main__':
    # dont forget to manually link site/images to _build/images

    here = Path(__file__).parent
    site_dir, build_dir = here / 'site', here / '_build'
    build_dir.mkdir(exist_ok=True)

    file_loader = FileSystemLoader([here])

    env = Environment(loader=file_loader, auto_reload=True)
    env.globals['title'] = 'The Wholesome Homecook'
    env.globals['home_carosel'] = [
        p.relative_to(site_dir)
        for p in (site_dir / 'images').glob('*png')
        if not p.name.lower().startswith('headshot')
    ][:5]
    env.globals['lorem'] = dedent('''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    ''').strip()

    callback = partial(build, site_dir=site_dir, output_dir=build_dir, env=env)
    rebuild_all(site_dir, build_dir, env=env)

    server = Server()
    host, port = '127.0.0.1', 5500
    host, port = '0.0.0.0', 5500

    server.watch(str(site_dir / '**'), callback)
    server.watch(str(here / 'templates' / '**'), callback)
    server.watch(str(here / 'components' / '**'), callback)
    server.serve(host=host, port=port, root='_build')

