=======
Log it!
=======

A simple manual logger originally designed to keep a log of
troubleshooting steps. The idea is to keep the messages short, but
plentiful.


Development
^^^^^^^^^^^

To start development:

#. ``git clone https://github.com/tanj/log-it.git``
#. Install `Poetry <https://python-poetry.org>`_
#. In the project directory run:

   #. ``virtualenv venv``
   #. Activate the virtual env.

      - In bash ``source venv/Scripts/activate``
      - In cmd ``venv/Scripts/activate.bat``

   #. ``poetry install -E postgres``
   #. ``pre-commit install``

#. ``mkdir instance``
#. create ``instance/instance_config.py`` with any private config
   vars. eg. ``SQLALCHEMY_DATABASE_URI``
#. Set the environment variable ``FLASK_APP``  to point to ``<PROJECT_DIR>/wsgi.py``


Testing
.......

This project is using `pytest <https://docs.pytest.org>`_ with
`coverage <https://coverage.readthedocs.io/en/coverage-5.3/index.html>`_ for
unit tests. The hope is to have as much test coverage as
possible. This will make any changes easier and we will know faster if
we break things.

#. ``coverage run -m pytest``
#. ``coverage html``
#. View coverage report at ``<PROJECT_DIR>/htmlcov/index.html``

I'd like to have any database testing be possible with sqlite. I'm
also hoping that a lot of the modules can be tested with `pytest-mock
<https://pypi.org/project/pytest-mock/>`_ (based on `Mock
<https://mock.readthedocs.io/en/latest/>`_) without having to create
too much data to test against.
