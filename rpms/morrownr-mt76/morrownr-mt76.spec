%define revision        92507536fbbedaaa1e20e103ad67a502a7a50b0b
%global debug_package   %{nil}

Name:           morrownr-mt76
Version:        0.git%{revision}
Release:        1
Summary:        Provides modern, mac80211, out-of-tree (out-of-kernel) Linux driver support for Mediatek wireless chips
License:        BSD-3-Clause
URL:            https://github.com/morrownr/mt76
Source0:        https://github.com/morrownr/mt76/archive/%{revision}.zip

Requires:       %{name}-kmod >= %{version}
Provides:       %{name}-kmod-common = %{version}
BuildRequires:  xz


%description
Provides modern, mac80211, out-of-tree (out-of-kernel) Linux driver support for
the following Mediatek wireless chips: MT7610, MT7630, MT7650, MT7612, MT7662,
MT7615, MT7663, MT7902, MT7920, MT7921, MT7922, MT7925, MT7927 and MT7928. Code
level equal to kernel 7.3 as of 2026-07-24.

%prep
%setup -q -C


%install
make install_fw FWDIR=%{buildroot}/lib/firmware/mediatek
find %{buildroot}/lib/firmware/mediatek -name '*.bin' -exec xz -f -C crc32 {} \;


%files
%license LICENSE
%doc MAINTAINING.md README.md SENDING-A-PATCH.md
/lib/firmware/mediatek
