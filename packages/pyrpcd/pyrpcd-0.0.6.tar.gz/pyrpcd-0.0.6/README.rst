pyrpcd
=================================

Pyrpcd is a RPC server, implemented by tornado framework.
Expose all functions of a python module in current directory.
Use voxe as data transporting protocol.

Usage
------------

Install::

    python -m pyrpcd.server hello.py


hello.py


.. code:: python

    def print_hello():
        print('hello ...')

    def remote_add(a, b):
        return a + b

main.py

.. code:: python

    import requests
    import voxe

    response = requests.post('http://127.0.0.1:8080/rpc/print_hello')
    response = requests.post('http://127.0.0.1:8080/rpc/remote_add', voxe.dumps(2, 3))
    print(voxe.loads(response.content))

Run::

    python main.py