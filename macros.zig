%zig_arches x86_64 aarch64 riscv64 %{mips64}

%_zig_version @@ZIG_VERSION@@
%__zig /usr/bin/zig

%zig_build \
    %__zig \\\
        --verbose  \\\
        --cache-dir zig-cache

%zig_install \
    DESTDIR="%{buildroot}" %zig_build \\\
        --prefix "%{_prefix}" \\
        --output-lib-dir "%{_libdir}" \\\
        --output-exe-dir "%{_bindir}" \\\
        --output-include-dir "%{_includedir}" \\\
        install

%zig_test \
    %zig_build \\\
        test