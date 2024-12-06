from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sportnews-api",
    version="0.1.6",  # Incrémentez la version pour la nouvelle publication
    author="Stefen",  # Votre nom réel
    author_email="votre.email@domain.com",  # Votre email professionnel
    description="Official Python SDK for the SportNews API - Access sports news in real time",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/votre-username/sportnews-sdk",
    project_urls={
        "Documentation": "https://docs.sportnews-api.com",
        "Source": "https://github.com/votre-username/sportnews-sdk",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    keywords="sports news api sdk actualités sportives",
)