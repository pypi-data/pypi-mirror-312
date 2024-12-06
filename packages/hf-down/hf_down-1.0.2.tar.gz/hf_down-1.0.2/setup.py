import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hf_down",
    version="1.0.2",
    author="LEL",
    url='',
    author_email="2324171649@qq.com",
    description="A tool to download files from Hugging Face repositories.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
