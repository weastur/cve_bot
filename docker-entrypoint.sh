#!/bin/sh

set -ex

current_dir="$(pwd)"
package_install_dir="$(python -c 'import cve_bot; import os; print(os.path.dirname(cve_bot.__file__))')"

cd "$package_install_dir"
alembic upgrade head

cd "$current_dir"
exec cve_bot
