#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/qcom-caf/sm8450',
    'hardware/qcom-caf/wlan',
    'hardware/xiaomi',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'libar-pal',
        'libpalclient',
    ): lib_fixup_remove,
}

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'vendor.qti.hardware.qccsyshal@1.0',
        'vendor.qti.hardware.qccsyshal@1.1',
        'vendor.qti.hardware.qccvndhal@1.0',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.qti.diaghal@1.0',
        'vendor.qti.hardware.wifidisplaysession@1.0',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    'system_ext/bin/wfdservice64': blob_fixup()
        .add_needed('libwfdservice_shim.so'),
    'system_ext/lib64/libwfdmmsrc_system.so': blob_fixup()
        .add_needed('libgui_shim.so'),
    'system_ext/lib64/libwfdnative.so': blob_fixup()
        .add_needed('libbinder_shim.so')
        .add_needed('libinput_shim.so')
        .remove_needed('android.hidl.base@1.0.so'),
    'system_ext/lib64/libwfdservice.so': blob_fixup()
        .add_needed('libaudioclient_shim.so')
        .replace_needed(
            'android.hardware.common-V2-ndk_platform.so',
            'android.hardware.common-V2-ndk.so'
        )
        .replace_needed(
            'android.media.audio.common.types-V2-cpp.so',
            'android.media.audio.common.types-V4-cpp.so'
        ),
    (
        'vendor/bin/hw/android.hardware.gnss-aidl-service-qti',
        'vendor/lib64/hw/android.hardware.gnss-aidl-impl-qti.so',
        'vendor/lib64/libgarden.so',
        'vendor/lib64/libgarden_haltests_e2e.so'
    ): blob_fixup()
        .replace_needed(
            'android.hardware.gnss-V1-ndk_platform.so',
            'android.hardware.gnss-V1-ndk.so'
        ),
    'vendor/bin/qcc-trd': blob_fixup()
        .replace_needed(
            'libgrpc++_unsecure.so',
            'libgrpc++_unsecure_prebuilt.so'
        ),
    (
        'vendor/etc/camera/pureView_parameter.xml',
        'vendor/etc/camera/pureShot_parameter.xml'
    ): blob_fixup()
        .regex_replace(r'=(\d+)>', r'="\1">'),
    'vendor/etc/media_codecs_parrot_v0.xml': blob_fixup()
        .regex_replace('.+media_codecs_(google_audio|google_c2|google_telephony|vendor_audio).+\n', ''),
    'vendor/etc/vintf/manifest/c2_manifest_vendor.xml': blob_fixup()
        .regex_replace('.+dolby.+\n', ''),
    (
        'vendor/lib64/hw/camera.qcom.so',
        'vendor/lib64/hw/com.qti.chi.override.so',
        'vendor/lib64/libcamxcommonutils.so',
        'vendor/lib64/libmialgoengine.so'
    ): blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    (
        'vendor/lib64/libagm.so',
        'vendor/lib64/libar-pal.so',
        'vendor/lib64/libaudioroute_ext.so',
        'vendor/lib64/libkaraokepal.so',
        'vendor/lib64/libmcs.so'
    ): blob_fixup()
        .replace_needed('libaudioroute.so', 'libaudioroute-v34.so'),
    'vendor/lib64/libQnnDspV65CalculatorStub.so': blob_fixup()
        .add_needed('liblog.so'),
    (
        'vendor/lib64/libalhLDC.so',
        'vendor/lib64/libalLDC.so',
        'vendor/lib64/libTrueSight.so',
        'vendor/lib64/libMiVideoFilter.so'
    ): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_lockPlanes')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
    'vendor/lib64/libcamximageformatutils.so': blob_fixup()
        .replace_needed(
            'vendor.qti.hardware.display.config-V2-ndk_platform.so',
            'vendor.qti.hardware.display.config-V2-ndk.so'
        ),
    (
        'vendor/lib64/libqtikeymint.so',
        'vendor/bin/hw/android.hardware.security.keymint-service-qti',
    ): blob_fixup()
        .replace_needed(
            'android.hardware.security.keymint-V1-ndk_platform.so',
            'android.hardware.security.keymint-V1-ndk.so'
        )
        .replace_needed(
            'android.hardware.security.secureclock-V1-ndk_platform.so',
            'android.hardware.security.secureclock-V1-ndk.so'
        )
        .replace_needed(
            'android.hardware.security.sharedsecret-V1-ndk_platform.so',
            'android.hardware.security.sharedsecret-V1-ndk.so'
        )
        .add_needed('android.hardware.security.rkp-V1-ndk.so'),
    'vendor/lib64/nfc_nci.nqx.default.hw.v1.so': blob_fixup()
        .add_needed('libbase_shim.so'),
    'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
        .add_needed('libhidlbase_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'garnet',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
