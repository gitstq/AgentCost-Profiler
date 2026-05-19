"""
Setup script for AgentCost-Profiler.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="agentcost-profiler",
    version="1.0.0",
    author="gitstq",
    author_email="",
    description="Lightweight AI Agent Performance & Cost Optimization Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/AgentCost-Profiler",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=5.4.0",
    ],
    extras_require={
        "rich": ["rich>=10.0.0"],
        "full": [
            "rich>=10.0.0",
            "psutil>=5.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agentcost-profiler=agentcost_profiler.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
