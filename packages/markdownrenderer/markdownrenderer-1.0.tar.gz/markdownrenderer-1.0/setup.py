from setuptools import setup, find_packages

setup(
    name="markdownrenderer",  # The name of your package
    version="1.0",  # The version of your package
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        'pywebview',
        'markdown',
        'flask',
    ],
    description="A simple markdown renderer in python",  # Short description
    long_description=open('README.md').read(),  # Read long description from README
    long_description_content_type='text/markdown',  # Markdown format for the long description
    author="BOTTOMFRAGGER523",  # Your name
    url="https://github.com/BOTTOMFRAGGER523/Markdown-RendererPy",  # URL of the project (GitHub, etc.)
    classifiers=[  # PyPI classifiers for categorizing the package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',  # GPLv2 license
        'Operating System :: OS Independent',  # Cross-platform support
    ],
    python_requires='>=3.10',  # Define the minimum Python version requirement
    license='GPLv2',  # Specify the GPLv2 license
    keywords='markdownrenderer, markdown renderer',  # Keywords for easier search on PyPI
)
