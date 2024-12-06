from setuptools import setup, find_packages

version = {
    "year" :2024,
    "minor" :1,
    "patch" :18,
}

setup(
    name='Blackforge',
    version=f"{version["year"]}.{version["minor"]}.{version["patch"]}",
    description='Light Shines Brighter In The Dark.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Izaiyah Stokes',
    author_email='d34d.dev@gmail.com',
    url='https://github.com/d34d0s/BlackForge',
    packages=find_packages(),
    package_data={"blackforge": ['assets/*']},
    install_requires=[
        "Numpy",
        "Pygame-CE",
        "SetupTools",
    ],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)