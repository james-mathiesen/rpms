# $Id$
# Authority: dag

%{?fc1:%define _without_kde32 1}
%{?el3:%define _without_kde32 1}
%{?rh9:%define _without_kde32 1}
%{?rh7:%define _without_kde32 1}
%{?el2:%define _without_kde32 1}

%{!?k3b_version:%define k3b_version %(rpm -q k3b --qf '%{RPMTAG_VERSION}' | tail -1)}

Summary: MP3 decoder plugin for k3b CD/DVD burner
Name: k3b-mp3
Version: %{k3b_version}
Release: 1
License: GPL
Group: Applications/Multimedia
URL: http://www.k3b.org/

Source: http://dl.sf.net/k3b/k3b-%{version}.tar.bz2
# Patch touches globals, better include this.
Patch0: k3b-0.12.2-statfs.patch
Patch1: k3b-0.11.24-no-bad-gcc.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: k3b
# Some of these are only to make the configure script happy.
BuildRequires: XFree86-devel, kdelibs-devel >= 6:3.1, libart_lgpl-devel, arts-devel
BuildRequires: zlib-devel, libpng-devel, libjpeg-devel
BuildRequires: gettext, taglib-devel libmad-devel lame-devel
%{!?_without_kd32:BuildRequires: libmng-devel fam-devel glib2-devel alsa-lib-devel esound-devel}

Requires: k3b = %{version}

%description
MP3 decoder plugin for k3b, a feature-rich and easy to handle CD/DVD
burning application.

%prep
%setup -n k3b-%{version}
#patch0 -p1 -b .statfs
#patch1 -p1 -b .no-bad-gcc

%build
source /etc/profile.d/qt.sh
%configure \
	--disable-rpath \
	--with-external-libsamplerate="no" \
	--without-oggvorbis \
	--without-flac \
	--with-qt-libraries="$QTDIR/lib"

%{__ln_s} -f %{_libdir}/libk3b.la libk3b/libk3b.la

%{__make} -C plugins/decoder/mp3 %{?_smp_mflags}
%{__make} -C plugins/encoder/lame %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} -C plugins/decoder/mp3 install DESTDIR="%{buildroot}"
%{__make} -C plugins/encoder/lame install DESTDIR="%{buildroot}"

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%dir %{_libdir}/kde3/
%{_libdir}/kde3/libk3bmaddecoder.*
%{_libdir}/kde3/libk3blameencoder.*
%dir %{_datadir}/apps/
%dir %{_datadir}/apps/k3b/
%dir %{_datadir}/apps/k3b/plugins/
%{_datadir}/apps/k3b/plugins/k3bmaddecoder.plugin
%{_datadir}/apps/k3b/plugins/k3blameencoder.plugin

%changelog
* Sun Mar 05 2006 Dag Wieers <dag@wieers.com> - 0.12.10-1
- Imported based on Livna SPEC file.
- Initial package. (using DAR)
