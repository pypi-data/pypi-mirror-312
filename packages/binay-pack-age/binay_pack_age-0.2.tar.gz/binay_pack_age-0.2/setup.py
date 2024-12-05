from setuptools import setup, find_packages


setup(
    name="binay_pack_age",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        
    ],
    entry_points={
        "console_scripts":[
            "pack_age = pack_age:hello",
        ],
    },
)