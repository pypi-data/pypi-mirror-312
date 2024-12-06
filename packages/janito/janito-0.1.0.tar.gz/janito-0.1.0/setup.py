from setuptools import setup, find_packages

setup(
    name="janito",
    version="0.1.0",
    author="João M. Pinto",
    author_email="lamego.pinto@gmail.com",
    url="https://github.com/joaompinto/janito",
    packages=find_packages(),
    install_requires=[
        "anthropic",
        "prompt_toolkit",
        "rich",
        "typer",
        "watchdog",
        "pytest"
    ],
    python_requires=">=3.8",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    description="Language-Driven Software Development Assistant powered by Claude AI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
    ],
    entry_points={
        'console_scripts': [
            'janito=janito:main',
        ],
    },
)

