from setuptools import find_packages, setup
from ffxivstat import __version__


setup(
    name='ffxivstat',
    version=__version__,
    author="Balazs Nadasdi",
    author_email="efertone@pm.me",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'BeautifulSoup4',
        'requests',
        'pyyaml',
        'pony',
        'psycopg2cffi',
    ],
    entry_points="""
    [console_scripts]
    ffxiv-email-report = ffxivstat.email_report:run
    ffxiv-price-history = ffxivstat.price_history:run
    ffxiv-report = ffxivstat.report:run
    """
)
