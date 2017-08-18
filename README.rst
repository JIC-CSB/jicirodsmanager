JIC iRODS manager
=================

Python tools to manage users/groups/quotas/namespaces in the iRODS zones.

These tools have been implemented to solve the specific problem of managing
users and groups in iRODS at the John Innes Centre. Although it is JIC specific
the implementation details may be of interest to other iRODS users that want to
organise iRODS zones into research groups where members are allowed to write
data.


Overview
--------

Below is an overview of what the structure that this tool is meant to support

- Individual users do not have home directories (this has to be explicitly
  disabled during the setup of the iRODS zone)
- Each research group has a named collection
- Each research group owns its collection

Th latter enables the members of the group to share their data with other users
in the zone without having to involve a systems administrator.


Usage
-----

To add a user to an iRODS zone install this software on the zone VM and run the
command below.

::

    irods-useradd olssont rg-matthew-hartley

If the group (``rg-matthew-hartley``) does not exist an appropriate error
message will appear.

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
4. It gives the ``rg-matthew-hartley`` group ownership permissions on the
   ``/rg-matthew-hartley`` collection

*Warning:* at the moment the quota functionality in iRODS does not appear to be
doing anything.

Once the group exists one can add users that belong to that group to the zone.

::

    irods-useradd olssont rg-matthew-hartley

The command above does two things.

1. It creates the user ``olssont``
2. It adds the user ``olssont`` to the ``rg-matthew-hartley`` group


Installation
------------

To install the jicirodsmanager package log into the iRODS zone server and clone this
repository in /opt, e.g.

::

    ssh root@jic-datazone.irods.nbi.ac.uk
    cd /opt
    git clone https://github.com/JIC-CSB/jicirodsmanager.git

The ``irods-useradd`` and ``irods-groupadd`` commands will then be available from the
``/opt/jicirodsmanager/bin`` directory.


Technical details
-----------------

The logic for managing users and groups resides in the base class
``jicirodsmanager.StorageManager`` and is subclassed by
``jicirodsmanager.irods.IrodsStorageManager`` which provides a specific
implementation for iRODS.

The specific iRODS implementation shells out commands using the
``jicirodsmanager.CommandWrapper`` class. This is used for logging
the commands that get shelled out and to catch errors from the
issued commands.

The scripts in the ``bin`` directory make use of the ``jicirodsmanager/cli.py``
script. In order to make this work from any location it needs to add the cloned
``jicirodsmanager`` repository to the ``PYTHONPATH`` environment variable. This
is achieved using the shim below::

    MYPATH=`realpath $0`
    BINPATH=`dirname $MYPATH`
    PACKAGEPATH=`dirname $BINPATH`
    export PYTHONPATH=$PYTHONPATH:$PACKAGEPATH

The command is then built up, for example in ``bin/irods-useradd`` this takes
the form of the below::

    CMD="python $PACKAGEPATH/jicirodsmanager/cli.py adduser $@"

When issuing iRODS commands one needs to be logged in as the ``irods``
user on the iRODS zone. However, one does not always SSH into the
server as the irods user and it can be a pain to have to remember to
become the iRODS user before making use of this tool. The ``irods-useradd``
and ``irods-groupadd`` bash scripts in the ``bin`` directory take care
of this using the shim below::

    if [ `whoami` == "irods" ]
    then
            $CMD
    else
            su irods -c "$CMD"
    fi


Notes from experiments on the command line
------------------------------------------

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

Finding the zone name programatically
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get the iRODS zone name using Python:

::

    irods_envfile = os.path.expanduser('~/.irods/irods_environment.json')
    irods_zone_name = json.load(open(irods_envfile))['irods_zone_name']
