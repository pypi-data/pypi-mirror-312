from setuptools import setup, find_packages

setup(
    name="uta-av",
    version="0.1.0",
    author="Agents Valley",
    author_email="agentsvalley@gmail.com",
    description="A terminal agent for generating and executing Ubuntu commands for you.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/agentsvalley/uta-av", 
    packages=find_packages(),
    install_requires=[
        "huggingface_hub>=0.14.1",
    ],
    entry_points={
        "console_scripts": [
            "uta-av=terminal_agent.agent:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)
