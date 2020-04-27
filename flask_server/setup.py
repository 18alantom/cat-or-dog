from setuptools import setup

setup(
    name='flask_server',
    packages=['flask_server'],
    include_package_data=True,
    python_requires="3.7.6",
    install_requires=[
        'flask', 'pytorch=1.5.0', 'numpy', 'opencv', 'torchvision'
    ],
)
