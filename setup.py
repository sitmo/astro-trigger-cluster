import setuptools

with open("README.md", "r") as fh:
    README = fh.read()

# This call to setup() does all the work
setuptools.setup(
    name="astro-trigger-cluster",
    version="0.0.1",
    description="A package for clustering triggers from radio astronomical pulse searches.",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=['astronomy','clustering'],
    url="https://github.com/sitmo/astro-trigger-cluster",
    author="Thijs van den Berg",
    author_email="thijs@sitmo.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    #packages=["astro-trigger-cluster"],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["pandas", "numpy"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)