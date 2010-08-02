Source10: kmodtool
Source11: find-requires
Source12: find-requires.ksyms
%define   kmodtool bash %{SOURCE10}
%{!?centos_ver: %define centos_ver %(Z=`rpm -q --whatprovides /etc/redhat-release`;A=`rpm -q --qf '%{V}' $Z`; echo ${A:0:1})}

# if kversion isn't defined on rpm build line, build against current kernel
%if %{centos_ver} == 4
%{!?kversion: %define kversion 2.6.9-89.EL}
%endif
%if %{centos_ver} == 5
%{!?kversion: %define kversion 2.6.18-194.el5}
%endif

# hint: this can he overridden with "--define kversion foo" on the rpmbuild command line, e.g.
# --define "kversion 2.6.18-8.el5"

%define kmod_name drbd83
%define short_name drbd

%define kverrel %(%{kmodtool} verrel %{?kversion} 2>/dev/null)

%define upvar ""

%if %{centos_ver} == 4
%ifarch i686 x86_64 ia64
%define xenvar xenU
%define smpvar smp
%endif

%ifarch i686
%define paevar hugemem
%endif

%ifarch x86_64
%define largesmpvar largesmp
%endif

%ifarch ppc64 ppc64iseries
%define kdumpvar kdump
%endif

%ifarch sparc64 ppc
%define smpvar smp
%endif

%{!?kvariants: %define kvariants %{?upvar} %{?smpvar} %{?xenvar} %{?paevar} %{?kdumpvar} %{?largesmpvar}}
%endif

%if %{centos_ver} == 5
%ifarch i686 x86_64 ia64
%define xenvar xen
%endif

%ifarch i686
%define paevar PAE
%endif

%ifarch ppc64 ppc64iseries
%define kdumpvar kdump
%endif

%ifarch sparc64 ppc
%define smpvar smp
%endif

%{!?kvariants: %define kvariants %{?upvar} %{?smpvar} %{?xenvar} %{?paevar} %{?kdumpvar}}
%endif

Name: %{kmod_name}-kmod
Summary: Distributed Redundant Block Device driver for Linux
Version: 8.3.8
Release: 1%{?dist}
Source: %{short_name}-%{version}.tar.gz
License: GPL
ExclusiveOS: linux
Group: System Environment/Kernel
Provides: %{name}
URL: http://www.drbd.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-root
ExclusiveArch: i686 x86_64

# Override find_provides to use a script that provides "kernel(symbol) = hash".
# Pass path of the RPM temp dir containing kabideps to find-provides script.
%global _use_internal_dependency_generator 0
%define __find_requires %_sourcedir/find-requires %{name}

%description
Drbd is a distributed replicated block device. It mirrors a
block device over the network to another machine. Think of it
as networked raid 1. It is a building block for setting up
high availability (HA) clusters.

Authors:
--------
    Philipp Reisner <philipp.reisner@linbit.com>
    Lars Ellenberg  <lars.ellenberg@linbit.com>

# magic hidden here:
%{expand:%(%{kmodtool} rpmtemplate_kmp %{kmod_name} %{kverrel} %{kvariants} 2>/dev/null)}

%prep
%setup -n %{short_name}-%{version} -q -c -T -a 0
pushd %{short_name}-%{version}
%configure --without-utils --with-km --without-udev --without-xen \
           --without-pacemaker --without-heartbeat --without-rgmanager \
           --without-bashcompletion
popd

for kvariant in %{kvariants} ; do
    cp -a %{short_name}-%{version} _kmod_build_$kvariant
done
cd %{short_name}-%{version}

%build

[ -n $RPM_BUILD_ROOT -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}

for kvariant in %{kvariants}
do
    ksrc=%{_usrsrc}/kernels/%{kverrel}${kvariant:+-$kvariant}-%{_target_cpu}
    pushd _kmod_build_$kvariant
    make KDIR="${ksrc}" module
    popd
done

%install

for kvariant in %{kvariants}
do
    ksrc=%{_usrsrc}/kernels/%{kverrel}${kvariant:+-$kvariant}-%{_target_cpu}
    pushd _kmod_build_$kvariant/drbd
    make -C "${ksrc}" INSTALL_MOD_PATH=$RPM_BUILD_ROOT INSTALL_MOD_DIR=extra/%{kmod_name} modules_install M=$PWD
    popd
    find $RPM_BUILD_ROOT -type f -name \*.ko -exec strip --strip-debug \{\} \;
done

%clean
[ -n $RPM_BUILD_ROOT -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Jun 04 2010 Ralph Angenendt <ralph@centos.org> drbd83-8.3.8-1
- upgraded to upstream version 8.3.8
* Thu Mar 18 2010 Ralph Angenendt <ralph@centos.org>
- upgraded to upstream version 8.3.7
* Mon May  4 2009 Ralph Angenendt <ralph@centos.org>
- upgraded to upstream version 8.3.1 
- created drbd83 branch to allow people to stay at 8.0/8.2
- make spec file work with 4 and 5
- First release of 8.3.x for CentOS
 
* Thu Oct  2 2008 Johnny Hughes <johnny@centos.org>
- modified to work with CentOS-5 weak updates

* Mon Jun  2 2008 Johnny Hughes <johnny@centos.org>
- upgraded to upstream version 8.2.6

* Tue Feb 26 2008 Johnny Hughes <johnny@centos.org>
- upgraded to upstream version 8.2.5

* Thu Feb  7 2008 Johnny Hughes <johnny@centos.org>
- upgraded to version 8.2.4 and built drbd82

* Sun Oct 10 2007 Johnny Hughes <johnny@centos.org>
- upgraded to upstream version 8.0.6

* Thu Jul 26 2007 Johnny Hughes <johnny@centos.org>
- upgraded to upstream version 8.0.4

* Thu May 10 2007 04:30:00 +0600 Johnny Hughes <johnny@centos.org>
- modified to roll in kmod building, this is the package to build modules only. 

* Mon May 7 2007 17:10:14 +0200 Philipp Reisner <phil@linbit.com>
- drbd (8.0.3-1)
 * Fixed a race condition that could cause us to continue to traverse a bio
   after it was freed. (led to an OOPS)
 * Fixed a race condition that could cause us to use members of an ee, after
   it was freed. (led to various weirdness)
 * Language fixes for the man pages.
 * The drbdsetup commands (events, wait-connect,...) release the lock now.
 * Minor fixes and updates to the user land tools and to the peer outdater.

* Fri Apr 6 2007 21:32:39 +0200 Philipp Reisner <phil@linbit.com>
- drbd (8.0.2-1)
 * Removed a bug that could cause an OOPS in drbd_al_to_on_disk_bm()
 * Improved the robustness of the UUID based algorithm that decides
   about the resync direction.
 * Fixed the error handling in case a the open() of a backing
   blockdevice fails.
 * Fixed a race condition that could cause a "drbdadm disconnect" to hang.
 * More verbosity in we can not claim a backing block device.
 * More verbosity and paranoia in the bitmap area.
 * On some vendor kernels 8.0.1 did not load because of kzalloc. fixed.
 * Fault injection can now not only be turned on or off, but can be 
   enabled on a per device basis.
 * Fixed the scripts and files needed to build drbd into a kernel.

* Mon Mar 3 2007 10:10:26 +0200 Philipp Reisner <phil@linbit.com>
- drbd (8.0.1-1)
 * Fixed some race conditions that could trigger an OOPS when the loca disk
   failes and DRBD detaches itself from the failing disk.
 * Added a missing call to drbd_try_outdate_peer().
 * LVM's LVs expose ambiguous queue settings. When a RAID-0 (md) PV is
   used the present a segment size of 64k but at the same time allow only
   8 sectors. Fixed DRBD to deal with that fact corretly.
 * New option "always-asbp" to also use the after-after-split-brain-policy
   handlers, even it is not possible to determine from the UUIDs that
   the data of the two nodes was related in the past.
 * More verbosity in case a bio_add_page() fails.
 * Replaced kmalloc()/memset() with kzmalloc(), and a wrapper for older kernls
 * A fast version of drbd_al_to_on_disk_bm(). This is necessary for short
   (even sub-second) switchover times while having large "al-extents" settings.
 * Fixed drbdadm's array overflows (of on stack objects)
 * drbdsetup can now dump its usage in a XML format
 * New init script for gentoo
 * Fixed Typos in the usage of /proc/sysrq-trigger in the example config.

* Wed Jan 24 2007 16:10:09 +0200 Philipp Reisner <phil@linbit.com>
- drbd (8.0.0-1)
 * No effecitve changes to rc2.

* Wed Jan 17 2007 17:30:23 +0200 Philipp Reisner <phil@linbit.com>
- drbd (8.0rc2-1)
 * Added the well known automagiacally adjust drbd_config.h to
   make drbd compile on every by vendor's backports defaced 
   kernel. ( Linux-2.6.x only of course )
 * Fixed races with starting and finishing resync processes 
   while heavy application IO is going on.
 * Ported DRBD to the new crypto API (and added a emulation of the
   now API on top of the old one for older 2.6.x kernels)
 * Code to perform better on ethernet networks with jumbo
   frames.
 * Bugfixes to our request code (race conditions).
 * Every error code that is returned by drbdsetup has a 
   textual description by now.

* Fri Dec 22 2006 15:19:10 +0200 Philipp Reisner <phil@linbit.com>
- drbd (8.0rc1-1)
 * The drbd-peer-outdater got updated to work in multi node heartbeat
   clusters. (But we still not suceeded to get this into Heartbeat's
   repository accepted.)
 * Fixed resync decission after a crash in a pri-pri cluster.
 * Implemented the ping-timeout option for "sub-second" failover clusters.
 * Implemented all the "violently" options in the reconnect handling.
 * Updated man pages of drbd.conf and drbdsetup.
 * Removed the "self-claiming" on secondary nodes.
 * Fixed an uncountable number of bugs.

* Fri Nov  3 2006 15:20:54 +0200 Philipp Reisner <phil@linbit.com>
- drbd (8.0pre6-1)
 * All panic() calls where removed from DRBD.
 * IO errors while accessing the backing storage device are now handled
   correct.
 * Conflict detection for two primaries is in place and tested.
 * More tracing stuff
 * Lots of bugs found and fixed

* Sun Oct 31 2006 22:03:54 +0200 Philipp Reisner <phil@linbit.com>
- drbd (8.0pre5-1)
 * The request code was completely rewritten.
 * The write conflict detection code for primary-primary is currently
   broken, but will be fixed soon.
 * drbdsetup is no longer based on IOCTL but works now via
   netlink/connector.
 * drbd_panic() is on its way out.
 * A runtime configurable tracing framework got added.
 * A lot of effort was put into finding and fixing bugs.

* Mon Jul 31 2006 12:04:41 +0200 Philipp Reisner <phil@linbit.com>
- drbd (8.0pre4-1)
 * Added the "drbd-peer-outdater" heartbeat plugin.
 * New ("cluster wide") state changes. (Cluster wide serialisation of
   major state changes, like becomming primary, invalidateing a disk etc...)
 * Write requests are now sent by the worker instead out of the process's
   context that calls make_request().
 * The worker thread no longer gets restarted upon loss of connection.
 * A testsuite developed by students of 'FH Hagenberg' was added.

* Tue Apr 20 2006 13:46:18 +0200 Philipp Reisner <phil@linbit.com>
- drbd (8.0pre3-1)
 * Now it works on device mapper (LVM) as well as on "real" block devices.
 * Finally (after years) a sane "drbdadm adjust" imprementation, which is
   really really robust.
 * Fixes for 64bit kernel / 32 bit userland environments
 * Fixes in the sys-v init script
 * Renamed "--do-what-I-say" to "--overwrite-data-of-peer". Hopefully
   people now understand what this option does.

* Tue Apr  6 2006 17:53:56 +0200 Philipp Reisner <phil@linbit.com>
- drbd (8.0-pre2-1)
 * removed the "on-disconnect" and "split-brain-fix" config options and
   added the "fencing" config option instead.
 * Updated all manpages to cover drbd-8.0
 * /proc/drbd shows the whole drbd_state_t, as well the logging of state
   changes shows every field of drbd_state_t now.
 * Deactivated most of the TCQ code for now, since it changed again
   in the mainline kernel.
 * Minor other fixes.

* Tue Mar 14 2006 11:37:56 +0200 Philipp Reisner <phil@linbit.com>
- drbd (8.0_pre1-1)
 * Removed support for Linux-2.4.x
 * Cleanup of the wire protocol.
 * Added optional peer authentication with a shared secret.
 * Consolidated state changes into a central function.
 * Improved, tunable after-split-brain recovery strategies.
 * Always verify all IDs used in the protocol that are used as pointers.
 * Introduced the "outdate" disk state, and commands for managing it.
 * Introduced the "drbdmeta" command, and require the user to create
   meta-data explicitly.
 * Support for primary/primary (for OCFS2, GFS...)
 * Replaced the sync-groups with the sync-after mechanism.
 * The "common" section in the configuration file.
 * Replaced the generation counters (GCs) with data-generation-UUIDs
 * Improved performance by using Linux-2.6's BIOs with up to 32k per
   IO request. Before we transferred only up to 4k per IO request.
 * A Warning if the disk sizes are more than 10% different.
 * A connection teardown packet to differentiate between a crash
   of the peer and a peer that is shut down gracefully.
 * External imposable SyncPause states, to serialize DRBD's resynchronisation
   with the resynchronisation of backing storage's RAID configurations.
 * Backing storage can be hot added to disk less nodes.
 * Prepared for advanced integration to Heartbeat-2.0
 * Changed internal APIs so that missed writes of the meta-data super
   block are reported as they happen.
 * The http://usage.drbd.org sub project.
 * Rewrote the scanner/parser of drbd.conf. 10 times smaller/faster and
   easier to maintain.
 * Asynchronous meta-data IO [ Code drop from the DRBD+ branch ]