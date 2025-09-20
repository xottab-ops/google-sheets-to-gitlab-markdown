from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='google-sheets-synchronisation',
  version='1.0.0',
  author='xottab-ops',
  author_email='jassik2002@mail.ru',
  description='This is my first module',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/xottab-ops/google-sheets-to-gitlab-markdown.git',
  packages=find_packages(),
  install_requires=[
      'python-dotenv',
      'gspread>=6.1.4',
      'google-auth>=2.35.0',
      'google-api-python-client>=2.149.0',
      'google-auth-httplib2>=0.2.0',
      'google-auth-oauthlib>=1.2.1',
      'pandas>=2.2.3',
      'tabulate>=0.9.0',
      'python-gitlab>=4.13.0',
  ],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='sheet sync gitlab',
  project_urls={
    'Documentation': 'link'
  },
  python_requires='>=3.7'
)