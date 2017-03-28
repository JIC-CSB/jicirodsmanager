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

    The group rg-matthew-hartley does not exist.
    Please create it first using the irods-groupadd command.

To create a group run the command below.

::

    irods-groupadd rg-matthew-hartley 5497558138880

The command above does a number of things:

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

Implementation details
----------------------

On the zone server, become the iRODS user:

::

    su irods

Making the group
~~~~~~~~~~~~~~~~

::

    iadmin mkgroup rg-matthew-hartley

Repetition gives an error:

::

    bash-4.2$ iadmin mkgroup rg-matthew-hartley
    remote addresses: 127.0.0.1 ERROR: rcGeneralAdmin failed with error -809000 CATALOG_ALREADY_HAS_ITEM_BY_THAT_NAME
    Level 0: Error -809000 CATALOG_ALREADY_HAS_ITEM_BY_THAT_NAME
    Level 1: DEBUG:

    bash-4.2$ echo $?
    4

Making the collection
~~~~~~~~~~~~~~~~~~~~~

::

    imkdir /jic_archive/rg-matthew-hartley

Again, repetition gives an error:

::

    bash-4.2$ imkdir /jic_archive/rg-matthew-hartley
    remote addresses: 127.0.0.1 ERROR: mkdirUtil: mkColl of /jic_archive/rg-matthew-hartley error. status = -809000 CATALOG_ALREADY_HAS_ITEM_BY_THAT_NAME
    bash-4.2$ echo $?
    3

Setting permissions on the collection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    ichmod own rg-matthew-hartley /jic_archive/rg-matthew-hartley
    ichmod inherit /jic_archive/rg-matthew-hartley

Note: We use own so that group members can share things by adding other users/groups using ``ichmod``.

Adding users to the group
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    iadmin atg rg-matthew-hartley olssont#nbi
    iadmin atg rg-matthew-hartley hartleym#nbi

Repeatedly adding the same user causes an error:

::

    bash-4.2$     iadmin atg rg-matthew-hartley olssont#nbi
    remote addresses: 127.0.0.1 ERROR: rcGeneralAdmin failed with error -809000 CATALOG_ALREADY_HAS_ITEM_BY_THAT_NAME
    bash-4.2$ echo $?
    4

Brainstorming
-------------

We'll have a StorageManager base class that provides some public functions that are used by the CLI. That way,
the CLI is easily reusable. The public functions will include:

1. Group exists
2. Add user
3. Add group (with an optional argument for specifying group quota, iRODS implementation will always use this).

