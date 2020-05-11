import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simulation_generator", # Replace with your own username
    version="0.1.0",
    author="Henrik Andersen Sveinsson",
    author_email="henriasv@fys.uio.no",
    description="Package for generating simulations from templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/henriasv/simulation-generator",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["molecular-builder @ git+https://github.com/henriasv/molecular-builder",
                      "pack-water @ git+https://github.com/evenmn/pack-water"]
)
