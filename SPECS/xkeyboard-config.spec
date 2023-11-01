# INFO: Package contains data-only, no binaries, so no debuginfo is needed
%global debug_package %{nil}

#global gitdate 20110415
#global gitversion 19a0026b5

Summary:    X Keyboard Extension configuration data
Name:       xkeyboard-config
Version:    2.28
Release:    1%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}
License:    MIT
URL:        http://www.freedesktop.org/wiki/Software/XKeyboardConfig

%if 0%{?gitdate}
Source0:    %{name}-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh
Source2:    commitid
%else
Source0:    http://xorg.freedesktop.org/archive/individual/data/%{name}/%{name}-%{version}.tar.bz2
%endif

BuildArch:  noarch

BuildRequires:  gettext gettext-devel
BuildRequires:  libtool
BuildRequires:  libxslt
BuildRequires:  perl(XML::Parser)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(x11) >= 1.4.3
BuildRequires:  pkgconfig(xorg-macros) >= 1.12
BuildRequires:  pkgconfig(xproto) >= 7.0.20
BuildRequires:  xkbcomp
BuildRequires:  git

%if 0%{?gitdate}
BuildRequires:  git-core
%endif

%description
This package contains configuration data used by the X Keyboard Extension (XKB),
which allows selection of keyboard layouts when using a graphical interface.

%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig

%description devel
Development files for %{name}.

%prep
%autosetup -S git

%build
autoreconf -v --force --install || exit 1
%configure \
    --enable-compat-rules \
    --with-xkb-base=%{_datadir}/X11/xkb \
    --with-xkb-rules-symlink=xorg

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# Remove unnecessary symlink
rm -f $RPM_BUILD_ROOT%{_datadir}/X11/xkb/compiled
%find_lang %{name} 

# Create filelist
{
   FILESLIST=${PWD}/files.list
   pushd $RPM_BUILD_ROOT
   find .%{_datadir}/X11/xkb -type d | sed -e "s/^\./%dir /g" > $FILESLIST
   find .%{_datadir}/X11/xkb -type f | sed -e "s/^\.//g" >> $FILESLIST
   popd
}

%files -f files.list -f %{name}.lang
%doc AUTHORS README NEWS TODO COPYING docs/README.* docs/HOWTO.*
%{_datadir}/X11/xkb/rules/xorg
%{_datadir}/X11/xkb/rules/xorg.lst
%{_datadir}/X11/xkb/rules/xorg.xml
%{_mandir}/man7/xkeyboard-config.*

%files devel
%{_datadir}/pkgconfig/xkeyboard-config.pc

%changelog
* Tue Oct 29 2019 Peter Hutterer <peter.hutterer@redhat.com> 2.28-1
- xkeyboard-config 2.28 (#1728817)

* Fri Jul 06 2018 Peter Hutterer <peter.hutterer@redhat.com> 2.24-3
- Remove high-keycode removal patches, xkbcomp 1.4.2 has been in stable for
  long enough (related #1587998)

* Thu Jun 07 2018 Peter Hutterer <peter.hutterer@redhat.com> 2.24-2
- Revert two high keycode mappings, xkbcomp fails to parse those.
  (#1587998)

* Tue Jun 05 2018 Peter Hutterer <peter.hutterer@redhat.com> 2.24-1
- xkeyboard-config 2.24

* Wed Feb 07 2018 Peter Hutterer <peter.hutterer@redhat.com> 2.23.1-1
- Fix typo in polish keyboard layout
- xkeyboard-config 2.23.1
- use autosetup

* Wed Jan 31 2018 Peter Hutterer <peter.hutterer@redhat.com> 2.23-1
- xkeyboard-config 2.23

* Fri Oct 06 2017 Peter Hutterer <peter.hutterer@redhat.com> 2.22-1
- xkeyboard-config 2.22

* Tue Sep 05 2017 Peter Hutterer <peter.hutterer@redhat.com> 2.21-3
- Fix typo in tel-salara (#1469407)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 01 2017 Peter Hutterer <peter.hutterer@redhat.com> 2.21-1
- xkeyboard-config 2.21

* Fri May 12 2017 Hans de Goede <hdegoede@redhat.com> - 2.20-4
- Add evdev mappings for KEY_SOUND, KEY_UWB, KEY_WWAN and KEY_RFKILL

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Peter Hutterer <peter.hutterer@redhat.com> 2.20-2
- Add BuildRequires: git

* Wed Feb 01 2017 Peter Hutterer <peter.hutterer@redhat.com> 2.20-1
- xkeyboard-config 2.20

* Mon Dec 05 2016 Peter Hutterer <peter.hutterer@redhat.com> 2.19-2
- Bump to keep F25 upgrade path happy, no changes.

* Tue Oct 11 2016 Peter Hutterer <peter.hutterer@redhat.com> 2.19-1
- xkeyboard-config 2.19

* Fri Jun 03 2016 Peter Hutterer <peter.hutterer@redhat.com> 2.18-1
- xkeyboard-config 2.18

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Peter Hutterer <peter.hutterer@redhat.com> 2.17-1
- xkeyboard-config 2.17

* Wed Jan 20 2016 Peter Hutterer <peter.hutterer@redhat.com>
- s/define/global/

* Tue Dec 22 2015 Peter Hutterer <peter.hutterer@redhat.com> 2.16-2
- Add br(thinkpad) to the xml file (#1292881)

* Thu Oct 15 2015 Peter Hutterer <peter.hutterer@redhat.com> 2.16-1
- xkeyboard-config 2.16

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Peter Hutterer <peter.hutterer@redhat.com> 2.15-1
- xkeyboard-config 2.15

* Thu Jan 29 2015 Peter Hutterer <peter.hutterer@redhat.com> 2.14-1
- xkeyboard-config 2.14

* Tue Nov 11 2014 Peter Hutterer <peter.hutterer@redhat.com> 2.13-3
- Add U+05BA (point holam haser for vav) on il(biblical) (#1132511)

* Thu Oct 23 2014 Simone Caronni <negativo17@gmail.com> - 2.13-2
- Clean up SPEC file, fix rpmlint warnings.
- Remove non-valid configure option.

* Wed Oct 01 2014 Adam Jackson <ajax@redhat.com> 2.13-1
- xkeyboard-config 2.13

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Peter Hutterer <peter.hutterer@redhat.com> 2.12-1
- xkeyboard-config 2.12

* Thu Jan 30 2014 Peter Hutterer <peter.hutterer@redhat.com> 2.11-1
- xkeyboard-config 2.11

* Mon Oct 07 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.10.1-1
- xkeyboard-config 2.20.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.9-3
- Fix changelog - percent sign needs to be escaped

* Wed Jul 17 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.9-2
- Fix up three bogus changelog dates

* Thu May 30 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.9-1
- xkeyboard-config 2.9

* Wed May 15 2013 Daniel Drake <dsd@laptop.org> 2.8-3
- Add upstream patches for OLPC mechanical keyboard support

* Tue Apr 16 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.8-2
- Fix a bunch of language codes (#952510, #952519)

* Thu Jan 31 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.8-1
- xkeyboard-config 2.8

* Wed Jan 02 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.7-4
- Fix Mali layout previously mapped to in(mal) (#647433)

* Wed Nov 14 2012 Peter Hutterer <peter.hutterer@redhat.com> - 2.7-3
- Rebuild with fixed xkbcomp, re-create the right directory listing (not
  that anyone actually uses it)

* Wed Oct 31 2012 Peter Hutterer <peter.hutterer@redhat.com> - 2.7-2
- Fix {?dist} tag

* Thu Sep 27 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.7-1
- xkeyboard-config 2.7

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.6-2
- Revert broken fix for is keyboard (#826220)

* Thu May 31 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.6-1
- xkeyboard-config 2.6
- change source URL, 2.6 is in a different directory
- force autoreconf, update to use intltoolize as autopoint

* Wed May 23 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.5.1-2
- Add upstream patch to fix OLPC azerty keyboard

* Thu Feb 02 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.5.1-1
- xkeyboard-config 2.5.1

* Mon Jan 23 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.5-1
- xkeyboard-config 2.5

* Thu Jan 19 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.4.1-4
- Move Ungrab and ClearGrab from the default layout to option
  grab:break_actions (#783044)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.4.1-2
- Change Serbian layouts to mark the cyrillic ones (#769751)

* Wed Oct 05 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.4.1-1
- xkeyboard-config 2.4.1
- change source URL from ftp.x.org to http://xorg.freedesktop.org, ftp takes
  too long to update

* Tue Jun 14 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.3-2
- Add 0001-Use-XSL-to-generate-man-page-from-the-rules-XML.patch, ship
  man-page
- Fix up broken git repo initialization when building from a tarball

* Thu Jun 02 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.3-1
- xkeyboard-config 2.3

* Fri Apr 15 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.2.1-2.20110415git19a0026b5
- Snapshot from git to fix French Canadian layouts (#694472)

* Wed Apr 06 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.2.1-1
- xkeyboard-config 2.2.1, 2.2 had a broken configure check
- Add new BR and don't disable build/runtime deps checks

* Mon Apr 04 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.2-1
- xkeyboard-config 2.2
- reinstate the git bits removed in previous commit

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.99-2
- Update to 2.1.99 release

* Fri Mar 11 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.1.99-1.20110311-git9333b2f3
- add bits required to build from git
- update to today's git snapshot

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.1-1
- xkeyboard-config 2.1
