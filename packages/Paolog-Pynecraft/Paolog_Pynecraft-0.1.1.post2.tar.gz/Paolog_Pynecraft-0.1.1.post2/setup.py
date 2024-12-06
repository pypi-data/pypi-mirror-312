import setuptools

# Read the contents of README.md
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    # Package info
	name="Paolog_Pynecraft",
	version="0.1.1-2",
	description="A Minecraft recreation made with Ursina",
	long_description=long_description,
    long_description_content_type='text/markdown',
	author="Paolog",
    # Package files
	include_package_data=True,
	package_data={"": ["*.*", "**/*.*"]},
	packages=["Paolog_Pynecraft", "Paolog_Pynecraft.src.Games"],
	install_requires=['ursina', 'appdata', 'perlin_noise', 'screeninfo']
)