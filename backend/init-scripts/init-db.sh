#!/bin/bash

# Crear la base de datos y tablas usando el archivo SQL
mysql -u user -psecret < /podman-entrypoint-initdb.d/bdvirtus.sql
