#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	LibreDWG - free implementation of the DWG file format
Summary(pl.UTF-8):	LibreDWG - wolnodostępna implementacja formatu plików DWG
Name:		libredwg
Version:	0.14
Release:	1
License:	GPL v3+
Group:		Libraries
Source0:	https://ftp.gnu.org/gnu/libredwg/%{name}-%{version}.tar.xz
# Source0-md5:	5dbca7fbb46ce3383c78fccebc8a734b
Patch0:		%{name}-info.patch
Patch1:		%{name}-python.patch
URL:		http://www.gnu.org/software/libredwg/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.14
BuildRequires:	bash
BuildRequires:	doxygen
BuildRequires:	help2man
BuildRequires:	libtool >= 2:2
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pcre2-8-devel
BuildRequires:	pcre2-16-devel
BuildRequires:	perl-devel
BuildRequires:	pkgconfig
BuildRequires:	pslib-devel
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
BuildRequires:	swig-python >= 2
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibreDWG is a free C library to read DWG files. DWG is a file format
created in the 70's for the emerging CAD applications. Currently it
is the native file format of AutoCAD, a proprietary CAD program
developed by AutoDesk.

%description -l pl.UTF-8
LibreDWG to wolnodostępna biblioteka C do odczytu plików DWG. DWG to
format plików powstały w latach 70. dla powstających aplikacji CAD.
Obecnie jest to natywny format AutoCAD-a - własnościowego programu
CAD rozwijanego przez firmę AutoDesk.

%package devel
Summary:	Header files for LibreDWG library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LibreDWG
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
# dwg.h file
Conflicts:	libdwg-devel

%description devel
Header files for LibreDWG library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LibreDWG.

%package static
Summary:	Static LibreDWG library
Summary(pl.UTF-8):	Statyczna biblioteka LibreDWG
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static LibreDWG library.

%description static -l pl.UTF-8
Statyczna biblioteka LibreDWG.

%package -n perl-libredwg
Summary:	Perl interface for LibreDWG library
Summary(pl.UTF-8):	Interfejs Perla do biblioteki LibreDWG
Group:		Development/Languages/Perl
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n perl-libredwg
Perl interface for LibreDWG library.

%description -n perl-libredwg -l pl.UTF-8
Interfejs Perla do biblioteki LibreDWG.

%package -n python3-libredwg
Summary:	Python interface for LibreDWG library
Summary(pl.UTF-8):	Interfejs Pythona do biblioteki LibreDWG
Group:		Development/Languages/Perl
Requires:	%{name}%{?_isa} = %{version}-%{release}
Obsoletes:	python-libredwg < 0.14

%description -n python3-libredwg
Python interface for LibreDWG library.

%description -n python3-libredwg -l pl.UTF-8
Interfejs Pythona do biblioteki LibreDWG.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%{__sed} -i -e '1s,/usr/bin/env perl,%{__perl},' src/gen-dynapi.pl

# no git-version-gen in release tarball
%{__sed} -i -e 's/m4_esyscmd(.*git-version-gen.*)/%{version},/' configure.ac

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	PYTHON="%{__python3}" \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-perl-install=vendor

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libredwg.la

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/_LibreDWG.la

# just example, nothing really useful
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-libredwg-%{version}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/libredwg/load_dwg.py $RPM_BUILD_ROOT%{_examplesdir}/python-libredwg-%{version}
# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_datadir}/libredwg/dwgadd.example*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO examples/dwgadd.example*
%attr(755,root,root) %{_bindir}/dwg2SVG
%attr(755,root,root) %{_bindir}/dwg2dxf
%attr(755,root,root) %{_bindir}/dwg2ps
%attr(755,root,root) %{_bindir}/dwgadd
%attr(755,root,root) %{_bindir}/dwgbmp
%attr(755,root,root) %{_bindir}/dwgfilter
%attr(755,root,root) %{_bindir}/dwggrep
%attr(755,root,root) %{_bindir}/dwglayers
%attr(755,root,root) %{_bindir}/dwgread
%attr(755,root,root) %{_bindir}/dwgrewrite
%attr(755,root,root) %{_bindir}/dwgwrite
%attr(755,root,root) %{_bindir}/dxf2dwg
%attr(755,root,root) %{_bindir}/dxfwrite
%{_libdir}/libredwg.so.*.*.*
%ghost %{_libdir}/libredwg.so.0
%{_mandir}/man1/dwg2SVG.1*
%{_mandir}/man1/dwg2dxf.1*
%{_mandir}/man1/dwg2ps.1*
%{_mandir}/man1/dwgadd.1*
%{_mandir}/man1/dwgbmp.1*
%{_mandir}/man1/dwgfilter.1*
%{_mandir}/man1/dwggrep.1*
%{_mandir}/man1/dwglayers.1*
%{_mandir}/man1/dwgread.1*
%{_mandir}/man1/dwgrewrite.1*
%{_mandir}/man1/dwgwrite.1*
%{_mandir}/man1/dxf2dwg.1*
%{_mandir}/man1/dxfwrite.1*
%{_mandir}/man5/dwgadd.5*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libredwg.so
%{_includedir}/dwg.h
%{_includedir}/dwg_api.h
%{_pkgconfigdir}/libredwg.pc
%{_infodir}/LibreDWG.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/libredwg.a

%files -n perl-libredwg
%defattr(644,root,root,755)
%{perl_vendorarch}/LibreDWG.pm
%dir %{perl_vendorarch}/auto
%dir %{perl_vendorarch}/auto/LibreDWG
%{perl_vendorarch}/auto/LibreDWG/LibreDWG.so

%files -n python3-libredwg
%defattr(644,root,root,755)
%{py3_sitedir}/_LibreDWG.so
%{py3_sitescriptdir}/LibreDWG.py
%{py3_sitescriptdir}/__pycache__/LibreDWG.cpython-*.pyc
%{_examplesdir}/python-libredwg-%{version}
