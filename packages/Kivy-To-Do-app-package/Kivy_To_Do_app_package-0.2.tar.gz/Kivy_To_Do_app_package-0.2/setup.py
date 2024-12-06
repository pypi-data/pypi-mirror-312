from setuptools import setup, find_packages
setup(
    name="Kivy_To_Do_app_package",
    version="0.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Kivy",
    ],
    entry_points={
        'console_scripts': [
            'Kivy_To_Do_app = Kivy_To_Do_app.__main__:main'
        ]
    },
    package_data={
        '': ['Kivy_To_Do_app_package/*'],
    },
)