#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
%define		_rc	rc5
Summary:	Library for 1394 Digital Camera Specification
Summary(pl.UTF-8):	Biblioteka dla specyfikacji Kamera Cyfrowa 1394
Name:		libdc1394
Version:	2.0.0
Release:	0.%{_rc}.1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://dl.sourceforge.net/libdc1394/%{name}-%{version}-%{_rc}.tar.gz
# Source0-md5:	dff62b3b0b0187e0253479c901a5fec3
URL:		http://sourceforge.net/projects/libdc1394/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	libraw1394-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXv-devel
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
specyfikacją Kamera Cyfrowa 1394 (dostępną pod
http://www.1394ta.org/).

%package devel
Summary:	libdc1394 header files
Summary(pl.UTF-8):	Pliki nagłówkowe libdc1394
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libraw1394-devel

%description devel
libdc1394 header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe libdc1394.

%package static
Summary:	Static libdc1394 library
Summary(pl.UTF-8):	Statyczna biblioteka libdc1394
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libdc1394 library.

%description static -l pl.UTF-8
Statyczna biblioteka libdc1394.

%prep
%setup -q -n %{name}-%{version}-%{_rc}

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

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/dc1394_reset_bus
%attr(755,root,root) %{_bindir}/dc1394_vloopback
%attr(755,root,root) %{_libdir}/libdc1394.so.20.0.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdc1394.so
%{_libdir}/libdc1394.la
%{_includedir}/dc1394
%{_pkgconfigdir}/libdc1394.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdc1394.a
%endif
