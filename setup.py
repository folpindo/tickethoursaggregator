from setuptools import find_packages, setup

# name can be any name.  This name will be used to create .egg file.
# name that is used in packages is the one that is used in the trac.ini file.
# use package name as entry_points
setup(
    name = 'TicketHoursAggregator',
    version = '0.0.1',
    packages = find_packages(),
    author = 'Faustino Olpindo',
    author_email = 'folpindo@gmail.com',
    description = 'Tries to listen any events triggered by ticket change and add hours to designated custom field.',
    keywords = 'add hours',
    url = '',
    install_requires = ['Trac>=0.11', 'Genshi>=0.5', 'Python>=2.5'],
    entry_points = """
        [trac.plugins]
        TicketHoursAggregator = tickethoursaggregator
    """,
)
