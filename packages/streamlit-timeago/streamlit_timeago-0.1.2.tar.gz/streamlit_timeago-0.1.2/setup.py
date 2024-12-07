from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-timeago",
    version="0.1.2",
    author="David Prihoda",
    author_email="david.prihoda@gmail.com",
    description="Streamlit wrapper of timeago-react to render time ago",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prihoda/streamlit-timeago",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
    extras_require={
        "devel": [
            "wheel",
            "pytest==7.4.0",
            "playwright==1.48.0",
            "requests==2.31.0",
            "pytest-playwright-snapshot==1.0",
            "pytest-rerunfailures==12.0",
        ]
    }
)
