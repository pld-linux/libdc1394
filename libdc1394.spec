#
# Conditional build:
%bcond_without	static_libs	# don't build static library
%bcond_with	v4l1		# build with Video4Linux 1.x API (dropped in linux kernel 2.6.38)

Summary:	Library for 1394 Digital Camera Specification
Summary(pl.UTF-8):	Biblioteka dla specyfikacji kamery cyfrowej 1394 (1394 Digital Camera)
Name:		libdc1394
Version:	2.2.5
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/libdc1394/%{name}-%{version}.tar.gz
# Source0-md5:	01acfcde2cc85863b0acb90dcffa1659
Patch0:		%{name}-link.patch
Patch1:		%{name}-ac.patch
# libdc1394-2.1.2 vs libdc1394_avt-2.1.2 diff (http://www.alliedvisiontec.com/fileadmin/content/PDF/Software/AVT_software/zip_files/AVTFire4Linux3v0.src.tar/libdc1394_avt-2.1.2.tar.gz)
Patch2:		%{name}-avt.patch
URL:		http://damien.douxchamps.net/ieee1394/libdc1394/
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel >= 1.2.4
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.9.6
BuildRequires:	libraw1394-devel >= 1.2.0
BuildRequires:	libtool
BuildRequires:	libusb-devel >= 1.0
%{?with_v4l1:BuildRequires:	linux-libc-headers < 7:2.6.38}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.583
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXv-devel
Requires:	SDL >= 1.2.4
Requires:	libraw1394 >= 1.2.0
Requires:	libusb >= 1.0
Provides:	libdc1394(avt) = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libdc1394 is a library that is intended to provide a high level
programming interface for application developers who wish to control
IEEE 1394 based cameras that conform to the 1394-based Digital Camera
Specification (found at http://www.1394ta.org/).

%description -l pl.UTF-8
libdc1394 jest biblioteką, której założeniem jest dostarczenie
interfejsu wysokiego poziomu dla twórców oprogramowania pragnących
sterować kamerami skonstruowanymi w oparciu o IEEE 1394 zgodnie ze
specyfikacją kamery cyfrowej 1394 (1394 Digital Camera, dostępną pod
http://www.1394ta.org/).

%package devel
Summary:	libdc1394 header files
Summary(pl.UTF-8):	Pliki nagłówkowe libdc1394
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libraw1394-devel >= 1.2.0
Requires:	libusb-devel >= 1.0
Provides:	libdc1394-devel(avt) = %{version}-%{release}

%description devel
libdc1394 header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe libdc1394.

%package static
Summary:	Static libdc1394 library
Summary(pl.UTF-8):	Statyczna biblioteka libdc1394
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	libdc1394-static(avt) = %{version}-%{release}

%description static
Static libdc1394 library.

%description static -l pl.UTF-8
Statyczna biblioteka libdc1394.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# man pages for noinst examples
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/{dc1394_multiview,grab_{color,gray,partial}_image}.1
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/avt_singleview.1

%if %{without v4l1}
# dc1394_vloopback not built if !HAVE_VIDEODEV, remove man page as well
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/dc1394_vloopback.1
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/dc1394_reset_bus
%attr(755,root,root) %{_libdir}/libdc1394.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdc1394.so.22
%{_mandir}/man1/dc1394_reset_bus.1*
%if %{with v4l1}
%attr(755,root,root) %{_bindir}/dc1394_vloopback
%{_mandir}/man1/dc1394_vloopback.1*
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdc1394.so
%{_libdir}/libdc1394.la
%{_includedir}/dc1394
%{_pkgconfigdir}/libdc1394-2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdc1394.a
%endif
