from setuptools import setup, find_packages
import os

setup(
    name="aws_noaction",
    version="0.1.1",
    author_email="a.ryabchenko@disasm.me",
    packages=find_packages(),
    install_requires=[
        "boto3>=1.26.0",
        "python-dotenv>=0.19.0",
    ],
    description="Prints current state of service from state.json on s3",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    keywords="aws, s3, state management",
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "read_state=app.main:read_state_from_s3",
        ],
    }
)