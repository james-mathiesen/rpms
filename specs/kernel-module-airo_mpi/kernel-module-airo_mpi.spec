# $Id$

# Authority: dag
# Upstream: Fabrice Bellet <fabrice@bellet.info>

# Archs: i686 i586 i386 athlon
# Distcc: 0
# Soapbox: 0
# BuildAsUser: 0

%{?rhfc1:%define __cc gcc32}

%define _libmoddir /lib/modules

%{!?kernel:%define kernel %(rpm -q kernel-source --qf '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' | tail -1)}

%define kversion %(echo "%{kernel}" | sed -e 's|-.*||')
%define krelease %(echo "%{kernel}" | sed -e 's|.*-||')

%define rname airo_mpi
%define rversion 20031220
%define rrelease 2

%define moduledir /kernel/drivers/net/wireless/airo_mpi
%define modules airo_mpi.o

Summary: Linux driver for the Cisco 350 miniPCI series.
Name: kernel-module-airo_mpi
Version: 1.6
Release: %{rrelease}.%{rversion}_%{kversion}_%{krelease}
License: GPL
Group: System Environment/Kernel
URL: http://bellet.info/~bellet/laptop/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://bellet.info/~bellet/laptop/airo_mpi-%{rversion}.tar.gz
BuildRoot: %{_tmppath}/root-%{name}-%{version}
Prefix: %{_prefix}

BuildRequires: kernel-source
Requires: /boot/vmlinuz-%{kversion}-%{krelease}

Obsoletes: %{rname}, kernel-%{rname}
Provides: %{rname}, kernel-%{rname}
Provides: kernel-modules

%description
Linux driver for the Cisco 350 miniPCI series.

These drivers are built for kernel %{kversion}-%{krelease}
and architecture %{_target_cpu}.
They might work with newer/older kernels.

%package -n kernel-smp-module-airo_mpi
Summary: Linux SMP driver for the Cisco 350 miniPCI series.
Group: System Environment/Kernel

Requires: /boot/vmlinuz-%{kversion}-%{krelease}smp

Obsoletes: %{rname}, kernel-%{rname}
Provides: %{rname}, kernel-%{rname}
Provides: kernel-modules

%description -n kernel-smp-module-airo_mpi
Linux SMP driver for the Cisco 350 miniPCI series.

These drivers are build for kernel %{kversion}-%{krelease}smp
and architecture %{_target_cpu}.
They might work with newer/older kernels.

%prep
%setup -n %{rname}-%{rversion}

### FIXME: Fix Makefile to override KERNEL_VERSION
%{__perl} -pi.orig -e 's|^#(KERNEL_VERSION)=.*$|$1 = %{kversion}-%{krelease}|' Makefile

%build
%{__rm} -rf %{buildroot}
echo -e "\nDriver version: %{rversion}\nKernel version: %{kversion}-%{krelease}\n"

### Prepare UP kernel.
cd %{_usrsrc}/linux-%{kversion}-%{krelease}
%{__make} -s distclean &>/dev/null
%{__cp} -f configs/kernel-%{kversion}-%{_target_cpu}.config .config
%{__make} -s symlinks oldconfig dep EXTRAVERSION="-%{krelease}" &>/dev/null
cd -

### Make UP module.
%{__make} %{?_smp_mflags} clean all \
	KERNEL_VERSION="%{kversion}-%{krelease}" \
	CC="${CC:-%{__cc}}"
%{__install} -d -m0755 %{buildroot}%{_libmoddir}/%{kversion}-%{krelease}%{moduledir}
%{__install} -m0644 %{modules} %{buildroot}%{_libmoddir}/%{kversion}-%{krelease}%{moduledir}

### Prepare SMP kernel.
cd %{_usrsrc}/linux-%{kversion}-%{krelease}
%{__make} -s distclean &>/dev/null
%{__cp} -f configs/kernel-%{kversion}-%{_target_cpu}-smp.config .config
%{__make} -s symlinks oldconfig dep EXTRAVERSION="-%{krelease}smp" &>/dev/null
cd -

### Make SMP module.
%{__make} %{?_smp_mflags} clean all \
	KERNEL_VERSION="%{kversion}-%{krelease}" \
	CC="${CC:-%{__cc}}"
%{__install} -d -m0755 %{buildroot}%{_libmoddir}/%{kversion}-%{krelease}smp%{moduledir}
%{__install} -m0644 %{modules} %{buildroot}%{_libmoddir}/%{kversion}-%{krelease}smp%{moduledir}

%install
### Install utilities

%post
/sbin/depmod -ae %{kversion}-%{krelease} || :

%postun
/sbin/depmod -ae %{kversion}-%{krelease} || :

%post -n kernel-smp-module-airo_mpi
/sbin/depmod -ae %{kversion}-%{krelease}smp || :

%postun -n kernel-smp-module-airo_mpi
/sbin/depmod -ae %{kversion}-%{krelease}smp || :

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc airo_mpi.HOWTO.txt
%{_libmoddir}/%{kversion}-%{krelease}%{moduledir}/

%files -n kernel-smp-module-airo_mpi
%defattr(-, root, root, 0755)
%doc airo_mpi.HOWTO.txt
%{_libmoddir}/%{kversion}-%{krelease}smp%{moduledir}/

%changelog
* Thu Mar 11 2004 Dag Wieers <dag@wieers.com> - 1.6-2.20031220
- Fixed the longstanding smp kernel bug. (Bert de Bruijn)

* Sun Dec 21 2003 Dag Wieers <dag@wieers.com> - 1.6-1.20031220
- Updated to release 20031220.

* Wed Dec 17 2003 Dag Wieers <dag@wieers.com> - 1.6-1.20031217
- Updated to release 20031217.

* Mon Dec 08 2003 Dag Wieers <dag@wieers.com> - 1.6-0.20031204
- Updated to release 20031204.

* Mon Dec 01 2003 Dag Wieers <dag@wieers.com> - 1.6-20031108
- Updated to release 20031108.

* Sun Oct 19 2003 Dag Wieers <dag@wieers.com> - 1.6-20031011
- Initial package. (using DAR)
