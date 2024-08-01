################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
C:/Users/Bach/Documents/GitHub/gecko_sdk/platform/radio/rail_lib/plugin/pa-conversions/pa_conversions_efr32.c 

OBJS += \
./gecko_sdk_4.4.3/platform/radio/rail_lib/plugin/pa-conversions/pa_conversions_efr32.o 

C_DEPS += \
./gecko_sdk_4.4.3/platform/radio/rail_lib/plugin/pa-conversions/pa_conversions_efr32.d 


# Each subdirectory must supply rules for building sources it contributes
gecko_sdk_4.4.3/platform/radio/rail_lib/plugin/pa-conversions/pa_conversions_efr32.o: C:/Users/Bach/Documents/GitHub/gecko_sdk/platform/radio/rail_lib/plugin/pa-conversions/pa_conversions_efr32.c gecko_sdk_4.4.3/platform/radio/rail_lib/plugin/pa-conversions/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: GNU ARM C Compiler'
	arm-none-eabi-gcc -g -gdwarf-2 -mcpu=cortex-m33 -mthumb -std=c99 '-DBGM220PC22HNA=1' '-DSL_APP_PROPERTIES=1' '-DBOOTLOADER_APPLOADER=1' '-DHARDWARE_BOARD_DEFAULT_RF_BAND_2400=1' '-DHARDWARE_BOARD_SUPPORTS_1_RF_BAND=1' '-DHARDWARE_BOARD_SUPPORTS_RF_BAND_2400=1' '-DSL_BOARD_NAME="BRD4314A"' '-DSL_BOARD_REV="A02"' '-DSL_COMPONENT_CATALOG_PRESENT=1' '-DMBEDTLS_CONFIG_FILE=<sl_mbedtls_config.h>' '-DMBEDTLS_PSA_CRYPTO_CONFIG_FILE=<psa_crypto_config.h>' '-DSL_RAIL_LIB_MULTIPROTOCOL_SUPPORT=0' '-DSL_RAIL_UTIL_PA_CONFIG_HEADER=<sl_rail_util_pa_config.h>' '-DSLI_RADIOAES_REQUIRES_MASKING=1' -I"C:\Users\Bach\Documents\GitHub\Mentor-TuDV8-TT-OpenLab-Fsoft\Project_Test_17072024\config" -I"C:\Users\Bach\Documents\GitHub\Mentor-TuDV8-TT-OpenLab-Fsoft\Project_Test_17072024\config\btconf" -I"C:\Users\Bach\Documents\GitHub\Mentor-TuDV8-TT-OpenLab-Fsoft\Project_Test_17072024\autogen" -IC:/Users/Bach/Documents/GitHub/Mentor-TuDV8-TT-OpenLab-Fsoft/Project_Test_17072024 -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/Device/SiliconLabs/BGM22/Include -IC:/Users/Bach/Documents/GitHub/gecko_sdk/app/common/util/app_assert -IC:/Users/Bach/Documents/GitHub/gecko_sdk/app/common/util/app_log -IC:/Users/Bach/Documents/GitHub/gecko_sdk/app/common/util/app_timer -IC:/Users/Bach/Documents/GitHub/gecko_sdk/protocol/bluetooth/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/common/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/protocol/bluetooth/bgcommon/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/protocol/bluetooth/bgstack/ll/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/hardware/board/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/bootloader -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/bootloader/api -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/CMSIS/Core/Include -IC:/Users/Bach/Documents/GitHub/gecko_sdk/hardware/driver/configuration_over_swo/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/security/sl_component/sl_cryptoacc_library/include -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/security/sl_component/sl_cryptoacc_library/src -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/driver/debug/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/service/device_init/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/emdrv/dmadrv/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/emdrv/common/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/emlib/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/radio/rail_lib/plugin/fem_util -IC:/Users/Bach/Documents/GitHub/gecko_sdk/app/bluetooth/common/gatt_service_device_information -IC:/Users/Bach/Documents/GitHub/gecko_sdk/app/bluetooth/common/in_place_ota_dfu -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/service/iostream/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/security/sl_component/sl_mbedtls_support/config -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/security/sl_component/sl_mbedtls_support/config/preset -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/security/sl_component/sl_mbedtls_support/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/util/third_party/mbedtls/include -IC:/Users/Bach/Documents/GitHub/gecko_sdk/util/third_party/mbedtls/library -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/service/mpu/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/emdrv/nvm3/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/service/power_manager/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/security/sl_component/sl_psa_driver/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/radio/rail_lib/common -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/radio/rail_lib/protocol/ble -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/radio/rail_lib/protocol/ieee802154 -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/radio/rail_lib/protocol/wmbus -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/radio/rail_lib/protocol/zwave -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/radio/rail_lib/chip/efr32/efr32xg2x -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/radio/rail_lib/protocol/sidewalk -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/radio/rail_lib/plugin/pa-conversions -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/radio/rail_lib/plugin/pa-conversions/efr32xg22 -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/radio/rail_lib/plugin/rail_util_power_manager_init -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/radio/rail_lib/plugin/rail_util_pti -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/security/sl_component/se_manager/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/security/sl_component/se_manager/src -IC:/Users/Bach/Documents/GitHub/gecko_sdk/util/silicon_labs/silabs_core/memory_manager -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/common/toolchain/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/service/system/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/service/sleeptimer/inc -IC:/Users/Bach/Documents/GitHub/gecko_sdk/platform/security/sl_component/sl_protocol_crypto/src -Os -Wall -Wextra -ffunction-sections -fdata-sections -imacrossl_gcc_preinclude.h -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mcmse --specs=nano.specs -c -fmessage-length=0 -MMD -MP -MF"gecko_sdk_4.4.3/platform/radio/rail_lib/plugin/pa-conversions/pa_conversions_efr32.d" -MT"$@" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


