
# Fedora package review: http://bugzilla.redhat.com/451643

# do unit tests
#define _with_check 1

Summary: Library for accessing MusicBrainz servers
Name: libmusicbrainz3
Version: 3.0.2
Release: 7%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
URL: http://www.musicbrainz.org/
Source0: ftp://ftp.musicbrainz.org/pub/musicbrainz/libmusicbrainz-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source10: doxygen-footer.html

# upstreamed: http://lists.musicbrainz.org/pipermail/musicbrainz-devel/2008-September/002575.html
# updated to comment out even Requires.private for now, to avoid needless deps
# (re)introduced by recent fedora pkgconfig behavior change 
Patch2: libmusicbrainz-3.0.1-private.patch
Patch3: libmusicbrainz-3.0.2-gcc44.patch

BuildRequires: cmake
%if 0%{?_check_check}
BuildRequires: cppunit-devel
%endif
BuildRequires: doxygen
BuildRequires: libdiscid-devel
BuildRequires: pkgconfig
BuildRequires: neon-devel

%description
The MusicBrainz client library allows applications to make metadata
lookup to a MusicBrainz server, generate signatures from WAV data and
create CD Index Disk ids from audio CD roms.

%package devel
Summary: Headers for developing programs that will use %{name} 
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
# patch2 removes the need for these
#Requires: libdiscid-devel neon-devel
%description devel
This package contains the headers that programmers will need to develop
applications which will use %{name}. 


%prep
%setup -q -n libmusicbrainz-%{version}

%patch2 -p1 -b .private
%patch3 -p1 -b .gcc44

# until doxygen is fixed, something like
# http://bugzilla.gnome.org/show_bug.cgi?id=579303 , hack out
# mulitilib-conflicting doxygen footers
install -p %{SOURCE10} doxygen-footer.html
echo "HTML_FOOTER         = doxygen-footer.html" >> Doxygen

%build
%{cmake} .

make %{?_smp_mflags} all docs


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot}

rm -f docs/installdox


%check
%if 0%{?_with_check}
make check
%endif


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS.txt COPYING.txt NEWS.txt README.txt
%{_libdir}/libmusicbrainz3.so.6*

%files devel
%defattr(-,root,root,-)
%doc docs/*
%{_includedir}/musicbrainz3/
%{_libdir}/libmusicbrainz3.so
%{_libdir}/pkgconfig/libmusicbrainz3.pc


%changelog
* Wed May 26 2010 Bastien Nocera <bnocera@redhat.com> 3.0.2-7
- Remove script from documentation
Related: rhbz#595773

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 3.0.2-6.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 3.0.2-5
- fix doxygen-induced multilib conflicts (#480378)
- add %%check section (disabled by default, pending cppunit detection issues)

* Wed Feb 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 3.0.2-4
- work harder to omit extraneous pkgconfig deps
- gcc44 patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.2-2
- rebuild for pkgconfig deps

* Tue Sep 16 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.2-1
- libmusicbrainz3-3.0.2

* Fri Sep 05 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.1-4
- Build docs (#461238)
- -devel: drop extraneous Requires

* Fri Jul 25 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.1-3
- fix recursive linking against libdiscid neon

* Thu Jul 24 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.1-2
- BR: libdiscid-devel
- -devel: Requires: libdiscid-devel neon-devel

* Mon Jun 16 2008 Rex Dieter <rdieter@fedoraproject.org> 3.0.1-1
- libmusicbrainz3-3.0.1

* Sun Jun 15 2008 Rex Dieter <rdieter@fedoraproject.org> 2.1.5-7
- Provides: libmusicbrainz2(-devel), prepare for libmusicbrainz3

* Fri Feb 22 2008 Rex Dieter <rdieter@fedoraproject.org> 2.1.5-6
- gcc43 patch (#434127)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.1.5-5
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.1.5-4
- specfile cosmetics

* Thu Nov 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 2.1.5-3
- use versioned Obsoletes
- drop (Build)Requires: libstdc++-devel
- License: LGPLv2+

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> - 2.1.5-2
- Rebuild for PPC toolchain bug

* Thu Jun 21 2007 - Bastien Nocera <bnocera@redhat.com> - 2.1.5-1
- Update to 2.1.5

* Mon Oct 23 2006 Matthias Clasen <mclasen@redhat.com> - 2.1.4-1
- Update to 2.1.4

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.1.1-4.1
- rebuild

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 2.1.1-4
- rebuild for -devel deps

* Tue Apr 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.1.1-3
- apply .spec file cleanups from Matthias Saou (#172926)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.1.1-2.1
- bump again for double-long bug on ppc(64)

* Tue Feb  7 2006 Christopher Aillon <caillon@redhat.com> - 2.1.1-2
- Stop shipping the .a file in the main package

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.1.1-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 23 2005 John (J5) Palmieri <johnp@redhat.com> 2.1.1-1
- Update to upstream version 2.1.1
- Removed libmusicbrainz-2.0.2-missing-return.patch
- Removed libmusicbrainz-2.0.2-conf.patch

* Wed Mar 03 2005 John (J5) Palmieri <johnp@redhat.com> 2.0.2-14
- Add patch to fix percision cast error to compile correctly on s390x
 
* Wed Mar 03 2005 John (J5) Palmieri <johnp@redhat.com> 2.0.2-13
- rebuild with gcc 4.0

* Mon Nov 08 2004 Colin Walters <walters@redhat.com> 2.0.2-12
- Add libmusicbrainz-2.0.2-missing-return.patch (bug #137289)

* Thu Oct 07 2004 Colin Walters <walters@redhat.com> 2.0.2-11
- BuildRequire expat-devel

* Tue Sep 28 2004 Colin Walters <walters@redhat.com> 2.0.2-10
- Move .so symlink to -devel package

* Tue Aug 31 2004 Colin Walters <walters@redhat.com> 2.0.2-9
- Add ldconfig calls (bz #131281)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Dec 18 2003 Brent Fox <bfox@redhat.com> 2.0.2-6
- add a BuildPreReq for libstdc++-devel and gcc-c++ (bug #106556)
- add a Requires for libstdc++-devel for libmusicbrainz-devel

* Mon Sep  1 2003 Bill Nottingham <notting@redhat.com>
- Obsoletes musicbrainz-devel too

* Mon Sep  1 2003 Jonathan Blandford <jrb@redhat.com>
- Obsoletes musicbrainz

* Fri Aug 22 2003 Bill Nottingham <notting@redhat.com> 2.0.2-5
- fix autoconf/libtool weirdness, remove exclusivearch

* Fri Aug 22 2003 Brent Fox <bfox@redhat.com> 2.0.2-4
- add ExcludeArch for s390x (something is really broken)

* Fri Aug 22 2003 Brent Fox <bfox@redhat.com> 2.0.2-3
- add ExcludeArch for ppc64

* Fri Aug 22 2003 Brent Fox <bfox@redhat.com> 2.0.2-2
- add ExcludeArch for x86_64 for now

* Thu Aug 21 2003 Brent Fox <bfox@redhat.com> 
- Initial build.


