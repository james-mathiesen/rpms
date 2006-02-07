# $Id$
# Authority: dag

### FIXME: Also include the xine-mms plugin

Summary: MMS stream downloader
Name: mms_client
Version: 0.0.3
Release: 1
License: GPL
Group: Applications/Internet
URL: http://www.geocities.com/majormms/

Source: http://www.geocities.com/majormms/mms_client-%{version}.tar.gz
BuildRoot: %{_builddir}/%{name}-%{version}-%{release}-root

%description
mms_client is a tool to download MMS streams to play them locally.
This can be useful for eg. watching a 300k stream on a 56k connection.

%prep
%setup

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/mmsclient

%changelog
* Fri Jun 10 2005 Wei-Lun <chaoweilun@pcmail.com.tw> - 0.0.3-1
- Initial spec file created.
