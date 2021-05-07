from sqlalchemy import select

from cve_bot.models import CVE, Notification, Package, PackageCVE
from cve_bot.updaters import (
    _create_cve,
    _create_notifications,
    _create_package_cve,
    _create_packages,
)


def test_create_packages(db, session):
    feed = {"package0": {}, "package3": {}}
    _create_packages(db["engine"], feed)
    stmt = select(Package.name)
    pkg_names = session.execute(stmt).scalars().all()
    assert sorted(pkg_names) == ["package0", "package1", "package2", "package3"]


def test_create_cve(db, session):
    feed = {
        "package0": {
            "CVE-2021-0004": {"description": "description", "scope": "scope", "releases": {}},
            "CVE-2021-0003": {"description": "description", "scope": "scope", "releases": {}},
        }
    }
    _create_cve(db["engine"], feed)
    stmt = select(CVE.name)
    cve_names = session.execute(stmt).scalars().all()
    assert sorted(cve_names) == ["CVE-2021-0001", "CVE-2021-0002", "CVE-2021-0003", "CVE-2021-0004"]


def test_create_package_cve(db, session):
    feed = {
        "package0": {
            "CVE-2021-0004": {"description": "description", "scope": "scope", "releases": {}},
            "CVE-2021-0003": {"description": "description", "scope": "scope", "releases": {}},
        }
    }
    _create_cve(db["engine"], feed)
    _create_package_cve(db["engine"], feed)
    stmt = select(PackageCVE.cve_name).where(PackageCVE.package_name == "package0")
    cve_names = session.execute(stmt).scalars().all()
    assert sorted(cve_names) == ["CVE-2021-0001", "CVE-2021-0002", "CVE-2021-0003", "CVE-2021-0004"]


def test_create_notifications(session):
    stmt = select(PackageCVE).where(PackageCVE.cve_name == "CVE-2021-0001", PackageCVE.package_name == "package0")
    package_cve = session.execute(stmt).scalars().first()
    changes = {
        "sid_status": {"old": "unresolved", "new": "unresolved"},
        "sid_urgency": {"old": "unimportant", "new": "unimportant"},
        "sid_fixed_version": {"old": "0", "new": "1"},
        "buster_status": {"old": "unresolved", "new": "unresolved"},
        "buster_urgency": {"old": "unimportant", "new": "unimportant"},
        "buster_fixed_version": {"old": "0", "new": "1"},
        "stretch_status": {"old": "unresolved", "new": "unresolved"},
        "stretch_urgency": {"old": "unimportant", "new": "unimportant"},
        "stretch_fixed_version": {"old": "0", "new": "1"},
        "bullseye_status": {"old": "unresolved", "new": "unresolved"},
        "bullseye_urgency": {"old": "unimportant", "new": "unimportant"},
        "bullseye_fixed_version": {"old": "0", "new": "1"},
    }
    _create_notifications(session, package_cve, changes)

    stmt = select(Notification.subscription_id).where(Notification.package_name == "package0")
    subscriptions = session.execute(stmt).scalars().all()
    assert sorted(subscriptions) == [1, 3]
