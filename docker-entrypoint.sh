#!/bin/sh

set -e

alembic upgrade head
exec cve_bot
