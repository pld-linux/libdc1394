Summary:	Library for 1394 Digital Camera Specification
Summary(pl):	Biblioteka dla specyfikacji Kamera Cyfrowa 1394
Name:		libdc1394
Version:	1.0.0
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/libdc1394/%{name}-%{version}.tar.gz
# Source0-md5:	e87fba1834e3e99ec3b96738080eb835
Patch0:		%{name}-link.patch
URL:		http://sourceforge.net/projects/libdc1394/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libraw1394-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libdc1394 is a library that is intended to provide a high level
programming interface for application developers who wish to control
IEEE 1394 based cameras that conform to the 1394-based Digital Camera
Specification (found at http://www.1394ta.org/).

%description -l pl
libdc1394 jest bibliotek±, której za³o¿eniem jest dostarczenie
interfejsu wysokiego poziomu dla twórców oprogramowania pragn±cych
sterowaæ kamerami skonstruowanymi w oparciu o IEEE 1394 zgodnie ze
specyfikacj± Kamera Cyfrowa 1394 (dostêpn± pod
http://www.1394ta.org/).

%package devel
Summary:	libdc1394 header files
Summary(pl):	Pliki nag³ówkowe libdc1394
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libraw1394-devel

%description devel
libdc1394 header files.

%description devel -l pl
Pliki nag³ówkowe libdc1394.

%package static
Summary:	Static libdc1394 library
Summary(pl):	Statyczna biblioteka libdc1394
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libdc1394 library.

%description static -l pl
Statyczna biblioteka libdc1394.

%prep
%setup -q
%patch0 -p1

%{__perl} -pi -e 's@-L/usr/X11R6/lib@-L/usr/X11R6/%{_lib}@' examples/Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
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
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libdc1394_control.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdc1394_control.so
%{_libdir}/lib*.la
%{_includedir}/libdc1394

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
