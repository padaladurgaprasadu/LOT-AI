from setuptools import setup, find_packages

setup(
    name="yai-sdk",
    version="10.0.0",
    description="Official Python SDK for yAI Autonomous AI Operating System (AIOS)",
    author="Padala Durga Prasad",
    author_email="durgaprasad@yai.ai",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
