# based on PLD Linux spec git://git.pld-linux.org/packages/libgd.git
Summary:	Dynamic image creation library
Name:		gd
Version:	2.1.1
Release:	1
License:	BSD-like
Group:		Libraries
Source0:	https://bitbucket.org/libgd/gd-libgd/downloads/libgd-%{version}.tar.xz
# Source0-md5:	9076f3abd1f9815d106da36467ea15bc
URL:		http://www.libgd.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
BuildRequires:	gettext-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	libvpx-devel
BuildRequires:	xorg-libXpm-devel
BuildRequires:	zlib-devel
Provides:	gd(gif) = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gd is the image manipulating library. It was created to allow graphs,
charts and the like to be generated on the fly for use on the World
wide Web, but is useful for any application in which custom images are
useful. It is not a paint program; it is a library. gd library creates
PNG, JPEG, GIF and WBMP images. PNG is a more compact format, and full
compression is available. JPEG works well with photographic images,
and is still more compatible with the major Web browsers than even PNG
is. WBMP is intended for wireless devices (not regular web browsers).

%package devel
Summary:	Development part of the GD library
Group:		Development/Libraries
Provides:	gd-devel(gif) = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig(fontconfig)
Requires:	pkgconfig(freetype2)
Requires:	pkgconfig(libpng)
Requires:	pkgconfig(xpm)


%description devel
This package contains the files needed for development of programs
linked against GD.

%package progs
Summary:	Utility programs that use libgd
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description progs
These are utility programs supplied with gd, the image manipulation
library. The libgd-progs package contains a group of scripts for
manipulating the graphics files in formats which are supported by the
libgd library.

%prep
%setup -qn libgd-%{version}

# hack to avoid inclusion of -s in --ldflags
%{__sed} -i 's,\@LDFLAGS\@,,g' config/gdlib-config.in

# don't fail on AM warnings
%{__sed} -i 's,-Werror,,' configure.ac

%build
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoheader}
%{__autoconf}
%configure \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING NEWS
%attr(755,root,root) %ghost %{_libdir}/libgd.so.?
%attr(755,root,root) %{_libdir}/libgd.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gdlib-config
%attr(755,root,root) %{_libdir}/libgd.so
%{_includedir}/*.h
%{_pkgconfigdir}/gdlib.pc

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%exclude %{_bindir}/gdlib-config

