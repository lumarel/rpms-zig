# https://ziglang.org/download/0.8.0/release-notes.html#Support-Table
# 32 bit builds currently run out of memory https://github.com/ziglang/zig/issues/6485
%global         zig_arches x86_64 aarch64 riscv64 %{mips64}

Name:           zig
Version:        0.8.0
Release:        1%{?dist}
Summary:        Programming language for maintaining robust, optimal, and reusable software

License:        MIT and NCSA and LGPLv2+ and LGPLv2+ with exceptions and GPLv2+ and GPLv2+ with exceptions and BSD and Inner-Net and ISC and Public Domain and GFDL and ZPLv2.1
URL:            https://ziglang.org
Source0:        https://github.com/ziglang/zig/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        macros.%{name}

# https://github.com/ziglang/zig/pull/9020
Patch0:         0001-specify-the-output-lib-exe-and-include-paths-with-fl.patch
Patch1:         0002-zig-build-rename-lib-dir-include-dir-exe-dir.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  llvm-devel
BuildRequires:  clang-devel
BuildRequires:  lld-devel
# for man page generation
BuildRequires:  help2man
# for the macro
BuildRequires:  sed
# for testing
#BuildRequires:  elfutils-libelf-devel
#BuildRequires:  libstdc++-static

Requires:       %{name}-libs = %{version}

# These packages are bundled as source

# NCSA
Provides: bundled(compiler-rt) = 12.0.0
# LGPLv2+, LGPLv2+ with exceptions, GPLv2+, GPLv2+ with exceptions, BSD, Inner-Net, ISC, Public Domain and GFDL
Provides: bundled(glibc) = 2.33
# NCSA
Provides: bundled(libcxx) = 12.0.0
# NCSA
Provides: bundled(libcxxabi) = 12.0.0
# NCSA
Provides: bundled(libunwind) = 12.0.0
# BSD, LGPG, ZPL
Provides: bundled(mingw) = 8.0.0
# MIT
Provides: bundled(musl) = 1.2.2

ExclusiveArch: %{zig_arches}

%description
Zig is an open-source programming language designed for robustness, optimality,
and clarity. This package provides the zig compiler and the associated runtime.

# the standard library contains only plain text
%package libs
Summary:        zig standard library
BuildArch:      noarch

%description libs
Standard Zig library

%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}

%description doc
Documentation for %{name}. For more information, visit %{url}

%package        rpm-macros
Summary:        Common RPM macros for %{name}
Requires:       rpm
BuildArch:      noarch

%description    rpm-macros  
This package contains common RPM macros for %{name}.

%prep
%autosetup -p1

%build

%cmake \
    -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo \
    -DZIG_PREFER_CLANG_CPP_DYLIB=true \
    -DZIG_VERSION:STRING="%{version}"
%cmake_build

# Zig has no official manpage
# https://github.com/ziglang/zig/issues/715
help2man --no-discard-stderr "%{__cmake_builddir}/zig" --version-option=version --output=%{name}.1

ln -s lib "%{__cmake_builddir}/"

# buildings docs fails on rawhide due to the libc version
%{__cmake_builddir}/zig build docs -Dversion-string="%{version}" || true
touch zig-cache/langref.html

%install
%cmake_install

mkdir -p %{buildroot}/%{_mandir}/man1
install -m 0644 %{name}.1 %{buildroot}%{_mandir}/man1/

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d/

install -p -m644 %{SOURCE1} %{buildroot}%{_rpmconfigdir}/macros.d/
sed -i -e "s|@@ZIG_VERSION@@|%{version}|"  %{buildroot}%{_rpmconfigdir}/macros.d/macros.%{name}

%check

# tests are affected by an LLVM regression
# https://bugs.llvm.org/show_bug.cgi?id=49401
# https://github.com/ziglang/zig/issues/8130
# %%{__cmake_builddir}/zig build test

%files
%license LICENSE
%{_bindir}/zig
%{_mandir}/man1/%{name}.1.*

%files libs
%{_prefix}/lib/%{name}

%files doc
%doc README.md
%doc zig-cache/langref.html
    
%files rpm-macros
%{_rpmconfigdir}/macros.d/macros.%{name}

%changelog
* Sat Jun 05 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.8.0-1
- Update to Zig 0.8.0

* Sun Dec 13 23:18:24 CET 2020 Jan Drögehoff <sentrycraft123@gmail.com> - 0.7.1-1
- Update to Zig 0.7.1

* Wed Nov 11 17:18:27 CET 2020 Jan Drögehoff <sentrycraft123@gmail.com> - 0.7.0-1
- Update to Zig 0.7.0

* Tue Aug 18 2020 Jan Drögehoff <sentrycraft123@gmail.com> - 0.6.0-1
- Initial zig spec

