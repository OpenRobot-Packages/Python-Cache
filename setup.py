import re
from setuptools import setup

with open('openrobot/cache/__init__.py') as f:
    try:
        version = re.search(
            r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.M
        ).group(1)
    except AttributeError:
        raise RuntimeError('Could not identify version') from None

    try:
        author = re.search(
            r'^__author__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.M
        ).group(1)
    except AttributeError:
        author = 'OpenRobot Packages'

try:
    with open('README.md', encoding='utf-8') as f:
        readme = f.read()
except:
    readme = ''

requirements = []
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='OpenRobot-Cache',
    version=version,
    description='A package to support cache with optional redis support with async and non-async support.',
    author=author,
    author_email='github@openrobot.xyz',
    url='https://github.com/OpenRobot-Packages/Python-Cache',
    packages=[
        'openrobot'
    ],
    license='MIT',
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'docs': [
            'sphinx>=4.0.2',
            'karma_sphinx_theme>=0.0.8',
            'sphinxcontrib-asyncio>=0.3.0',
            'sphinx-nervproject-theme>=2.0.4',
        ]
    },
)