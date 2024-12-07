from setuptools import setup, find_packages
import io

# Read README with UTF-8 encoding
with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ollama-ocr",
    version="0.1.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "langchain_ollama>=0.1.0",
        "Pillow>=10.0.0",
        "requests>=2.25.0",
        "python-magic>=0.4.0",
        "transformers>=4.0.0"
    ],
    author="Anoop Maurya",
    author_email="mauryaanoop3@gmail.com",
    description="OCR powered by Ollama Vision Models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imanoop7/Ollama-OCR",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)