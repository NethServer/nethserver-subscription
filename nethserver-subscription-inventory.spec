%global debug_package %{nil}

Summary: NethServer Subscriptions inventory agent
Name: nethserver-subscription-inventory
Version: 3.5.0
Release: 1%{?dist}
License: GPL
URL: %{url_prefix}/nethserver-subscription
Source0: %{name}-%{version}.tar.gz

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
# noop

%install
install -m 0755 -D -T root/etc/cron.daily/nethserver-inventory %{buildroot}/etc/cron.daily/nethserver-inventory
cp -av root/opt %{buildroot}/opt
(cd %{buildroot}; find . -type f | sed 's/^\.//' ) > %{name}-filelist

%ifarch x86_64
%files -f %{name}-filelist
%else
%files
%endif
%defattr(-,root,root)
%doc COPYING
%doc README.rst

