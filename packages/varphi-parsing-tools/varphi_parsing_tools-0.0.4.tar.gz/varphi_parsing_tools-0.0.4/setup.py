from setuptools import setup, find_packages

setup(
    name="varphi_parsing_tools",
    version="0.0.4",
    description="Lexer, parser, and representor for the Varphi programming language.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Hassan El-Sheikha",
    author_email="hassan.elsheikha@utoronto.ca",
    url="https://github.com/hassanelsheikha/varphi_parsing_tools",
    packages=find_packages(),
    install_requires=[
        "antlr4-python3-runtime==4.13.2",
        "varphi_types==0.0.4"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
