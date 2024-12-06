from setuptools import setup, find_packages

setup(
    name="varphi_lsp_server",
    version="0.0.3",
    description="Language Server Protocol server for the Varphi Programming Language.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Hassan El-Sheikha",
    author_email="hassan.elsheikha@utoronto.ca",
    url="https://github.com/hassanelsheikha/varphi_lsp_server",
    packages=find_packages(),
    install_requires=[
        "varphi_parsing_tools==0.0.4",
        "pygls==2.0.0a2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'varphi_lsp_server=varphi_lsp_server.varphi_lsp_server:main',
        ],
    },
    include_package_data=True,
)

