Summary: NethServer Subscriptions
Name: nethserver-subscription
Version: 3.5.0
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
Requires: %{name}-inventory = %{version}-%{release}

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
(cd root; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} --ignoredir '/opt' --ignorefile '/etc/cron.daily/nethserver-inventory' %{buildroot} > filelist

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
%ifarch x86_64
Requires: %{name} = %{version}-%{release}
%endif
%description ui
NethServer Subscriptions UI
%files ui -f filelist-ui
%defattr(-,root,root)
%doc COPYING
%doc README.rst


%changelog
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
