thorlabs_elliptec
=================

This is a python interface to Thorlabs Elliptec series of piezoelectric motion stages and mounts. It
should support all models including:

- Thorlabs Elliptec ELL6 SM1 threaded dual-position slider
- Thorlabs Elliptec ELL7 linear stage
- Thorlabs Elliptec ELL8 rotation stage
- Thorlabs Elliptec ELL9 SM1 threaded four-position slider
- Thorlabs Elliptec ELL10 linear stage
- Thorlabs Elliptec ELL12 SM05 threaded six-position slider
- Thorlabs Elliptec ELL14 SM1 threaded rotation mount
- Thorlabs Elliptec ELL17 28 mm travel linear stage
- Thorlabs Elliptec ELL18 rotation stage
- Thorlabs Elliptec ELL20 60 mm travel linear stage

As of version 1.0, all basic functionality is implemented. Version 1.2 introduces the "multi-drop"
capability which allow multiple devices to share a single serial port device. Note however that only
a single device can be moved at a time due to a limitation with the communications protocol. If
multiple devices must be moved simultaneously, each device must be connected via its own serial port
(such as a dedicated USB to serial adaptor).


Support
-------

Documentation can be found online at `<https://thorlabs-elliptec.readthedocs.io/en/latest>`__.

Source code is hosted at `<https://gitlab.com/ptapping/thorlabs-elliptec>`__.

Bug reports, feature requests and suggestions can be submitted to the `issue tracker
<https://gitlab.com/ptapping/thorlabs-elliptec/-/issues>`__.

The documentation from Thorlabs on the `Elliptec serial communication protocol
<https://www.thorlabs.com/Software/Elliptec/Communications_Protocol/ELLx%20modules%20protocol%20manual_Issue7.pdf>`__
may also be of use.


License
-------

This software is free and open source, licensed under the GNU Public License.
See the `LICENSE <https://gitlab.com/ptapping/thorlabs-elliptec/-/blob/main/LICENSE>`__ for details.