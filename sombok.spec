#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Unicode Text Segmentation library
Summary(ja.UTF-8):	ユニコード テキスト分節パッケージ
Summary(pl.UTF-8):	Biblioteka do przenoszenia tekstu
Name:		sombok
Version:	2.4.0
Release:	1
License:	GPL v1+ or Artistic
Group:		Libraries
#Source0Download: https://github.com/hatukanezumi/sombok/releases
Source0:	https://github.com/hatukanezumi/sombok/archive/%{name}-%{version}.tar.gz
# Source0-md5:	761921401ff323ce37d76e217062d2e8
URL:		https://github.com/hatukanezumi/sombok
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	libthai-devel >= 0.1.9
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires:	libthai >= 0.1.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sombok library package performs Line Breaking Algorithm described in 
Unicode Standard Annex #14 (UAX #14). East_Asian_Width informative 
properties defined by Annex #11 (UAX #11) may be concerned to
determine breaking positions. This package also implements "default"
Grapheme Cluster segmentation described in Annex #29 (UAX #29).

%description -l pl.UTF-8
Biblioteka sombok wykonuje algorytm łamania linii opisany w dokumencie
Unicode Standard Annex #14 (UAX #14). Przy określaniu miejsc łamania
brana jest pod uwagę własność informacyjna East_Asian_Width
zdefiniowana w dokumencie Annex #11 (UAX #11). Pakiet obsługuje także
"domyślne" dzielenie Grapheme Cluster opisane w dokumencie Annex #29
(UAX #29).

%package devel
Summary:	Header files for sombok library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki sombok
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for sombok library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki sombok.

%package static
Summary:	Static sombok library
Summary(pl.UTF-8):	Statyczna biblioteka sombok
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static sombok library.

%description static -l pl.UTF-8
Statyczna biblioteka sombok.

%package apidocs
Summary:	API documentation for sombok library
Summary(pl.UTF-8):	Dokumentacja API biblioteki sombok
Group:		Documentation

%description apidocs
API documentation for sombok library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki sombok.

%prep
%setup -q -n sombok-sombok-%{version}

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

# workaround for am install
%{__mv} doc/html/search doc/html-search

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# undo for %doc
%{__mv} doc/html-search doc/html/search
# packaged as %doc in -apidocs
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/sombok

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsombok.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog* NEWS README TODO
%lang(ja) %doc README.ja_JP
%attr(755,root,root) %{_libdir}/libsombok.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsombok.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsombok.so
%{_includedir}/sombok.h
%{_includedir}/sombok_constants.h
%{_pkgconfigdir}/sombok.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsombok.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
