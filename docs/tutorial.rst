Tutorial
========

Each Intent module (Units, Numbers, Dates, Solver) is packaged as a service. That is, to use the module, you must instantiate an object of type (for example) NumberService. This allows the user to parameterize their function calls universally (e.g., by providing a specific timezone to be used across extractions for the Date module).

Typical usage of the Date module, for example, might look like::

    #!/usr/bin/env python
    from intent.dates import DateService

    service = DateService()
    date = service.extractDate("On March 3 at 12:15pm...")
    ...

Or, if the user were to provide a specific timezone (with `pytz <http://pytz.sourceforge.net>`_)::

    #!/usr/bin/env python
    from intent.dates import DateService
    from pytz import timezone

    service = DateService(tz=timezone('US/Eastern'))
    date = service.extractDate("On March 3 at 12:15pm...")
    ...

The other modules function similarly; you can find a wide range of use cases and examples in the test suite.
