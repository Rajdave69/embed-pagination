from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="simple-embed-pagination",
    version="1.0.2",
    description="Easily create pagination for discord.py embeds.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=["paginator"],
    package_dir={'': "src"},
    url="https://github.com/RajDave69/embed-pagination",
    authors=["FaddyManatee", "RajDave69"],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ]
)
