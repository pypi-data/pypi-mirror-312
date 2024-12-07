from setuptools import setup, find_packages

setup(
    name="st_link_analysis_ie2",
    version="0.3.0",
    author="AlrasheedA, Dylan Lau",
    description="A streamlit custom component for visualizing and interacting with graphs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["streamlit", "cytoscape", "graph", "link analysis"],
    install_requires=["streamlit>=0.63"],
    packages=find_packages(include=["st_link_analysis_ie2", "st_link_analysis_ie2.*"]),
    package_data={
        "st_link_analysis_ie2": [
            "component/*.py",
            "frontend/build/*",
        ]
    },
    project_urls={
        "Homepage": "https://github.com/AlrasheedA/st-link-analysis",
        "Issues": "https://github.com/AlrasheedA/st-link-analysis/issues",
    },
    extras_require={
        "dev": [
            "ruff",
            "pytest",
        ]
    },
    entry_points={
        "console_scripts": []
    },
)
