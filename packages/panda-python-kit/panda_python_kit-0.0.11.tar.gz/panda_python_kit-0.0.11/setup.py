from setuptools import setup, find_packages

setup(
    name="panda-python-kit",
    version="0.0.11",
    author="zhaojiedi.zjd",
    author_email="1072892917@qq.com",

    packages=find_packages(),
    install_requires=["requests","python-dateutil","pandas"],
    include_package_data=True,
    platforms='any',
    python_requires='>=3.6',

    description="panda python kit",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    license="MIT",
    url="",
)
