from setuptools import setup
import os.path

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# The text of the requirements file
with open(os.path.join(HERE, "requirements.txt")) as fid:
    requirements = fid.read()

setup(
    name="soundy",
    version="1.0.0",
    description="Download SoundCloud tracks easily",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MohamedHaroon/Soundy",
    author="Mohamed Haroon",
    author_email="Mohamedessa736@gmail.com",
    license="GPL-3.0",
    keywords="SoundCloud scrape download downloader track soundy",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["soundy"],
    include_package_data=True,
    install_requires=requirements
)