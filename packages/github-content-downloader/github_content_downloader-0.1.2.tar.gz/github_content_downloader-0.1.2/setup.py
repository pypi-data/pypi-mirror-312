from setuptools import setup, find_packages

setup(
    name="github-content-downloader",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        'console_scripts': [
            'ghcd=github_downloader.cli:main',
        ],
    },
    author="Md.Soykot",
    author_email="md.soykot2910@gmail.com",
    description="Download any file or folder from GitHub repositories without cloning",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/soykot2910/github-content-downloader",
    python_requires=">=3.6",
) 