import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="makeup_service",
    version="0.0.1",
    author="Artem Baraniuk",
    author_email="artem.baranyuk@gmail.com",
    description="Applies simple makeup on videos with human face",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Art95/makeup_service",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'makeup_service': ['data/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'torch',
        'torchvision',
        'scikit-image',
        'flask',
        'numpy'
    ]
)
