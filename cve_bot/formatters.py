import json


def format_cve(cve):
    return f"<b>{cve.name}</b>\n<code>{cve.description}</code>\n"


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
    return f"""<b>{package_cve.package_name}</b>
    <i>stretch:</i>
         status: <code>{package_cve.stretch_status}</code>
         urgency: <code>{package_cve.stretch_urgency}</code>
         fixed_version: <code>{package_cve.stretch_fixed_version}</code>
    <i>buster:</i>
         status: <code>{package_cve.buster_status}</code>
         urgency: <code>{package_cve.buster_urgency}</code>
         fixed_version: <code>{package_cve.buster_fixed_version}</code>
    <i>bullseye:</i>
         status: <code>{package_cve.bullseye_status}</code>
         urgency: <code>{package_cve.bullseye_urgency}</code>
         fixed_version: <code>{package_cve.bullseye_fixed_version}</code>
    <i>sid:</i>
         status: <code>{package_cve.sid_status}</code>
         urgency: <code>{package_cve.sid_urgency}</code>
         fixed_version: <code>{package_cve.sid_fixed_version}</code>
"""


def _format_notification_cve_property(cve_info, prop):
    old = cve_info[prop]["old"]
    new = cve_info[prop]["new"]
    if old == new:
        return new
    return f"<s>{old}</s> -> <b>{new}</b>"


def format_notification(notification):
    cve_info = json.loads(notification.information)
    return f"""<b>{notification.package_name}</b>
    <i>stretch:</i>
         status: {_format_notification_cve_property(cve_info, 'stretch_status')}
         urgency: {_format_notification_cve_property(cve_info, 'stretch_urgency')}
         fixed_version: {_format_notification_cve_property(cve_info, 'stretch_fixed_version')}
    <i>buster:</i>
         status: {_format_notification_cve_property(cve_info, 'buster_status')}
         urgency: {_format_notification_cve_property(cve_info, 'buster_urgency')}
         fixed_version: {_format_notification_cve_property(cve_info, 'buster_fixed_version')}
    <i>bullseye:</i>
         status: {_format_notification_cve_property(cve_info, 'bullseye_status')}
         urgency: {_format_notification_cve_property(cve_info, 'bullseye_urgency')}
         fixed_version: {_format_notification_cve_property(cve_info, 'bullseye_fixed_version')}
    <i>sid:</i>
         status: {_format_notification_cve_property(cve_info, 'sid_status')}
         urgency: {_format_notification_cve_property(cve_info, 'sid_urgency')}
         fixed_version: {_format_notification_cve_property(cve_info, 'sid_fixed_version')}
"""


def format_my_subscriptions(subscriptions):
    reply_text = ""
    for subscription in subscriptions:
        reply_text = "{reply_text}\n{formatted_cve}\n".format(
            reply_text=reply_text, formatted_cve=format_cve(subscription.cve)
        )
    return reply_text
