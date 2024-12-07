from setuptools import setup, find_packages

setup(
    name='ultraconfiguration',
    version='1.1.0',
    license="MIT License with attribution requirement",
    author="Ranit Bhowmick",
    author_email='bhowmickranitking@duck.com',
    description='''UltraConfiguration is a fast and efficient Python library for loading and managing configuration files with ease.''',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Kawai-Senpai/UltraConfiguration',
    download_url='https://github.com/Kawai-Senpai/UltraConfiguration',
    keywords=["Config", "Configuration", "JSON", "YAML", "Settings"],
    install_requires=[
        'pyyaml>=6.0',        # For YAML support
        'jsonschema>=4.0.0',  # For schema validation
        'typing-extensions;python_version<"3.8"',  # For older Python support
        'aiofiles>=23.1.0',   # For async file operations
        'asyncio>=3.4.3',     # For Python < 3.8
    ],
    python_requires='>=3.7',
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-asyncio>=0.21.0',  # For testing async features
            'black>=22.0.0',
            'mypy>=0.900',
            'flake8>=4.0.0',
        ],
        'docs': [
            'sphinx>=4.0.0',
            'sphinx-rtd-theme>=1.0.0',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Typing :: Typed',
    ],
)
