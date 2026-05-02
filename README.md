# grub-btrfs RPM packaging for Fedora

Unofficial RPM packaging of [Antynea/grub-btrfs](https://github.com/Antynea/grub-btrfs)
for Fedora 43, 44, and Rawhide.

## Why this exists

The previously available [kylegospo/grub-btrfs Copr](https://copr.fedorainfracloud.org/coprs/kylegospo/grub-btrfs/)
has not been updated in 3 years. This repo provides current packaging of
upstream releases.

## Installation

```bash
sudo dnf copr enable zzahkaboom24/grub-btrfs
sudo dnf install grub-btrfs
```

After installing, configure the daemon for Timeshift (skip if using Snapper):

```bash
sudo systemctl edit --full grub-btrfsd
# Change ExecStart= to:
# ExecStart=/usr/bin/grub-btrfsd --syslog --timeshift-auto

sudo systemctl enable --now grub-btrfsd
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
```

Reboot. You should see a "Fedora Linux snapshots" submenu in GRUB.

## What's modified from upstream

- Config defaults patched for Fedora paths during build (`/boot/grub2`,
  `/usr/sbin/grub2-mkconfig`, etc.)
  - Read [this](https://github.com/Antynea/grub-btrfs/issues/419#issuecomment-4165437249) for more info how I found out about it
  - I found grub2-mkconfig in both of these locations
    ```
    which grub2-mkconfig
    ls -la /usr/bin/grub2-mkconfig /usr/sbin/grub2-mkconfig
    -rwxr-xr-x. 1 root root 9208 Apr  8 02:00 /usr/bin/grub2-mkconfig
    -rwxr-xr-x. 1 root root 9208 Apr  8 02:00 /usr/sbin/grub2-mkconfig
    ```
- Makefile's "must be root" check removed (rpmbuild correctly runs non-root)
- Arch Linux initramfs hooks excluded (Fedora doesn't use mkinitcpio)

## Building locally

```bash
git clone https://github.com/zzahkaboom24/grub-btrfs-rpm.git
cd grub-btrfs-rpm
spectool -g -R grub-btrfs.spec
rpmbuild -ba grub-btrfs.spec
```

## License

The packaging files in this repo are licensed under GPL-3.0-or-later, matching
the upstream grub-btrfs project. Upstream grub-btrfs is Copyright (C) Antynea,
also GPL-3.0-or-later.


