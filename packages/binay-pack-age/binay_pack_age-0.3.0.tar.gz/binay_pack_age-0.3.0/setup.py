from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()
    
setup(
    name="binay_pack_age",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        
    ],
    entry_points={
        "console_scripts":[
            "pack_age = pack_age:hello",
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown"
)