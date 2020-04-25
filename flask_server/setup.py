from setuptools import setup

setup(
    name='flask_server',
    packages=['flask_server'],
    include_package_data=True,
    install_requires=[
        'flask', 'pytorch', 'numpy', 'opencv', 'torchvision'
    ],
)
