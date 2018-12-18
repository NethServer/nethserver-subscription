Summary: NethServer Subscriptions
Name: nethserver-subscription
Version: 3.2.1
Release: 1%{?dist}
License: GPL
URL: %{url_prefix}/%{name}
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

Provides: nethserver-inventory = %{version}
Obsoletes: nethserver-inventory < %{version}
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
Requires: puppet-agent
Requires: jq

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
%{genfilelist} %{buildroot} > filelist

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
