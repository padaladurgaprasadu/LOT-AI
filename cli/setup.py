from setuptools import setup

setup(
    name="yai-cli",
    version="10.0.0",
    description="Official Command-Line Tool for yAI Autonomous AI Operating System (AIOS)",
    author="Padala Durga Prasad",
    author_email="durgaprasad@yai.ai",
    py_modules=["yai_cli"],
    install_requires=[
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "yai=yai_cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
