import logging

import requests
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from cve_bot import db
from cve_bot.models import CVE, Package, PackageCVE

logger = logging.getLogger(__name__)


INFO_URL = "https://security-tracker.debian.org/tracker/data/json"


def _create_packages(db_engine, security_info):
    with Session(db_engine) as session:
        db_packages = set([name for (name,) in session.execute(select(Package.name)).all()])
        current_packages = set([name for name in security_info.keys()])
        diff = list(current_packages - db_packages)
        for package_name in diff:
            session.add(Package(name=package_name))
        session.commit()


def _create_cve(db_engine, security_info):
    with Session(db_engine) as session:
        db_cve = set([name for (name,) in session.execute(select(CVE.name)).all()])
        current_cve = []
        for cve in security_info.values():
            current_cve.extend(cve.keys())
        current_cve = set(current_cve)
        diff = current_cve - db_cve
        for package_name in security_info:
            for cve_name in security_info[package_name]:
                fields_values = {
                    "scope": security_info[package_name][cve_name].get("scope", ""),
                    "description": security_info[package_name][cve_name].get("description", ""),
                    "debianbug": security_info[package_name][cve_name].get("debianbug"),
                }
                if cve_name in diff:
                    session.add(
                        CVE(
                            name=cve_name,
                            **fields_values,
                        )
                    )
                    diff.remove(cve_name)
                else:
                    session.execute(update(CVE).where(CVE.name == cve_name).values(**fields_values))
            session.commit()


def debian_update():
    response = requests.get(INFO_URL)
    response.raise_for_status()
    packages = response.json()

    db_engine = db.get_engine()
    _create_packages(db_engine, packages)
    _create_cve(db_engine, packages)
