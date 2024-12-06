from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()
    
setup(
    name="binay_parajuli",
    version="0.0.1",
    author="Binay Raj Parajuli",
    author_email="binayaparajuli17@gmail.com",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts":[
            "pack_age = pack_age:hello",
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown"
)