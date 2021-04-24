import json


def format_cve(cve):
    return f"{cve.name}\n{cve.description}\n"


def format_cve_with_packages(cve, package_cve):
    return "{cve_info}{package_cve_info}".format(
        cve_info=format_cve(cve), package_cve_info=format_package_cve_list(package_cve)
    )


def format_package_cve_list(package_cve):
    reply_text = ""
    for pkg_cve in package_cve:
        reply_text = "{reply_text}{formatted_pkg_cve}".format(
            reply_text=reply_text,
            formatted_pkg_cve=format_package_cve(pkg_cve),
        )
    return reply_text


def format_package_cve(package_cve):
    return f"""==============================
{package_cve.package_name}
    stretch:
         status: {package_cve.stretch_status}
         urgency: {package_cve.stretch_urgency}
         fixed\_version: {package_cve.stretch_fixed_version}
    buster:
         status: {package_cve.buster_status}
         urgency: {package_cve.buster_urgency}
         fixed\_version: {package_cve.buster_fixed_version}
    bullseye:
         status: {package_cve.bullseye_status}
         urgency: {package_cve.bullseye_urgency}
         fixed\_version: {package_cve.bullseye_fixed_version}
    sid:
         status: {package_cve.sid_status}
         urgency: {package_cve.sid_urgency}
         fixed\_version: {package_cve.sid_fixed_version}
==============================
"""


def _format_notification_cve_property(cve_info, prop):
    old = cve_info[prop]["old"]
    new = cve_info[prop]["new"]
    if old == new:
        return new
    return f"<s>{old}</s> -> <b>{new}</b>"


def format_notification(notification):
    cve_info = json.loads(notification.information)
    return f"""==============================
{notification.package_name}
    stretch:
         status: {_format_notification_cve_property(cve_info, 'stretch_status')}
         urgency: {_format_notification_cve_property(cve_info, 'stretch_urgency')}
         fixed_version: {_format_notification_cve_property(cve_info, 'stretch_fixed_version')}
    buster:
         status: {_format_notification_cve_property(cve_info, 'buster_status')}
         urgency: {_format_notification_cve_property(cve_info, 'buster_urgency')}
         fixed_version: {_format_notification_cve_property(cve_info, 'buster_fixed_version')}
    bullseye:
         status: {_format_notification_cve_property(cve_info, 'bullseye_status')}
         urgency: {_format_notification_cve_property(cve_info, 'bullseye_urgency')}
         fixed_version: {_format_notification_cve_property(cve_info, 'bullseye_fixed_version')}
    sid:
         status: {_format_notification_cve_property(cve_info, 'sid_status')}
         urgency: {_format_notification_cve_property(cve_info, 'sid_urgency')}
         fixed_version: {_format_notification_cve_property(cve_info, 'sid_fixed_version')}
==============================
"""


def format_my_subscriptions(result_cve):
    reply_text = ""
    for cve in result_cve:
        reply_text = "{reply_text}\n{formatted_cve}\n==============================".format(
            reply_text=reply_text, formatted_cve=format_cve(cve)
        )
    return reply_text
