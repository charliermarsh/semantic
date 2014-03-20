Documentation
=============

Intent consists of four modules, each of which is responsible for extracting a different type of semantic text:

.. toctree::
   :maxdepth: 2

   dates
   numbers
   math
   units

Each module is structured as a *service*. That is, to use the *numbers* module, you must instantiate an object of class *NumberService*. This simplifies the process of providing customizing the modules, such as when providing a specific timezone under which *DateService* should parse text.
