Summary:     Bootstrap a new Red Hat Enterprise Linux system (like debootstrap)
Name:        febootstrap
Version:     2.11
Release:     7%{?dist}
License:     GPLv2+
Group:       Development/Tools
URL:         http://et.redhat.com/~rjones/febootstrap/
Source0:     http://et.redhat.com/~rjones/febootstrap/files/%{name}-%{version}.tar.gz
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root
ExclusiveArch: x86_64

# Improve the stability of the checksum and reduce the need to rebuild
# the appliance.
Patch0:      0001-helper-Ignore-times-of-special-files-when-calculatin.patch

BuildRequires: /usr/bin/pod2man
BuildRequires: fakeroot >= 1.11
BuildRequires: fakechroot >= 2.9-20
BuildRequires: yum >= 3.2
BuildRequires: /sbin/mke2fs
BuildRequires: /sbin/insmod.static
BuildRequires: e2fsprogs-devel
BuildRequires: glibc-static
BuildRequires: prelink

Requires:    fakeroot >= 1.11
Requires:    fakechroot >= 2.9-20
Requires:    yum >= 3.2
Requires:    febootstrap-supermin-helper = %{version}-%{release}

# These are suggestions.  However making them hard requirements
# pulls in far too much stuff.
#Requires:    qemu
#Requires:    filelight
#Requires:    baobab     # Not as nice as filelight.


%description
febootstrap is a Red Hat Enterprise Linux equivalent to Debian's
debootstrap.  You can use it to create a basic Red Hat Enterprise
Linux or Fedora filesystem, and build initramfs (initrd.img) or
filesystem images.

febootstrap also includes a separate tool to minimize filesystems by
removing unneeded locales, documentation etc.

The main difference from other appliance building tools is that this
one doesn't need to be run as root.


%package supermin-helper
Summary:     Runtime support for febootstrap
Group:       Development/Tools
Requires:    util-linux-ng
Requires:    cpio
Requires:    /sbin/mke2fs
Requires:    /sbin/insmod.static
Obsoletes:   febootstrap < 2.11-6


%description supermin-helper
%{name}-supermin-helper contains the runtime support for %{name}.


%prep
%setup -q

%patch0 -p1


%build
%configure
make


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Clean up the examples/ directory which will get installed in %doc.
# In this case I don't want the scripts to be executable because
# people should read them carefully before running them.
rm examples/Makefile*
chmod -x examples/*.sh

# febootstrap-supermin-helper is marked as requiring an executable
# stack.  This happens because we use objcopy to create one of the
# component object files from a data file.  The program does not in
# fact require an executable stack.  The easiest way to fix this is to
# clear the flag here.
execstack -c $RPM_BUILD_ROOT%{_bindir}/febootstrap-supermin-helper


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README examples
%{_bindir}/febootstrap
%{_bindir}/febootstrap-run
%{_bindir}/febootstrap-install
%{_bindir}/febootstrap-minimize
%{_bindir}/febootstrap-to-initramfs
%{_bindir}/febootstrap-to-supermin
%{_mandir}/man8/febootstrap.8*
%{_mandir}/man8/febootstrap-run.8*
%{_mandir}/man8/febootstrap-install.8*
%{_mandir}/man8/febootstrap-minimize.8*
%{_mandir}/man8/febootstrap-to-initramfs.8*
%{_mandir}/man8/febootstrap-to-supermin.8*


%files supermin-helper
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/febootstrap-supermin-helper
%{_mandir}/man8/febootstrap-supermin-helper.8*


%changelog
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
