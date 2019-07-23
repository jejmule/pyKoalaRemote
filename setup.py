import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyKoalaRemote",
    version="0.0.1",
    author="Jérôme Parent",
    author_email="jerome.parent@lynceetec.com",
    description="Python wrapper for dotNet Koala Remote Client provided by LyncéeTec to control Digital Holographique Microscope using proprietary Koala software",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jejmule/pyKoalaRemote",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microssoft :: Windows",
    ],
)