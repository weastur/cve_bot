insert into cve (name, description, scope, debianbug) values ('CVE-2021-0003', 'description', 'scope', 'bug');
insert into cve (name, description, scope, debianbug) values ('CVE-2021-0002', 'description', 'scope', 'bug');
insert into cve (name, description, scope, debianbug) values ('CVE-2021-0001', 'description', 'scope', 'bug');

insert into packages (name) values ('package0');
insert into packages (name) values ('package1');
insert into packages (name) values ('package2');

insert into subscriptions (id, chat_id) values (1, 1);
insert into subscriptions (id, chat_id) values (2, 2);
insert into subscriptions (id, chat_id) values (3, 3);

insert into package_cve (package_name, cve_name, sid_status, sid_urgency, sid_fixed_version, bullseye_status, bullseye_urgency, bullseye_fixed_version, buster_status, buster_urgency, buster_fixed_version, stretch_status, stretch_urgency, stretch_fixed_version) values ('package0', 'CVE-2021-0001', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0');
insert into package_cve (package_name, cve_name, sid_status, sid_urgency, sid_fixed_version, bullseye_status, bullseye_urgency, bullseye_fixed_version, buster_status, buster_urgency, buster_fixed_version, stretch_status, stretch_urgency, stretch_fixed_version) values ('package1', 'CVE-2021-0001', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0');
insert into package_cve (package_name, cve_name, sid_status, sid_urgency, sid_fixed_version, bullseye_status, bullseye_urgency, bullseye_fixed_version, buster_status, buster_urgency, buster_fixed_version, stretch_status, stretch_urgency, stretch_fixed_version) values ('package2', 'CVE-2021-0001', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0');
insert into package_cve (package_name, cve_name, sid_status, sid_urgency, sid_fixed_version, bullseye_status, bullseye_urgency, bullseye_fixed_version, buster_status, buster_urgency, buster_fixed_version, stretch_status, stretch_urgency, stretch_fixed_version) values ('package0', 'CVE-2021-0002', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0');
insert into package_cve (package_name, cve_name, sid_status, sid_urgency, sid_fixed_version, bullseye_status, bullseye_urgency, bullseye_fixed_version, buster_status, buster_urgency, buster_fixed_version, stretch_status, stretch_urgency, stretch_fixed_version) values ('package1', 'CVE-2021-0002', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0');
insert into package_cve (package_name, cve_name, sid_status, sid_urgency, sid_fixed_version, bullseye_status, bullseye_urgency, bullseye_fixed_version, buster_status, buster_urgency, buster_fixed_version, stretch_status, stretch_urgency, stretch_fixed_version) values ('package0', 'CVE-2021-0003', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0', 'unresolved', 'unimportant', '0');

insert into subscription_cve (cve_name, subscription_id) values ('CVE-2021-0001', 1);
insert into subscription_cve (cve_name, subscription_id) values ('CVE-2021-0002', 1);
insert into subscription_cve (cve_name, subscription_id) values ('CVE-2021-0003', 1);
insert into subscription_cve (cve_name, subscription_id) values ('CVE-2021-0001', 2);
insert into subscription_cve (cve_name, subscription_id) values ('CVE-2021-0002', 2);
insert into subscription_cve (cve_name, subscription_id) values ('CVE-2021-0001', 3);

insert into notifications (id, subscription_id, package_name, information) values (1, 1, 'package2', '{"buster_fixed_version": {"old": "0", "new": "1"}}');
insert into notifications (id, subscription_id, package_name, information) values (2, 2, 'package1', '{"buster_fixed_version": {"old": "0", "new": "1"}}');
insert into notifications (id, subscription_id, package_name, information) values (3, 3, 'package0', '{"buster_fixed_version": {"old": "0", "new": "1"}}');
