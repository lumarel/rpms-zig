%zig_arches x86_64 aarch64 riscv64 %{mips64}

%__zig %{_bindir}/zig

%_zig_cache_dir %{_vpath_builddir}/zig-cache
%_zig_package_dir %{_zig_cache_dir}/p

# expected features for each arch when targeting baseline
# found in https://github.com/ziglang/zig/tree/master/lib/std/Target
#
# aarch64:
#   enable_select_opt, ete, fuse_adrp_add, fuse_aes, neon, use_postra_scheduler,
#
# x86_64:
#   cmov, cx8, fxsr, idivq_to_divl, macrofusion, mmx, nopl, slow_3ops_lea, slow_incdec, sse2, vzeroupper, x87
#
# riscv64:
#   a, c, d, i, m
#
# mips64:
#   mips64r2
#
%_zig_cpu baseline
%_zig_target native
%_zig_release_mode safe

# seperated build options
%_zig_general_options --verbose --release=%{_zig_release_mode} --build-id=sha1 --summary all
%_zig_project_options -Dtarget=%{_zig_target} -Dcpu=%{_zig_cpu}
# 0.16.0 introduced packaging changes which install packages into this relative directory
# Will be ovewritable in 0.17.0
# https://codeberg.org/ziglang/zig/pulls/31950
%_zig_system_integration --system "zig-pkg"
%_zig_advanced_options -fallow-so-scripts --cache-dir "%{_zig_cache_dir}" --global-cache-dir "%{_zig_cache_dir}"

%_zig_build_options %{?_zig_general_options} %{?_zig_project_options} %{?_zig_system_integration} %{?_zig_advanced_options} %{?zig_build_options}
%_zig_install_options --prefix "%{_prefix}" --prefix-lib-dir "%{_libdir}" --prefix-exe-dir "%{_bindir}" --prefix-include-dir "%{_includedir}" %{?zig_install_options}
%_zig_fetch_options --global-cache-dir %{_zig_cache_dir} %{?zig_fetch_options}
%_zig_test_options %{?zig_test_options}


%zig_prep %{shrink: \
    mkdir -p \
        %{_zig_cache_dir} \
        %{_zig_package_dir} \
        "zig-pkg" \
}

%zig_build %{shrink: \
    %__zig \
        build \
        %{?_zig_build_options} \
}

%zig_install %{shrink: \
    DESTDIR="%{buildroot}" \
    %zig_build \
        install \
        %{?_zig_install_options} \
}

%zig_fetch %{shrink: \
    %__zig \
        fetch \
        %{?_zig_fetch_options} \
}

%zig_test %{shrink: \
    %zig_build \
        test \
        %{?%_zig_test_options} \
}
