from setuptools import setup

setup(
    name="social-media-downloader",
    version="v1.0.3",
    author="Nayan Das",
    author_email="nayanchandradas@hotmail.com",
    author_portfolio="https://socialportal.nayanchandradas.com",
    description="A tool to download videos from YouTube, TikTok, Instagram, and Facebook.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nayandas69/social-media-downloader",
    license="MIT",
    py_modules=["downloader"],  # Since downloader.py is in the root directory
    install_requires=[
        "yt-dlp",
        "instaloader",
        "requests",
        "beautifulsoup4",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "social-media-downloader=downloader:main",  # CLI command: module:function
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.6",
)
