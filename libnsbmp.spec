#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	Decoding library for BMP and ICO file formats
Summary(pl.UTF-8):	Biblioteka dekodująca pliki w formatach BMP oraz ICO
Name:		libnsbmp
Version:	0.1.5
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	4a6f89a85a4cecfdfedd9c1ddd05c2db
URL:		http://www.netsurf-browser.org/projects/libnsbmp/
BuildRequires:	netsurf-buildsystem >= 1.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libnsbmp is a decoding library for BMP and ICO image file formats,
written in C. It was developed as part of the NetSurf project and is
available for use by other software under the MIT licence.

%description -l pl.UTF-8
Libnsbmp to napisana w C biblioteka dekodująca pliki obrazów w
formatach BMP oraz ICO. Powstała jako część projektu NetSurf i jest
dostępna do wykorzystania przez inne programy na licencji MIT.

%package devel
Summary:	libnsbmp library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libnsbmp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the include files and other resources you can
use to incorporate libnsbmp into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libnsbmp w swoich
programach.

%package static
Summary:	libnsbmp static library
Summary(pl.UTF-8):	Statyczna biblioteka libnsbmp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libnsbmp library.

%description static -l pl.UTF-8
Statyczna biblioteka libnsbmp.

%prep
%setup -q

%build
export AR="%{__ar}"
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared

%if %{with static_libs}
%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static
%endif

%install
rm -rf $RPM_BUILD_ROOT

export AR="%{__ar}"
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_libdir}/libnsbmp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnsbmp.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnsbmp.so
%{_includedir}/libnsbmp.h
%{_pkgconfigdir}/libnsbmp.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnsbmp.a
%endif
