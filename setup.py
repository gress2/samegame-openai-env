import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="samegame-openai-env",
    version="0.0.1",
    author="Collin Gress",
    author_email="gress126@gmail.com",
    description="A SameGame OpenAI environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gress2/samegame-openai-env",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
