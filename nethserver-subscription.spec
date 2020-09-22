Summary: NethServer Subscriptions
Name: nethserver-subscription
Version: 3.6.3
Release: 1%{?dist}
License: GPL
URL: %{url_prefix}/%{name}
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

Provides: nethserver-alerts = %{version} 
Obsoletes: nethserver-alerts < %{version}

BuildRequires: nethserver-devtools
BuildRequires: gettext
BuildRequires: python2-devel

Requires: nethserver-base
Requires: nethserver-yum-cron
Requires: nethserver-collectd
Requires: nethserver-lib
Requires: python-requests
Requires: curl
Requires: jq
Requires: %{name}-inventory

# HACK: allow upgrade from NS 7.7 where sclo-php71-php-pecl-imagick was installed
Obsoletes: sclo-php71-php-pecl-imagick <= 3.4.4

%description
NethServer Subscriptions

%prep
%setup -q

%build
%{makedocs}
perl createlinks
mkdir -p root%{python2_sitelib}
cp -a lib/nethserver_alerts.py root%{python2_sitelib}

%install
(cd root; find . -depth -print | sed \
        -e '\|^/opt| d' \
        -e '\|/etc/cron.daily/nethserver-inventory| d' \
        -e '\|/usr/sbin/nethserver-inventory| d' \
        -e '\|/usr/sbin/ardad| d' \
        -e '\|/etc/e-smith/events/actions/nethserver-inventory-send| d' \
    | cpio -dump %{buildroot})
%{genfilelist} \
    --file /etc/sudoers.d/20_nethserver_subscription 'attr(0440,root,root)' \
    %{buildroot} > filelist

# 1. Split UI parts from core package
grep -E ^%{_nsuidir}/ filelist > filelist-ui
grep -vE ^%{_nsuidir}/ filelist > filelist-core

# 2. Move Alerts UI back to core:
grep -F Alerts filelist-ui >> filelist-core
sed -i '/Alerts/ d' filelist-ui

%files -f filelist-core
%defattr(-,root,root)
%doc COPYING
%doc README.rst
%dir %{_nseventsdir}/%{name}-update

%package ui
Summary: NethServer Subscriptions UI
Requires: %{name} = %{version}-%{release}
%description ui
NethServer Subscriptions UI
%files ui -f filelist-ui
%defattr(-,root,root)
%doc COPYING
%doc README.rst

%changelog
* Fri Sep 18 2020 Davide Principi <davide.principi@nethesis.it> - 3.6.3-1
- Collect facts for systemd restart (on-failure) events - nethesis/dev#5854

* Fri Jul 17 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.6.2-1
- Cockpit: enhance rebranding - nethesis/dev#5843

* Wed May 06 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.6.1-1
- Upgrade blocked by sclo-php71-php-pecl-imagick - Bug NethServer/dev#6156

* Tue May 05 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.6.0-1
- NethServer 7.8.2003

* Wed Mar 18 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.5.4-1
- Bad sudoers permission - Bug NethServer/dev#6081

* Mon Nov 04 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.5.3-1
- inventory: suppress backup warning (#29) - Nethserver/dev#5880

* Fri Oct 25 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.5.2-1
- Subscription: last backup not reported inside inventory - NethServer/dev#5880

* Tue Oct 15 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.5.1-1
- Nethserver-cockpit is not installable - Bug NethServer/arm-dev#32

* Tue Oct 01 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.5.0-1
- New NethServer 7.7.1908 defaults - NethServer/dev#5831

* Wed Mar 06 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.4.1-1
- Restore config regression with ultimate software origin policy - Bug NethServer/dev#5724

* Fri Feb 22 2019 Davide Principi <davide.principi@nethesis.it> - 3.4.0-1
- Ultimate software origin policy - NethServer/dev#5704

* Thu Feb 14 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.3.4-1
- hide PSK content: PSK is a sensitive content which must be redacted - nethserver-subscription#22
- fix backup info type: the value was read from obsolete configuration key - nethserver-subscription#22

* Thu Jan 31 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.3.3-1
- Remove single backup data - NethServer/dev#5691

* Fri Jan 11 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.3.2-1
- Make sure subscription.repo is disabled - NethServer/dev#5676

* Thu Jan 10 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.3.1-1
- Subscription: implement unsubscribe - NethServer/dev#5688

* Fri Dec 21 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.3.0-1
- Cockpit: support Community and Enterprise registration - NethServer/dev#5676

* Fri Dec 07 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.2.1-1
- Repository metadata GPG signature - NethServer/dev#5664

* Wed Dec 05 2018 Davide Principi <davide.principi@nethesis.it> - 3.2.0-1
- Bump distro version 7.6.1810
- New firmware fact -- NethServer/nethserver-subscription#17

* Fri Oct 05 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.1.2-1
- Inventory: no info about primary backup - Bug NethServer/dev#5598

* Thu Aug 30 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.1.1-1
- Backup-data: multiple schedule and backends - NethServer/dev#5538

* Wed May 30 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.1.0-1
- Software update policy API - NethServer/dev#5505

* Mon May 21 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.0.3-1
- Release NS 7.5.1804

* Fri Apr 27 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.0.2-1
- Custom Alerts hysteresis value - NethServer/dev#5458

* Thu Mar 29 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.0.1-1
- ns6upgrade cannot access Enterprise repositories - Bug Nethesis/dev#5364

* Mon Mar 19 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.0.0-1
- Implement clients for NethServer Subscriptions - NethServer/dev#5425

* Tue Mar 13 2018 Davide Principi <davide.principi@nethesis.it> - 3.0.0-0.1
- Development version (merge nethserver-alerts)
