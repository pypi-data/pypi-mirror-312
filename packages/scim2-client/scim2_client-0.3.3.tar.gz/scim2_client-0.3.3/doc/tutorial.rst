Tutorial
--------

Initialization
==============

scim2-client depends on request engines such as `httpx <https://github.com/encode/httpx>`_ to perform network requests.
This tutorial demonstrate how to use scim2-client with httpx, and suppose you have installed the `httpx` extra for example with ``pip install scim2-models[httpx]``.

As a start you will need to instantiate a httpx :code:`Client` object that you can parameter as your will, and then pass it to a :class:`SCIM client <scim2_client.BaseSCIMClient>` object.
In addition to your SCIM server root endpoint, you will probably want to provide some authorization headers through the httpx :code:`Client` :code:`headers` parameter:

.. code-block:: python

    from httpx import Client
    from scim2_models import User, EnterpriseUserUser, Group
    from scim2_client.engines.httpx import SyncSCIMClient

    client = Client(base_url="https://auth.example/scim/v2", headers={"Authorization": "Bearer foobar"})
    scim = SyncSCIMClient(client, resource_models=(User[EnterpriseUser], Group))

You need to give to indicate to :class:`~scim2_client.BaseSCIMClient` all the different :class:`~scim2_models.Resource` types that you will need to manipulate with the :code:`resource_models` parameter.
This is needed so scim2-client will be able to guess which resource type to instante when an arbitrary payload is met.

.. todo::

    We plan to implement the automatic discovery of SCIM server resources,
    so they can dynamically be used without explicitly passing them with the :code:`resource_models` parameter.

Performing actions
==================

scim2-client allows your application to interact with a SCIM server as described in :rfc:`RFC7644 §3 <7644#section-3>`, so you can read and manage the resources.
The following actions are available:

- :meth:`~scim2_client.BaseSyncSCIMClient.create`
- :meth:`~scim2_client.BaseSyncSCIMClient.query`
- :meth:`~scim2_client.BaseSyncSCIMClient.replace`
- :meth:`~scim2_client.BaseSyncSCIMClient.delete`
- :meth:`~scim2_client.BaseSyncSCIMClient.search`

Have a look at the :doc:`reference` to see usage examples and the exhaustive set of parameters, but generally it looks like this:

.. code-block:: python

    from scim2_models import Error

    request = User(user_name="bjensen@example.com")
    response = scim.create(request)
    if isinstance(response, Error):
        raise SomethingIsWrong(response.detail)

    return f"User {user.id} have been created!"

.. note::

    PATCH modification and bulk operation request are not yet implement,
    but :doc:`any help is welcome! <contributing>`

Request and response validation
===============================

By default, the data passed to the :class:`SCIM client <scim2_client.BaseSCIMClient>` as well as the server response will be validated against the SCIM specifications, and will raise an error if they don't respect them.
However sometimes you want to accept invalid inputs and outputs.
To achieve this, all the methods provide the following parameters, all are :data:`True` by default:

- :paramref:`~scim2_client.BaseSCIMClient.check_request_payload`:
  If :data:`True` (the default) a :class:`~pydantic.ValidationError` will be raised if the input does not respect the SCIM standard.
  If :data:`False`, input is expected to be a :data:`dict` that will be passed as-is in the request.
- :paramref:`~scim2_client.BaseSCIMClient.check_response_payload`:
  If :data:`True` (the default) a :class:`~pydantic.ValidationError` will be raised if the server response does not respect the SCIM standard.
  If :data:`False` the server response is returned as-is.
- :code:`expected_status_codes`: The list of expected status codes in the response.
  If :data:`None` any status code is accepted.
  If an unexpected status code is returned, a :class:`~scim2_client.errors.UnexpectedStatusCode` exception is raised.
- :paramref:`~scim2_client.BaseSCIMClient.raise_scim_errors`: If :data:`True` (the default) and the server returned an :class:`~scim2_models.Error` object, a :class:`~scim2_client.SCIMResponseErrorObject` exception will be raised.
  If :data:`False` the error object is returned.


.. tip::

   Check the request :class:`Contexts <scim2_models.Context>` to understand
   which value will excluded from the request payload, and which values are
   expected in the response payload.

Engines
=======

scim2-client comes with a light abstraction layers that allows for different requests engines.
Currently those engines are shipped:

- :class:`~scim2_client.engines.httpx.SyncSCIMClient`: A synchronous engine using `httpx <https://github.com/encode/httpx>`_ to perform the HTTP requests.
- :class:`~scim2_client.engines.httpx.AsyncSCIMClient`: An asynchronous engine using `httpx <https://github.com/encode/httpx>`_ to perform the HTTP requests. It has the very same API than its synchronous version, except it is asynchronous.
- :class:`~scim2_client.engines.werkzeug.TestSCIMClient`: A test engine for development purposes.
  It takes a WSGI app and directly execute the server code instead of performing real HTTP requests.
  This is faster in unit test suites, and helpful to catch the server exceptions.

You can easily implement your own engine by inheriting from :class:`~scim2_client.BaseSCIMClient`.

Additional request parameters
=============================

Any additional parameter will be passed to the underlying engine methods.
This can be useful if you need to explicitly pass a certain URL for example:

.. code-block:: python

   scim.query(url="/User/i-know-what-im-doing")
