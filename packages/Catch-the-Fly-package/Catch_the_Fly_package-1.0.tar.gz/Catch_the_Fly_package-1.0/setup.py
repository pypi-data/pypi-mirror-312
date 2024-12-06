from setuptools import setup, find_packages
setup(
    name="Catch_the_Fly_package",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pygame",
    ],
    entry_points={
        'console_scripts': [
            'Catch_the_Fly = Catch_the_Fly.__main__:main'
        ]
    },
    package_data={
        '': ['Catch_the_Fly_package/assets/*'],
        '': ['Catch_the_Fly_package/backgrounds/*'],
    },
)