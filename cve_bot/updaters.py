import json
import logging

import requests
from sqlalchemy import select
from sqlalchemy.orm import Session
from telegram.ext import CallbackContext

from cve_bot import db
from cve_bot.models import CVE, Notification, Package, PackageCVE, Subscription
from cve_bot.perf import track

logger = logging.getLogger(__name__)


INFO_URL = "https://security-tracker.debian.org/tracker/data/json"


def _get_all_db_packages(session):
    stmt = select(Package.name)
    return {retval[0] for retval in session.execute(stmt)}


def _get_all_db_cve(session):
    stmt = select(CVE)
    return {result_row[0].name: result_row[0] for result_row in session.execute(stmt)}


def _get_all_db_package_cve(session):
    result_set = session.execute(select(PackageCVE))
    return {result_row[0].pk: result_row[0] for result_row in result_set}


def _extract_cve_field_values(security_info, package_name, cve_name):
    return {
        "scope": security_info[package_name][cve_name].get("scope", ""),
        "description": security_info[package_name][cve_name].get("description", ""),
        "debianbug": security_info[package_name][cve_name].get("debianbug"),
    }


def _extract_package_cve_filed_values(security_info, package_name, cve_name):
    cve_info = security_info[package_name][cve_name]
    return {
        "sid_status": cve_info["releases"].get("sid", {}).get("status", ""),
        "sid_urgency": cve_info["releases"].get("sid", {}).get("urgency", ""),
        "sid_fixed_version": cve_info["releases"].get("sid", {}).get("fixed_version", ""),
        "bullseye_status": cve_info["releases"].get("bullseye", {}).get("status", ""),
        "bullseye_urgency": cve_info["releases"].get("bullseye", {}).get("urgency", ""),
        "bullseye_fixed_version": cve_info["releases"].get("bullseye", {}).get("fixed_version", ""),
        "stretch_status": cve_info["releases"].get("stretch", {}).get("status", ""),
        "stretch_urgency": cve_info["releases"].get("stretch", {}).get("urgency", ""),
        "stretch_fixed_version": cve_info["releases"].get("stretch", {}).get("fixed_version", ""),
        "buster_status": cve_info["releases"].get("buster", {}).get("status", ""),
        "buster_urgency": cve_info["releases"].get("buster", {}).get("urgency", ""),
        "buster_fixed_version": cve_info["releases"].get("buster", {}).get("fixed_version", ""),
    }


@track(10)
def _create_packages(db_engine, security_info):
    with Session(db_engine) as session:
        db_packages = _get_all_db_packages(session)
        current_packages = set(security_info.keys())
        for package_name in list(current_packages - db_packages):
            logger.info("Add %s package to DB", package_name)
            session.add(Package(name=package_name))
        session.commit()


@track(10)
def _create_cve(db_engine, security_info):  # noqa: WPS210
    with Session(db_engine) as session:
        db_cve = _get_all_db_cve(session)
        for package_name in security_info:
            for cve_name in security_info[package_name]:
                field_values = _extract_cve_field_values(security_info, package_name, cve_name)
                current_cve = db_cve.get(cve_name)
                if current_cve is not None:
                    current_cve.set_values(**field_values)
                else:
                    logger.info("Add %s CVE to DB", cve_name)
                    db_cve[cve_name] = CVE(
                        name=cve_name,
                        **field_values,
                    )
                    session.add(db_cve[cve_name])
        session.commit()


def _create_notifications(session, package_cve, changes):
    for prop in changes:  # noqa: WPS503
        if changes[prop]["old"] != changes[prop]["new"]:
            break
    else:
        return
    changes = json.dumps(changes)
    stmt = select(Subscription).where(Subscription.cve_name == package_cve.cve_name)
    for subscription in session.execute(stmt).scalars().all():
        notification = Notification(
            subscription=subscription, information=changes, package_name=package_cve.package_name
        )
        logger.info("Create notification: %s", notification)
        session.add(notification)


@track(10)
def _create_package_cve(db_engine, security_info):  # noqa: WPS210
    with Session(db_engine) as session:
        db_package_cve = _get_all_db_package_cve(session)
        for package_name in security_info:
            logger.debug("Process %s package", package_name)
            for cve_name in security_info[package_name]:
                logger.debug("Process %s for %s", cve_name, package_name)
                field_values = _extract_package_cve_filed_values(security_info, package_name, cve_name)
                current_pk = PackageCVE.get_pk(package_name, cve_name)
                current_package_cve = db_package_cve.get(current_pk)
                if current_package_cve is not None:
                    _create_notifications(session, current_package_cve, current_package_cve.set_values(**field_values))
                else:
                    logger.info("Add package(%s) <-> CVE(%s) relation", package_name, cve_name)
                    db_package_cve[current_pk] = PackageCVE(
                        cve_name=cve_name,
                        package_name=package_name,
                        **field_values,
                    )
                    session.add(db_package_cve[current_pk])
        session.commit()


def debian_update(_: CallbackContext):
    response = requests.get(INFO_URL)
    response.raise_for_status()
    packages = response.json()

    db_engine = db.get_engine()
    _create_packages(db_engine, packages)
    _create_cve(db_engine, packages)
    _create_package_cve(db_engine, packages)
