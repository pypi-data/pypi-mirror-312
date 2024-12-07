import setuptools 

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="track_id_generator_nan",
    # Replace with your own username above
    version="0.0.1",
    author="Nan",
    author_email="nancybetter4work@gmail.com",
    description="To generate a unique 12 track id, which contain letters and digits.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nan-wang-good/generate_pkg.git", 
    packages=setuptools.find_packages(),
    # if you have libraries that your module/package/library
    #you would include them in the install_requires argument
    install_requires=[
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)