from setuptools import setup, find_packages

setup(
    name="vineethr_library",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",  # Specify the Django version required
        "Pymongo>=4.10.1",
        "Djangorestframework>=3.15.2",
        "Boto3>=1.35.71"
    ],
    description="Vehicle Insurance Application",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vineethram10/Car-Insurance",  # Update with your repo
    author="Vineeth",
    author_email="vinethrmkr@gmail.com",
    license="MIT",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
