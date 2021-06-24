%zig_arches x86_64 aarch64 riscv64 %{mips64}

%_zig_version @@ZIG_VERSION@@
%__zig /usr/bin/zig

%zig_build \
    %__zig \\\
        --verbose  \\\
        --cache-dir zig-cache

%zig_install \
    DESTDIR="%{buildroot}" %zig_build \\\
        --prefix "%{_prefix}" \\\
        --prefix-lib-dir "%{_libdir}" \\\
        --prefix-exe-dir "%{_bindir}" \\\
        --prefix-include-dir "%{_includedir}" \\\
        install

%zig_test \
    %zig_build \\\
        test
