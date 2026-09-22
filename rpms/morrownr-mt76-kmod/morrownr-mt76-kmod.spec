# (un)define the next line to either build for the newest or all current kernels
%define buildforkernels newest
#define buildforkernels current
#define buildforkernels akmod
#define kernels         blah.fc44.x86_64

%define revision        92507536fbbedaaa1e20e103ad67a502a7a50b0b

# name should have a -kmod suffix
Name:           morrownr-mt76-kmod

Version:        0.git%{revision}
Release:        1
Summary:        Provides modern, mac80211, out-of-tree (out-of-kernel) Linux driver support for Mediatek wireless chips

Group:          System Environment/Kernel

License:        BSD-3-Clause
URL:            https://github.com/morrownr/mt76
Source0:        https://github.com/morrownr/mt76/archive/%{revision}.zip
Patch0:         no-depmod-when-make-install.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  %{_bindir}/kmodtool


# Verify that the package build for all architectures.
# In most time you should remove the Exclusive/ExcludeArch directives
# and fix the code (if needed).
# ExclusiveArch:  i686 x86_64 ppc64 ppc64le armv7hl aarch64
# ExcludeArch: i686 x86_64 ppc64 ppc64le armv7hl aarch64

# get the proper build-sysbuild package from the repo, which
# tracks in all the kernel-devel packages
BuildRequires:  %{_bindir}/kmodtool

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }


%description
Provides modern, mac80211, out-of-tree (out-of-kernel) Linux driver support for
the following Mediatek wireless chips: MT7610, MT7630, MT7650, MT7612, MT7662,
MT7615, MT7663, MT7902, MT7920, MT7921, MT7922, MT7925, MT7927 and MT7928. Code
level equal to kernel 7.3 as of 2026-07-24.


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0
%patch 0 -p 1 -d mt76-%{revision}

for kernel_version in %{?kernel_versions} ; do
    cp -a mt76-%{revision} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
    make modules %{?_smp_mflags} -C "${kernel_version##*___}" M=${PWD}/_kmod_build_${kernel_version%%___*}
done


%install
rm -rf ${RPM_BUILD_ROOT}

for kernel_version in %{?kernel_versions}; do
    make install -C ${PWD}/_kmod_build_${kernel_version%%___*} MODDIR=${RPM_BUILD_ROOT}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
done
%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT
