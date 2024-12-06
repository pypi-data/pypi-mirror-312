from setuptools import setup, find_packages

setup(
    name="long_s",
    version="1.0.33", 
    description="This Python tool accurately inserts the historical long S character ( ſ ) back into the given text to make it appear as if it were written before the 20th century. English, French, German, Spanish and Italian are supported.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="TravisGK",
    author_email="githubtravisgk@gmail.com",
    url="https://github.com/travisgk/py-long-s/tree/main",
    packages=find_packages(),
    include_package_data=True,
    package_dir={"long_s": "long_s"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.21.0",
        "python-docx>=1.1.0",
        "odfpy>=1.4.0",
        "unidecode>=1.3.0",
    ],
)
