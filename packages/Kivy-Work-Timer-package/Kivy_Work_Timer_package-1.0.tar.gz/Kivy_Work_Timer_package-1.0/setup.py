from setuptools import setup, find_packages
setup(
    name="Kivy_Work_Timer_package",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "kivy",
    ],
    entry_points={
        'console_scripts': [
            'Kivy_Work_Timer = Kivy_Work_Timer.__main__:main'
        ]
    },
    package_data={
        '': ['Kivy_Work_Timer_package/*'],
    },
)