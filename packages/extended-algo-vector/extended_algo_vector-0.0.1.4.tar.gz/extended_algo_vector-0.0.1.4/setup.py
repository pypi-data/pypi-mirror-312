import time

from setuptools import setup
import shutil

try:
    print('Removing cache data before install...')
    shutil.rmtree('./build/')
    shutil.rmtree('./dist/')
    shutil.rmtree('./extended_algo.egg-info/')
    shutil.rmtree('./.pytest_cache/')
    time.sleep(1)
except:
    ...

# TODO: 'pandas_ta @ git+https://github.com/twopirllc/pandas-ta.git@development'
#  pypi does not support direct url for the following requirement

setup(name='extended-algo-vector',
      version='0.0.1.4',
      description='wrapper for vector algo that supports the extended-chart and strategy discovery',
      url='https://github.com/karunkrishna/extended_algo_vector',
      author='Karun Krishna',
      author_email='karun.krishna@gmail.com',
      license='MIT',
      packages=['extended_algo_vector', 'extended_algo_vector.engine', 'extended_algo_vector.market',
                'extended_algo_vector.market.bars','extended_algo_vector.market.events', 'extended_algo_vector.market.utils',
                'extended_algo_vector.report', 'extended_algo_vector.report.calculate', 'extended_algo_vector.report.utils',
                'extended_algo_vector.market.bars', 'extended_algo_vector.market.utils'],
      install_requires=['numpy', 'pandas', 'python-dotenv', 'extended-chart', 'tqdm', 'pyarrow',
                        'SQLAlchemy', 'mysqlclient', 'setuptools','ib_async'],
      zip_safe=False
      )


