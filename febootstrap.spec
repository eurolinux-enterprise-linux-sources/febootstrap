Summary:     Bootstrapping tool for creating supermin appliances
Name:        febootstrap
Version:     3.21
Release:     4%{?dist}
License:     GPLv2+
Group:       Development/Tools
URL:         http://people.redhat.com/~rjones/febootstrap/
Source0:     http://people.redhat.com/~rjones/febootstrap/files/%{name}-%{version}.tar.gz
Source1:     http://people.redhat.com/~rjones/febootstrap/files/%{name}-2.11.tar.gz
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root
ExclusiveArch: x86_64

Patch1:      0001-helper-Drop-supplemental-groups-when-using-g-command.patch
Patch2:      0001-Copy-sticky-setgid-bits-from-directory-to-base.img-a.patch
Patch3:      0001-Ignore-ghost-non-regular-files.patch
Patch4:      0001-helper-user-and-group-flags-require-an-argument.patch

BuildRequires: /usr/bin/pod2man
BuildRequires: fakeroot >= 1.11
BuildRequires: fakechroot >= 2.9-20
BuildRequires: yum >= 3.2
BuildRequires: /sbin/mke2fs
BuildRequires: e2fsprogs-devel
BuildRequires: glibc-static
BuildRequires: ocaml, ocaml-findlib-devel
BuildRequires: prelink
BuildRequires: zlib-static

Requires:    fakeroot >= 1.11
Requires:    fakechroot >= 2.9-20
Requires:    yum >= 3.2
Requires:    yum-utils
Requires:    febootstrap-supermin-helper = %{version}-%{release}

# These are suggestions.  However making them hard requirements
# pulls in far too much stuff.
#Requires:    qemu
#Requires:    filelight
#Requires:    baobab     # Not as nice as filelight.


%description
febootstrap is a tool for building supermin appliances.  These are
tiny appliances (similar to virtual machines), usually around 100KB in
size, which get fully instantiated on-the-fly in a fraction of a
second when you need to boot one of them.

Note that febootstrap in RHEL 6.3+ builds febootstrap (version 2.11)
and febootstrap3 (version %{version}).  This is for backwards
compatibility with RHEL 6.0, 6.1 and 6.2.


%package supermin-helper
Summary:     Runtime support for febootstrap
Group:       Development/Tools
Requires:    util-linux-ng
Requires:    cpio
Requires:    /sbin/mke2fs
Obsoletes:   febootstrap < 2.11-6


%description supermin-helper
%{name}-supermin-helper contains the runtime support for %{name}.


%prep
# This creates:
#   febootstrap-3.x/
#   febootstrap-3.x/febootstrap-3.x/    # febootstrap3
#   febootstrap-3.x/febootstrap-2.11/   # febootstrap
%setup -q -c
%setup -T -D -a 1

pushd %{name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
popd


%build
pushd %{name}-%{version}
%configure
make
popd

pushd %{name}-2.11
%configure
make
popd


%install
rm -rf $RPM_BUILD_ROOT

# Install febootstrap 3.x.
make -C %{name}-%{version} DESTDIR=$RPM_BUILD_ROOT install
mv $RPM_BUILD_ROOT%{_bindir}/febootstrap $RPM_BUILD_ROOT%{_bindir}/febootstrap3
mv $RPM_BUILD_ROOT%{_mandir}/man8/febootstrap.8 $RPM_BUILD_ROOT%{_mandir}/man8/febootstrap3.8 

# Install febootstrap 2.11.
make -C %{name}-2.11 DESTDIR=$RPM_BUILD_ROOT install

# But we want febootstrap-supermin-helper v3.  Both versions are
# compatible but the newest version has all the bug fixes.
rm $RPM_BUILD_ROOT%{_bindir}/febootstrap-supermin-helper
install -m 0755 %{name}-%{version}/helper/febootstrap-supermin-helper $RPM_BUILD_ROOT%{_bindir}/
rm $RPM_BUILD_ROOT%{_mandir}/man8/febootstrap-supermin-helper.8
install -m 0644 %{name}-%{version}/helper/febootstrap-supermin-helper.8 $RPM_BUILD_ROOT%{_mandir}/man8/

# febootstrap-supermin-helper is marked as requiring an executable
# stack.  This happens because we use objcopy to create one of the
# component object files from a data file.  The program does not in
# fact require an executable stack.  The easiest way to fix this is to
# clear the flag here.
execstack -c $RPM_BUILD_ROOT%{_bindir}/febootstrap-supermin-helper

# Doc files.
cp %{name}-%{version}/COPYING COPYING
cp %{name}-%{version}/README README3
cp %{name}-2.11/README README2


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README2 README3
%{_bindir}/febootstrap
%{_bindir}/febootstrap-run
%{_bindir}/febootstrap-install
%{_bindir}/febootstrap-minimize
%{_bindir}/febootstrap-to-initramfs
%{_bindir}/febootstrap-to-supermin
%{_bindir}/febootstrap3
%{_mandir}/man8/febootstrap.8*
%{_mandir}/man8/febootstrap-run.8*
%{_mandir}/man8/febootstrap-install.8*
%{_mandir}/man8/febootstrap-minimize.8*
%{_mandir}/man8/febootstrap-to-initramfs.8*
%{_mandir}/man8/febootstrap-to-supermin.8*
%{_mandir}/man8/febootstrap3.8*


%files supermin-helper
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/febootstrap-supermin-helper
%{_mandir}/man8/febootstrap-supermin-helper.8*


%changelog
* Mon Aug  5 2013 Richard Jones <rjones@redhat.com> - 3.21-4
- Fix directory permissions to include setgid and sticky bits.
- Ignore ghost non-regular files.
- Fix segfault when -u/-g options missing argument.
  related: rhbz#958184

* Fri Jun 28 2013 Richard Jones <rjones@redhat.com> - 3.21-2
- Drop supplemental groups when using -g command line option
  resolves: rhbz#902478

* Fri May 17 2013 Richard Jones <rjones@redhat.com> - 3.21-1
- Rebase to febootstrap 3.21.
  resolves: rhbz#958184
- Remove upstream patch.

* Wed Aug 15 2012 Richard Jones <rjones@redhat.com> - 3.12-2
- Hotfix: helper: Fix -u and -g options when host uses LDAP or NIS
  resolves: RHBZ#803962

* Tue Dec 20 2011 Richard Jones <rjones@redhat.com> - 3.12-1
- Rebase to febootstrap 3.12.
  resolves: RHBZ#719877

* Sat Aug 27 2011 Richard Jones <rjones@redhat.com> - 3.9-1
- Rebase to febootstrap 3.9.
  resolves: RHBZ#719877
- This package contains febootstrap (version 2.11) and febootstrap3.

* Thu Mar 17 2011 Richard Jones <rjones@redhat.com> - 2.11-7
- Splitting the package broke RHEL 6.0 -> 6.1 upgrades.  Add an Obsoletes
  header to fix this.
  resolves: RHBZ#669839

* Mon Jan 17 2011 Richard Jones <rjones@redhat.com> - 2.11-6
- Split package into febootstrap (for building) and febootstrap-supermin-helper
  (for running).  Note that febootstrap depends on febootstrap-supermin-helper,
  but you can install febootstrap-supermin-helper on its own (RHBZ#669839).

* Fri Jan 14 2011 Richard Jones <rjones@redhat.com> - 2.11-5
- Clear executable stack flag on febootstrap-supermin-helper.

* Sat Dec 11 2010 Richard W.M. Jones <rjones@redhat.com> - 2.11-3
- Backport patch to improve the stability of the checksum and reduce
  the need to rebuild the appliance.
- Add BR + Requires on insmod.static.

* Thu Nov 18 2010 Richard W.M. Jones <rjones@redhat.com> - 2.11-2
- Rebase to version 2.11 (RHBZ#628849).

* Thu Nov 18 2010 Richard W.M. Jones <rjones@redhat.com> - 2.10-2
- Rebase to version 2.10 (RHBZ#628849).
- Include fixes for building on ppc and ppc64 ...
- ... but set ExclusiveArch x86_64.

* Tue Jul  6 2010 Richard W.M. Jones <rjones@redhat.com> - 2.7-1.2
- Don't add extra characters after dist tag in release (RHBZ#604549).

* Thu May 27 2010 Richard W.M. Jones <rjones@redhat.com> - 2.7-1.el6.1
- Rebrand for Red Hat Enterprise Linux (RHBZ#594419).

* Mon May 17 2010 Richard Jones <rjones@redhat.com> - 2.7-1
- Backport version 2.7 from Rawhide (fixes RHBZ#592051).
- febootstrap-supermin-helper shell script rewritten in C for speed.
- This package contains C code so it is no longer 'noarch'.
- MAKEDEV isn't required.

* Fri Jan 22 2010 Richard Jones <rjones@redhat.com> - 2.6-1
- New upstream release 2.6.
- Recheck package in rpmlint.
- Import new package from Rawhide.

* Thu Oct 22 2009 Richard Jones <rjones@redhat.com> - 2.5-2
- New upstream release 2.5.
- Remove BR upx (not needed by upstream).
- Two more scripts / manpages.

* Thu Jul 30 2009 Richard Jones <rjones@redhat.com> - 2.4-1
- New upstream release 2.4.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 15 2009 Richard Jones <rjones@redhat.com> - 2.3-1
- New upstream release 2.3.

* Mon Jun 15 2009 Richard Jones <rjones@redhat.com> - 2.2-1
- New upstream release 2.2.

* Mon May 11 2009 Richard Jones <rjones@redhat.com> - 2.0-1
- New upstream release 2.0.

* Thu May  7 2009 Richard Jones <rjones@redhat.com> - 1.9-1
- New upstream release 1.9.

* Fri May  1 2009 Richard Jones <rjones@redhat.com> - 1.8-1
- New upstream release 1.8.

* Mon Apr 20 2009 Richard Jones <rjones@redhat.com> - 1.7-1
- New upstream release 1.7.

* Tue Apr 14 2009 Richard Jones <rjones@redhat.com> - 1.5-3
- Configure script has (unnecessary) BuildRequires on fakeroot,
  fakechroot, yum.

* Tue Apr 14 2009 Richard Jones <rjones@redhat.com> - 1.5-2
- Initial build for Fedora.
