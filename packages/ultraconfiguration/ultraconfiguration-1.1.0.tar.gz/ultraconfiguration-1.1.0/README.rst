UltraConfiguration
===========

A high-performance, thread-safe configuration management library for Python with async support.

Features
--------

- Thread-safe singleton configuration manager
- Support for JSON and YAML formats
- Nested configuration access using dot notation
- LRU caching for fast repeated access
- Comprehensive error handling and logging
- Type hints for better IDE support
- Optional schema validation
- Pretty-printing support
- Async/Background operations support
- Memory-efficient caching
- Context manager support

Installation
------------

.. code-block:: bash

    pip install ultraconfiguration

Quick Start
-----------

.. code-block:: python

    from ultraconfiguration import UltraConfig

    # Basic usage
    config = UltraConfig()
    config.load_config('config.json')
    db_host = config.get('database.host', 'localhost')
    config.set('app.debug', True)
    config.save_config('config.json')

    # Using as context manager
    with UltraConfig() as config:
        config.load_config('config.json')
        config.set('app.name', 'MyApp')

Async Support
-------------

.. code-block:: python

    import asyncio
    from ultraconfiguration import UltraConfig

    async def main():
        config = UltraConfig()
        
        # Async loading
        await config.load_config_async('config.json')
        
        # Background saving
        future = config.save_config_background('config.json')
        
        # Do other work while saving
        print("Saving in background...")
        
        # Wait if needed
        await asyncio.wrap_future(future)

    asyncio.run(main())

Schema Validation
-----------------

.. code-block:: python

    config = UltraConfig()
    config.load_config('config.json', schema_path='schema.json')

Advanced Features
-----------------

### Nested Configuration

.. code-block:: python

    # Setting nested values
    config.set('database.credentials.username', 'admin')

    # Getting nested values with default
    host = config.get('database.host', 'localhost')

### Pretty Printing

.. code-block:: python

    # Save with pretty formatting
    config.save_config('config.json', pretty=True)

### Change Detection

.. code-block:: python

    if config.has_changes():
        config.save_config('config.json')

### Cache Management

.. code-block:: python

    # Clear cached values
    config.clear_cache()

    # Reset entire configuration
    config.reset()

Performance
-----------

- LRU caching for frequently accessed values
- Thread pooling for async operations
- Weak references for memory efficiency
- Optimized file I/O operations

Thread Safety
-------------

All operations are thread-safe and can be used in multi-threaded applications:
- Concurrent read operations
- Synchronized write operations
- Safe async operations

Requirements
------------

- Python 3.7+
- PyYAML
- jsonschema (for schema validation)

License
-------

MIT License with attribution requirement

Contributing
------------

Contributions are welcome! Please feel free to submit a Pull Request.
