from setuptools import setup, find_packages

setup(
    name='package_notification',  # Package name
    version='0.1.0',              # Version
    description='A package to send package delivery notifications via email.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Manjula Kore',
    author_email='koremanju00@gmail.com',
    url='https://github.com/Manjula-K-coder/Package_Tracking_System',  # Update with your repo
    license='MIT',
    packages=find_packages(),     # Automatically find sub-packages
    install_requires=[
        'Django>=3.0',            # Django dependency for send_mail
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',      # Python version compatibility
)
