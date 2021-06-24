%zig_arches x86_64 aarch64 riscv64 %{mips64}

%_zig_version @@ZIG_VERSION@@
%zig /usr/bin/zig

%zig_build \
    %zig \\\
        build \\\
        --verbose  \\\
        --cache-dir zig-cache

%zig_install \
    DESTDIR="%{buildroot}" %zig_build \\\
        install \\\ 
        --prefix "%{_prefix}" \\\
        --prefix-lib-dir "%{_libdir}" \\\
        --prefix-exe-dir "%{_bindir}" \\\
        --prefix-include-dir "%{_includedir}"

%zig_test \
    %zig_build \\\
        test
