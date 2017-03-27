JIC iRODS manager
=================

Python tools to manage users/groups/quotas/namespaces in an iRODS zone.

Usage
-----

To add a user to an iRODS zone install this software on the zone VM and run the command below.

::

    irods-useradd olssont rg-matthew-hartley

If the group (``rg-matthew-hartley``) does not exist an appropriate error message will appear.

::
    The group rg-matthew-hartley does not exit.
    Please create it first using the irods-groupadd command.

To create a group run the command below.

::

    irods-groupadd rg-matthew-hartley 5497558138880

The command above does three things:

1. It creates the group ``rg-matthew-hartley`` in the zone
2. It sets the group quota to 5Tb
3. It creates the collection ``/rg-matthew-hartley`` 
4. It gives the ``rg-matthew-hartley`` group permissions to write to the
   ``/rg-matthew-hartley`` collection

Once the group exists one can add users that belong to that group to the zone.

::

    irods-useradd olssont rg-matthew-hartley

The command above does two things.

1. It creates the user ``olssont``
2. It adds the user ``olssont`` to the ``rg-matthew-hartley`` group

Outstanding questions
~~~~~~~~~~~~~~~~~~~~~

- Should it be possible to create groups without a quota?
- Should it be possible to add users without a group?
- Should it be possible to add a user to a second group?


Installation
------------
To install the jicirodsmanager package.

::

    cd jicirodsmanager
    python setup.py install
