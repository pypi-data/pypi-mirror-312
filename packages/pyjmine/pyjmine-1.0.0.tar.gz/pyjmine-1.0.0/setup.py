
from setuptools import setup, find_packages

long_description = 'pyjmine v1'

setup(
    name="pyjmine",
    version="1.0.0",
    author="Maehdakvan",
    author_email="visitanimation@google.com",
    description=".",
    long_description=long_description,
    url="https://t.me/maehdak_van",
    project_urls={
        "Bug Tracker": "https://t.me/maehdak_van",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=['jpype1', 'psutil', 'requests', 'lxml'],
    python_requires='>=3.6'
)