# This spec file is licensed under GPL-3.0-or-later
# grub-btrfs is Copyright (C) Antynea, licensed under GPL-3.0-or-later

Name:           grub-btrfs
Version:        4.14
Release:        1%{?dist}
Summary:        Include btrfs snapshots in GRUB boot options

License:        GPL-3.0-or-later
URL:            https://github.com/Antynea/grub-btrfs
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  systemd-rpm-macros

Requires:       btrfs-progs
Requires:       grub2-tools
Requires:       bash >= 4.0
Requires:       gawk
Recommends:     inotify-tools

%description
grub-btrfs adds Btrfs snapshots to the GRUB boot menu, allowing you to
boot into a snapshot directly from GRUB. Supports manual snapshots,
snapper, and timeshift.

%prep
%autosetup

for option in \
    '^#GRUB_BTRFS_SNAPSHOT_KERNEL_PARAMETERS=' \
    '^#GRUB_BTRFS_GRUB_DIRNAME=' \
    '^#GRUB_BTRFS_MKCONFIG=' \
    '^#GRUB_BTRFS_SCRIPT_CHECK='; do
    if ! grep -q "$option" config; then
        echo "ERROR: expected config option not found: $option" >&2
        echo "Upstream config layout changed; review %%prep before bumping." >&2
        exit 1
    fi
done

if ! grep -q 'id -u' Makefile; then
    echo "ERROR: expected root-check pattern not found in Makefile" >&2
    echo "Upstream Makefile changed; review the install-target patch." >&2
    exit 1
fi

sed -i \
  -e '/^#GRUB_BTRFS_SNAPSHOT_KERNEL_PARAMETERS=/a GRUB_BTRFS_SNAPSHOT_KERNEL_PARAMETERS="rd.live.overlay.overlayfs=1"' \
  -e '/^#GRUB_BTRFS_GRUB_DIRNAME=/a GRUB_BTRFS_GRUB_DIRNAME="/boot/grub2"' \
  -e '/^#GRUB_BTRFS_MKCONFIG=/a GRUB_BTRFS_MKCONFIG=/usr/sbin/grub2-mkconfig' \
  -e '/^#GRUB_BTRFS_SCRIPT_CHECK=/a GRUB_BTRFS_SCRIPT_CHECK=grub2-script-check' \
  config

# Remove the "must be root" check from the install target — rpmbuild runs as non-root
# and DESTDIR-based installs don't need root privileges
sed -i '/test "$(shell id -u)" != 0/,/^[[:space:]]*fi$/d' Makefile

%build
# Nothing to compile — grub-btrfs is shell scripts

%install
make install DESTDIR=%{buildroot} PREFIX=/usr SYSTEMD=true INITCPIO=false GRUB_UPDATE_EXCLUDE=true

%post
%systemd_post grub-btrfsd.service

%preun
%systemd_preun grub-btrfsd.service

%postun
%systemd_postun_with_restart grub-btrfsd.service

%files
%license %{_datadir}/licenses/grub-btrfs/LICENSE
%doc %{_datadir}/doc/grub-btrfs/README.md
%doc %{_datadir}/doc/grub-btrfs/initramfs-overlayfs.md
%config(noreplace) %{_sysconfdir}/default/grub-btrfs/config
%{_sysconfdir}/grub.d/41_snapshots-btrfs
%{_bindir}/grub-btrfsd
%{_unitdir}/grub-btrfsd.service
%{_mandir}/man8/grub-btrfs.8*
%{_mandir}/man8/grub-btrfsd.8*

%changelog
* Sat May 02 2026 zzahkaboom24 fedora@zzahkaboom24.de - 4.14-1
- Update to upstream 4.14
- Initial package for Fedora 44+
- Apply Fedora-specific config defaults during build
