from setuptools import setup, find_packages

setup(
    name="llama_ocr_py",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "ollama>=0.1.27",
        "Pillow>=10.1.0",
        "python-dotenv>=1.0.0",
        "opencv-python>=4.8.1.78",
        "numpy>=1.21.0",
    ],
    author="Mazharul Islam Leon",
    author_email="xtleon.xleo@gmail.com",
    description="A package for document extraction using Ollama Vision model",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/princexoleo/llama_ocr_py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
