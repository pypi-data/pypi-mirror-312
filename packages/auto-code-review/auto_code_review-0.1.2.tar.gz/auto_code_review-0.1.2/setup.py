from setuptools import setup, find_packages

setup(
    name='auto-code-review',  
    version='0.1.2', 
    packages=find_packages(),
    install_requires=[  
        'PyYAML',
        'requests',
        'openai'
    ],
    author='Dmitry Geyvandov',
    author_email='geyvandovdd@gmail.com',
    description='Auto-code-review for GitHub Pull Requests via ChatGPT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yosuke-yuikimatsu/auto-code-review',
    classifiers=[ 
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
