from setuptools import setup, find_packages

setup(
    name="memgpt",
    version="0.2.0",
    author="Norwegian Brain Initiative",
    packages=find_packages(),
    python_requires='>=3.6',
    include_package_data=True,
    description="This package contains the code for training a "
                "memory-augmented GPT model on patient data. "
                ""
                "Please note that this is not the 'letta' company project with the"
                "https://github.com/letta-ai/letta; for use of their package, pls"
                "use 'pymemgpt' instead.",
)
