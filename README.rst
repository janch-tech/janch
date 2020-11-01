About Janch
===========

Janch is a utility that can be customized for checking anything.
It reads what it needs to check from a YAML file.


Features
--------

I just started the tool so the features are limited.

1. Run a linux command and inspect its output
2. Run a grep command and inspect its output
3. Gather content of a web address (http/https) and inspect the response


Installation
------------

.. code-block:: bash

    pip install janch



Quick Start
-----------

1. Create a YAML such as the following

.. code-block:: bash

    touch sample.yml
    vim sample.yml

.. code-block:: yaml

    command-example:
      gather:
        type: command
        command_str: python --version
      inspect:
        result: ^Python 3\.(.*)$

    grep-example:
      gather:
        type: grep
        filepath: test.env
        search: '='
      inspect:
        result: (.*)=(.*)
        line_count: 1

    webservice-example:
      gather:
        type: http
        url: http://www.example.com
      inspect:
        status: 200





2. Create a sample file for checking

.. code-block:: bash

    touch test.env
    vim test.env

.. code-block::

    # File Content
    Hello=world


3. Run Janch

.. code-block:: bash

    janch run sample.yml

4. You should get an output that looks as follows

.. code-block:: text

    item                            type    field           expected                        actual                          match error
    grep-example                    grep    result          (.*)=(.*)                       Hello=world                     True  False
    grep-example                    grep    line_count      1                               1                               True  False
    grep-example                    grep    error           NOERROR                         NOERROR                         True  False
    command-example                 command result          ^Python 3\.(.*)$                Python 3.8.2                    True  False
    command-example                 command error           NOERROR                         NOERROR                         True  False
    webservice-example              http    status          200                             200                             True  False
    webservice-example              http    error           NOERROR                         NOERROR                         True  False


5. The match column shows which of the items from the yaml behaved as expected






