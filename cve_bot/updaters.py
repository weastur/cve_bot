import logging

import requests
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from cve_bot import db
from cve_bot.models import CVE, Package, PackageCVE

logger = logging.getLogger(__name__)


INFO_URL = "https://security-tracker.debian.org/tracker/data/json"


def _get_all_db_packages(session):
    stmt = select(Package.name)
    return {retval[0] for retval in session.execute(stmt)}


def _get_all_db_cve(session):
    stmt = select(CVE.name)
    return {retval[0] for retval in session.execute(stmt)}


def _get_all_debian_cve(security_info):
    current_cve = []
    for cve in security_info.values():
        current_cve.extend(cve.keys())
    return set(current_cve)


def _create_packages(db_engine, security_info):
    with Session(db_engine) as session:
        db_packages = _get_all_db_packages(session)
        current_packages = set(security_info.keys())
        for package_name in list(current_packages - db_packages):
            session.add(Package(name=package_name))
        session.commit()


def _create_cve(db_engine, security_info):  # noqa: WPS210
    with Session(db_engine) as session:
        diff = _get_all_debian_cve(security_info) - _get_all_db_cve(session)
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
                    stmt = update(CVE).where(CVE.name == cve_name).values(**fields_values)  # noqa: WPS221
                    session.execute(stmt)
            session.commit()


def _create_package_cve(db_engine, security_info):
    with Session(db_engine) as session:
        for package_name in security_info:
            for cve_name in security_info[package_name]:
                exists = (
                    session.query(PackageCVE).filter_by(cve_name=cve_name, package_name=package_name).count() == 1
                )  # noqa: WPS221
                field_values = {
                    "sid_status": security_info[package_name][cve_name]["releases"]
                    .get("sid", {})
                    .get("status", ""),  # noqa: WPS221
                    "sid_urgency": security_info[package_name][cve_name]["releases"]
                    .get("sid", {})
                    .get("urgency", ""),  # noqa: WPS221
                    "sid_fixed_version": security_info[package_name][cve_name]["releases"]
                    .get("sid", {})
                    .get("fixed_version", ""),
                    "bullseye_status": security_info[package_name][cve_name]["releases"]
                    .get("bullseye", {})
                    .get("status", ""),
                    "bullseye_urgency": security_info[package_name][cve_name]["releases"]
                    .get("bullseye", {})
                    .get("urgency", ""),
                    "bullseye_fixed_version": security_info[package_name][cve_name]["releases"]
                    .get("bullseye", {})
                    .get("fixed_version", ""),
                    "stretch_status": security_info[package_name][cve_name]["releases"]
                    .get("stretch", {})
                    .get("status", ""),
                    "stretch_urgency": security_info[package_name][cve_name]["releases"]
                    .get("stretch", {})
                    .get("urgency", ""),
                    "stretch_fixed_version": security_info[package_name][cve_name]["releases"]
                    .get("stretch", {})
                    .get("fixed_version", ""),
                    "buster_status": security_info[package_name][cve_name]["releases"]
                    .get("buster", {})
                    .get("status", ""),
                    "buster_urgency": security_info[package_name][cve_name]["releases"]
                    .get("buster", {})
                    .get("urgency", ""),
                    "buster_fixed_version": security_info[package_name][cve_name]["releases"]
                    .get("buster", {})
                    .get("fixed_version", ""),
                }
                if exists:
                    session.execute(
                        update(PackageCVE)
                        .where(PackageCVE.cve_name == cve_name and PackageCVE.package_name == package_name)
                        .values(**field_values)
                    )
                else:
                    session.add(PackageCVE(cve_name=cve_name, package_name=package_name, **field_values))
                session.commit()


def debian_update():
    response = requests.get(INFO_URL)
    response.raise_for_status()
    packages = response.json()

    db_engine = db.get_engine()
    _create_packages(db_engine, packages)
    _create_cve(db_engine, packages)
    _create_package_cve(db_engine, packages)
