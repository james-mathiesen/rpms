# $Id$
# Authority: dries
# Upstream: Bob Faist <bob,faist$gmail,com>

%define perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`perl -V:installvendorarch`"; echo $installvendorarch)

%define real_name WebService-MusicBrainz

Summary: Search the MusicBrainz website
Name: perl-WebService-MusicBrainz
Version: 0.04
Release: 1
License: Artistic/GPL
Group: Applications/CPAN
URL: http://search.cpan.org/dist/WebService-MusicBrainz/

Source: http://search.cpan.org//CPAN/authors/id/B/BF/BFAIST/WebService-MusicBrainz-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
BuildRequires: perl, perl(ExtUtils::MakeMaker)

%description
This module will search the MusicBrainz database through their web service 
and return objects with the found data.

%prep
%setup -n %{real_name}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall
%{__rm} -rf %{buildroot}%{perl_archlib}/perllocal.pod %{buildroot}%{perl_vendorarch}/auto/*/*/.packlist

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc Changes README
%doc %{_mandir}/man3/WebService::MusicBrainz*
%{perl_vendorlib}/WebService/MusicBrainz.pm
%{perl_vendorlib}/WebService/MusicBrainz/

%changelog
* Sun Nov 19 2006 Dries Verachtert <dries@ulyssis.org> - 0.04-1
- Initial package.
