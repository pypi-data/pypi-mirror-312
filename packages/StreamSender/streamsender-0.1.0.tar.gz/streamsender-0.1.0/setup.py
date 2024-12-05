from setuptools import setup, find_packages

setup(
    name="StreamSender",
    version="0.1.0",
    author="liushihai02",
    author_email="liushihai02@58.com",
    packages=find_packages(),
    install_requires=[
        'scapy==2.6.0',
        'opencv-python==4.10.0.84',
        'pydub==0.25.1',
        'loguru==0.7.2',
        'soundfile==0.12.1',
        'librosa==0.10.2',
        'numpy==1.26.4'
    ],
    description="A SDK for sending RTP and RTMP streams",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.9',
)
