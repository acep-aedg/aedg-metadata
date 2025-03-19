aedg_metadata.gen_meta
======================

.. py:module:: aedg_metadata.gen_meta

.. autoapi-nested-parse::

   Code from the Sandbox Notebook



Attributes
----------

.. autoapisummary::

   aedg_metadata.gen_meta.CONFIG_FILE
   aedg_metadata.gen_meta.METADATA_FILE
   aedg_metadata.gen_meta.new_pkg


Classes
-------

.. autoapisummary::

   aedg_metadata.gen_meta.AedgOemetadata


Functions
---------

.. autoapisummary::

   aedg_metadata.gen_meta.check_schema


Module Contents
---------------

.. py:class:: AedgOemetadata

   .. attribute:: config

      configuration info for metadata generation

      :type: dict

   .. attribute:: package

      data package metadata conforming to the OEMetadata standard

      :type: dict


   .. py:method:: add_fields() -> None

      Add the fields



   .. py:method:: add_license() -> None

      Add the license



   .. py:method:: apply_config() -> None

      Copy in configs specific to this file



   .. py:method:: generate() -> None

      Run all the steps



   .. py:method:: prep_aedg() -> None

      Make some basic changes that will be true of all AEDG metadata



   .. py:attribute:: all_alaska_bb


   .. py:attribute:: data_package


.. py:function:: check_schema(package: dict[Any, Any]) -> None

   Function from OEMetadata to check schema against standard


.. py:data:: CONFIG_FILE
   :value: '../config/public/public_communities_monthly_generation.yml'


.. py:data:: METADATA_FILE
   :value: '../../metadata/public/public_communities_monthly_generation.json'


.. py:data:: new_pkg
