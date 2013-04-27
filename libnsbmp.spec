#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	Decoding library for BMP and ICO file formats
Name:		libnsbmp
Version:	0.1.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	5b33ff44dfb48e628bcadbe7e51edf90
Patch0:		lib.patch
URL:		http://www.netsurf-browser.org/projects/libnsbmp/
BuildRequires:	netsurf-buildsystem
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libnsbmp is a decoding library for BMP and ICO image file formats,
written in C. It was developed as part of the NetSurf project and is
available for use by other software under the MIT licence.

%package devel
Summary:	libnsbmp library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libnsbmp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the libraries, include files and other resources you can use
to incorporate libnsbmp into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libnsbmp w swoich
programach.

%package static
Summary:	libnsbmp static libraries
Summary(pl.UTF-8):	Statyczne biblioteki libnsbmp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libnsbmp libraries.

%description static -l pl.UTF-8
Statyczna biblioteka libnsbmp.

%prep
%setup -q
%patch0 -p1

%build
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} Q= \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared

%if %{with static_libs}
%{__make} Q= \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install Q= \
	lib=%{_lib} \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} install Q= \
	lib=%{_lib} \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnsbmp.so.*.*.*
%ghost %{_libdir}/libnsbmp.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libnsbmp.so
%{_includedir}/libnsbmp.h
%{_pkgconfigdir}/libnsbmp.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnsbmp.a
%endif
