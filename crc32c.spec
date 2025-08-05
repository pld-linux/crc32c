#
# Conditional build:
%bcond_without	tests	# unit testing
#
Summary:	CRC32C library
Summary(pl.UTF-8):	Biblioteka cyklicznego kodu nadmiarowego CRC32C
Name:		crc32c
Version:	1.1.2
Release:	2
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/google/crc32c/tags
Source0:	https://github.com/google/crc32c/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	cc0338e6a60c38cab04a70a2c36cd9f2
Patch0:		%{name}-system-libs.patch
URL:		https://github.com/google/crc32c
BuildRequires:	cmake >= 3.1
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	sed >= 4.0
%if %{with tests}
# with cmake support
BuildRequires:	glog-devel >= 0.6
BuildRequires:	google-benchmark-devel
BuildRequires:	gtest-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project (originating in Google LevelDB key-value store) collects
a few CRC32C implementations under an umbrella that dispatches to a
suitable implementation based on the host computer's hardware
capabilities.

CRC32C is specified as the CRC that uses the iSCSI polynomial in RFC
3720. The polynomial was introduced by G. Castagnoli, S. Braeuer and
M. Herrmann. CRC32C is used in software such as Btrfs, ext4, Ceph and
leveldb.

%description -l pl.UTF-8
Ten projekt (wywodzący się z bazy klucz-wartość Google LevelDB) zbiera
kilka implementacji CRC32C w obudowaniu, które wybiera implementację
pasującą do możliwości sprzętowych komputera.

Algorytm CRC32C to cykliczny kod nadmiarowy, wykorzystujący wielomian
iSCSI określony w RFC 3720. Wielomian został wprowadzony przez G.
Castagnoliego, S. Braeuera i M. Herrmanna. Algorytm jest
wykorzystywany w takim oprogramowaniu, jak btrfs, ext4, ceph czy
leveldb.

%package devel
Summary:	Header files for crc32c library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki crc32c
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for crc32c library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki crc32c.

%prep
%setup -q
%patch -P0 -p1

# crc32c_sse42_unittest is missing runtime detection of CPU capabilities
if ! grep -q '^flags .* sse4_2' /proc/cpuinfo ; then
	%{__sed} -i -e 's/if HAVE_SSE42 /if 0 /' src/crc32c_sse42_unittest.cc
fi

%build
install -d build
cd build
%cmake .. \
	%{!?with_tests:-DCRC32C_BUILD_BENCHMARKS=OFF -DCRC32C_BUILD_TESTS=OFF -DCRC32C_USE_GLOG=OFF}

%{__make}

%if %{with tests}
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.md
%attr(755,root,root) %{_libdir}/libcrc32c.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcrc32c.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcrc32c.so
%{_includedir}/crc32c
%{_libdir}/cmake/Crc32c
