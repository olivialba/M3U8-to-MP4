from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

VERSION = '0.0.1'
DESCRIPTION = 'Python package to convert m3u8 streams to mp4 videos using FFMPEG'

# Setting up
setup(
    name="lolclient-lib",
    version=VERSION,
    author="Alba (Alberto Olivi)",
    author_email="olivialberto02@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license='MIT',
    url='https://github.com/olivialba',
    install_requires=['requests', 'ffmpeg-python'],
    keywords=['m3u8', 'mp4', 'python', 'm3u8 to mp4', 'convert m3u8', 'playlist'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)