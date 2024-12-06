from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="admin_custom_filter",
    version="1.0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['templates/admin/*']},
    install_requires=[
        'bleach>=6.2.0'
    ],
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Abdulaziz Baqaleb",
    author_email="ab.ah.bq@gmail.com",
    maintainer="Abdulaziz Baqaleb",
    maintainer_email="ab.ah.bq@gmail.com",
    license="MIT License",
    url="https://github.com/i3z101/admin_custom_filter/tree/master"
)