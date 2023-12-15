import os
import re
from typing import List

import setuptools


def get_requirements(requirements_file: str) -> List[str]:
    """Read requirements from requirements.in."""

    file_path = os.path.join(os.path.dirname(__file__), requirements_file)
    with open(file_path, 'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if not line.startswith('#') and line]
    return lines


def find_version(*file_path_parts: str) -> str:
    """Get version from virtuscale.__init__.__version__."""

    file_path = os.path.join(os.path.dirname(__file__), *file_path_parts)
    with open(file_path, 'r') as f:
        version_file_text = f.read()

    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file_text,
        re.M,
    )
    if version_match:
        return version_match.group(1)

    raise RuntimeError(f'Unable to find version string in file: {file_path}.')


def read_readme() -> str:
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_path) as f:
        return f.read()


docker = ['docker']
kubernetes = ['kfp-kubernetes<2']

setuptools.setup(
    name='virtuscale',
    version=find_version('virtuscale', '__init__.py'),
    description='Virtuscale SDK',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='The FootprintAI Authors',
    url='https://github.com/footprintai/virtuscale',
    project_urls={
        'Bug Tracker':
            'https://github.com/footprintai/virtuscale/issues',
        'Source':
            'https://github.com/footprintai/virtuscale/tree/master/sdk',
        'Changelog':
            'https://github.com/footprintai/virtuscale/blob/master/sdk/RELEASE.md',
    },
    install_requires=get_requirements('requirements.in'),
    extras_require={
        'all': docker + kubernetes,
        'kubernetes': kubernetes,
    },
    packages=setuptools.find_packages(exclude=['*test*']),
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7.0,<3.13.0',
    include_package_data=True,
    )
