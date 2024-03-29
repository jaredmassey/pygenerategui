import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygenerategui", # Replace with your own username
    version="0.0.8",
    author="Jared Massey",
    author_email="jared@jaredmassey.com",
    description="Utility for generating simple GUI to execute Python code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaredmassey/pygenerategui",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)