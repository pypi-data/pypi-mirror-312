from setuptools import setup, find_packages

setup(
    name="selenium-proxy", 
    version="0.1.0",  
    description="Considering that there is no function that works very well natively in Selenium for using proxys with authentication in chromedriver, this is an effective way to solve this problem.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Kairo Trzeciak",
    author_email="trz.kairodev@gmail.com",
    url="https://github.com/kairodev/selenium-proxy",
    license="MIT",
    packages=find_packages(),  
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  
)