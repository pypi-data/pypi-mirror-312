from setuptools import setup, find_packages

setup(
    name='audio-segmenter',
    version='0.1.2',
    description='Advanced Audio Segmentation Tool',
    author='Emirhan Kuru',
    author_email='1emirhankuru@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pydub',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'audio-segmenter=audio_segmenter.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
)