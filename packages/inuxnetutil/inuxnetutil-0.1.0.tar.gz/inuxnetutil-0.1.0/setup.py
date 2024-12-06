from setuptools import setup, find_packages
import os
with open(os.path.join(os.path.dirname(__file__),"README.md")) as f:
    long_desc = f.read()
with open(os.path.join(os.path.dirname(__file__),"requirements.txt")) as f:
    dependencies = f.read().splitlines()

setup(
    name='inuxnetutil',
    version='0.1.0',
    py_modules=["inuxnetutil"],
    url='https://newgit.inuxnet.org/devel/inuxnetutil.git',
    license='MIT',
    license_files=('LICENSE.txt',),
    long_description=long_desc,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    project_urls={
        "Documentation": "https://newgit.inuxnet.org/devel/inuxnetutil.git",
        "Source Code": "https://newgit.inuxnet.org/devel/inuxnetutil.git",
    },
    packages=find_packages(where="inuxnetutil"),
    package_dir={'': 'inuxnetutil'},
    include_package_data=True,
    install_requires=dependencies,
    author='Jess Williams',
    keywords="validation encrypt decrypt inuxnet",
    author_email='devel@inuxnet.org',
    description='Set of common handy functions and tools.',
    entry_points={"console_scripts": ["cryptfile=inuxnetutil:main_cryptfile",
                                      "encryptfile=inuxnetutil:main_encryptfile",
                                      "decryptfile=inuxnetutil:main_decryptfile",
                                      "encrypt=inuxnetutil:main_encrypt",
                                      "decrypt=inuxnetutil:main_decrypt"]},
)