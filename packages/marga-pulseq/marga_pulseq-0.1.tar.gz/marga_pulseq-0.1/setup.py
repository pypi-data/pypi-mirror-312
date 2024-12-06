from setuptools import setup

setup(name='marga_pulseq',
      version='0.1',
      description='A simple interpreter from PulSeq to MARGA',
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      url='https://github.com/marcos-mri/marga-pulseq',
      author='José Miguel Algarín',
      author_email='josalggui@i3m.upv.es',
      license='MIT',
      packages=['marga_pulseq'],
      install_requires=[],
      classifiers=['Operating System :: OS Independent',
                   'Programming Language :: Python'],
      python_requires='>=3.6',
      )