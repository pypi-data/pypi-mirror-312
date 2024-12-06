from setuptools import setup, find_packages

setup(
    name='transcribe_zh_en',
    version='0.9',
    packages=find_packages(),  # Automatically find all submodules
    install_requires=[         # List dependencies here
        'ffmpeg-python==0.2.0',
        'faster-whisper==1.1.0',
        'torch==2.4.1',
    ],
    entry_points={
        'console_scripts': [
            'transcribe_zh_en = transcribe_zh_en.main:main',  # Entry point to the main function
        ],
    },
    author="Mousa Abdulhamid",
    author_email="mousa.abdulhamid97@gmail.com",
    description="A package to transcribe Chinese subtitles and remove audio from videos",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Abdulhamid97Mousa/transcribe_zh_en",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)