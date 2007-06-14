# $Id$
# Authority: dries
# Upstream: Chris Winters <chris$cwinters,com>

%define perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`perl -V:installvendorarch`"; echo $installvendorarch)

%define real_name Class-Factory

Summary: Base class for dynamic factory classes
Name: perl-Class-Factory
Version: 1.05
Release: 1
License: Artistic/GPL
Group: Applications/CPAN
URL: http://search.cpan.org/dist/Class-Factory/

Source: http://search.cpan.org/CPAN/authors/id/P/PH/PHRED/Class-Factory-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
BuildRequires: perl, perl(ExtUtils::MakeMaker)

%description
A base class for dynamic factory classes.

%prep
%setup -n %{real_name}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall
%{__rm} -rf %{buildroot}%{perl_archlib} %{buildroot}%{perl_vendorarch}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc Changes README
%doc %{_mandir}/man3/*
%{perl_vendorlib}/Class/Factory.pm

%changelog
* Sun Apr 29 2007 Dries Verachtert <dries@ulyssis.org> - 1.05-1
- Updated to release 1.05.

* Mon Sep 18 2006 Dries Verachtert <dries@ulyssis.org> - 1.04-1
- Updated to release 1.04.

* Wed Mar 22 2006 Dries Verachtert <dries@ulyssis.org> - 1.03-1.2
- Rebuild for Fedora Core 5.

* Sat Apr  9 2005 Dries Verachtert <dries@ulyssis.org> - 1.03-1
- Initial package.
