%global debug_package %{nil}

Summary: NethServer Subscriptions inventory agent
Name: nethserver-subscription-inventory
Version: 3.5.0
Release: 1%{?dist}
License: GPL
URL: %{url_prefix}/nethserver-subscription
Source0: %{name}-%{version}.tar.gz
BuildRequires: nethserver-devtools

%ifarch x86_64
Requires: puppet-agent
%endif

Provides: nethserver-inventory = %{version}
Obsoletes: nethserver-inventory < %{version}

%description
NethServer Subscriptions inventory collects system facts and sends them every 
day to a centralized server

%prep
%setup -q

%build
mkdir createlinks.d
(cd createlinks.d; perl ../createlinks-inventory)

%install
touch %{name}-filelist
%ifarch x86_64
install -m 0755 -D -T root/etc/cron.daily/nethserver-inventory %{buildroot}/etc/cron.daily/nethserver-inventory
install -m 0755 -D -T root/usr/sbin/nethserver-inventory %{buildroot}/usr/sbin/nethserver-inventory
install -m 0755 -D -T root/usr/sbin/ardad %{buildroot}/usr/sbin/ardad
install -m 0755 -D -T root/etc/e-smith/events/actions/nethserver-inventory-send %{buildroot}/etc/e-smith/events/actions/nethserver-inventory-send
cp -av root/opt %{buildroot}/opt
(cd %{buildroot}; find . -type f | sed 's/^\.//' ) >> %{name}-filelist

(cd createlinks.d/root; find . -depth -print | cpio -dump %{buildroot})
(cd createlinks.d/root; find . -not -type d | sed 's/^\.//' ) >> %{name}-filelist
%endif

%files -f %{name}-filelist
%defattr(-,root,root)
%doc COPYING
%doc README.rst

