from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent

# Ensure the file exists; fallback to a default description if missing
readme_file = this_directory / "Readme_PyPi.md"
if readme_file.exists():
    long_description = readme_file.read_text()
else:
    long_description = "Simple library to write Python emails."

setup(
    name="emailfly",
    version="1.0.0",
    license='MIT',
    description="Simple library to write python emails",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="EncoreSky Technologies",
    author_email='samrathpatidar@encoresky.com',
    url='https://github.com/samrath-est/mailer.git',
    packages=find_packages(include=["emailfly", "emailfly.*"]),  
    include_package_data=True,
    install_requires=[
        "beautifulsoup4==4.12.3",  # Correct typo here
        "pillow==11.0.0"
    ],
    dependency_links=[],
    entry_points={},
)
