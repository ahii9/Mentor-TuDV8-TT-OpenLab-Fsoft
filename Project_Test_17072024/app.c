/***************************************************************************//**
 * @file
 * @brief Core application logic.
 *******************************************************************************
 * # License
 * <b>Copyright 2020 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 * The licensor of this software is Silicon Laboratories Inc.
 *
 * This software is provided 'as-is', without any express or implied
 * warranty. In no event will the authors be held liable for any damages
 * arising from the use of this software.
 *
 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely, subject to the following restrictions:
 *
 * 1. The origin of this software must not be misrepresented; you must not
 *    claim that you wrote the original software. If you use this software
 *    in a product, an acknowledgment in the product documentation would be
 *    appreciated but is not required.
 * 2. Altered source versions must be plainly marked as such, and must not be
 *    misrepresented as being the original software.
 * 3. This notice may not be removed or altered from any source distribution.
 *
 ******************************************************************************/
#include "em_common.h"
#include "app_assert.h"
#include "sl_bluetooth.h"
#include "gatt_db.h"
#include "app.h"
/*******************************************************************************
 * Define
 */
#define TRIGGER_PIN 1
#define TRIGGER_PORT gpioPortB
#define ECHO_PIN 2
#define ECHO_PORT gpioPortB
/**************************************************************
 * Externs
 **************************************************************/
extern bool Timer0_OF;
/*********************************************************************************
 * Variable
 */
// The advertising set handle allocated from Bluetooth stack.
static uint8_t advertising_set_handle = 0xff;
uint32_t count = 0;
uint32_t distance;
uint32_t distance_test = 100;
bool trigger_done = false;
bool echo_time_out = false;
/******************************************************************************
 * Function user
 */
void delayMs(uint32_t time, bool *Timer0_OF) {

    while (time != 0) {
        if (*Timer0_OF) {
            time = time - 1;
            *Timer0_OF = false;  // Đặt lại cờ Timer0_OF
        }
        //app_log("time = %d \n", time);
    }
}

static sl_status_t send_data_distance(uint8_t connection,
                                              uint16_t characteristic,
                                              uint32_t distance);
/**************************************************************************//**
 * Application Init.
 *****************************************************************************/
SL_WEAK void app_init(void)
{
  //GPIO_PinModeSet(gpioPortA, 4, gpioModePushPull, 1);
  CMU_ClockEnable(cmuClock_GPIO, true);
  GPIO_PinModeSet(gpioPortB, ECHO_PIN, gpioModeInput, 0);
  GPIO_PinModeSet(gpioPortB, TRIGGER_PIN, gpioModePushPull, 1);
  Timer0_Init();
  Timer0_Enable();
  /////////////////////////////////////////////////////////////////////////////
  // Put your additional application init code here!                         //
  // This is called once during start-up.                                    //
  /////////////////////////////////////////////////////////////////////////////
}

/**************************************************************************//**
 * Application Process Action.
 *****************************************************************************/
SL_WEAK void app_process_action(void)
{
  /////////////////////////////////////////////////////////////////////////////
  // Put your additional application code here!                              //
  // This is called infinitely.                                              //
  // Do not call blocking functions from here!                               //
  ///////////////////////////////////////////////////////////////////////////////
//  GPIO_PinOutSet(gpioPortB, TRIGGER_PIN);
//  delayMs(5000, &Timer0_OF);
//  GPIO_PinOutClear(gpioPortB, TRIGGER_PIN);
//  delayMs(5000, &Timer0_OF);
  app_log("start\n");
  GPIO_PinOutSet(gpioPortB, TRIGGER_PIN);
  delayMs(200, &Timer0_OF);
  GPIO_PinOutClear(gpioPortB, TRIGGER_PIN);
  app_log("trigger done!\n");
  while (!GPIO_PinInGet(gpioPortB, ECHO_PIN)){
      //app_log("",count);
      if (Timer0_OF == true) {
                      count++;
                      Timer0_OF = false;
      }
  }
  count = 0;
  while (GPIO_PinInGet(gpioPortB, ECHO_PIN)) {
              if (Timer0_OF == true) {
                  count++;
                  Timer0_OF = false;
              }
              app_log("");
  }
  app_log("Echo_Pin is down\n");
  distance = count * 343 / 1000; // F= 10^5 hz -> count*34300*10^5 (cm)
  //app_log("distance: %d\n", distance);
  count =0;
  echo_time_out = false;
  app_log("distance: %d\n", distance);
  send_data_distance(advertising_set_handle, gattdb_data_distance, distance);
}

/**************************************************************************//**
 * Bluetooth stack event handler.
 * This overrides the dummy weak implementation.
 *
 * @param[in] evt Event coming from the Bluetooth stack.
 *****************************************************************************/
void sl_bt_on_event(sl_bt_msg_t *evt)
{
  sl_status_t sc;

  switch (SL_BT_MSG_ID(evt->header)) {
    // -------------------------------
    // This event indicates the device has started and the radio is ready.
    // Do not call any stack command before receiving this boot event!
    case sl_bt_evt_system_boot_id:
      // Create an advertising set.
      sc = sl_bt_advertiser_create_set(&advertising_set_handle);
      app_assert_status(sc);

      // Generate data for advertising
      sc = sl_bt_legacy_advertiser_generate_data(advertising_set_handle,
                                                 sl_bt_advertiser_general_discoverable);
      app_assert_status(sc);

      // Set advertising interval to 100ms.
      sc = sl_bt_advertiser_set_timing(
        advertising_set_handle,
        160, // min. adv. interval (milliseconds * 1.6)
        160, // max. adv. interval (milliseconds * 1.6)
        0,   // adv. duration
        0);  // max. num. adv. events
      app_assert_status(sc);
      // Start advertising and enable connections.
      sc = sl_bt_legacy_advertiser_start(advertising_set_handle,
                                         sl_bt_legacy_advertiser_connectable);
      app_assert_status(sc);
      if (sc == SL_STATUS_OK) {
//sc = send_data_distance(distance);
          //send_data_distance(advertising_set_handle, gattdb_data_distance, distance);
              app_log_status_error(sc);
      }
      break;

    // -------------------------------
    // This event indicates that a new connection was opened.
    case sl_bt_evt_connection_opened_id:
     // send_data_distance(advertising_set_handle, gattdb_data_distance, distance);
      break;

    // -------------------------------
    // This event indicates that a connection was closed.
    case sl_bt_evt_connection_closed_id:
      // Generate data for advertising
      sc = sl_bt_legacy_advertiser_generate_data(advertising_set_handle,
                                                 sl_bt_advertiser_general_discoverable);
      app_assert_status(sc);

      // Restart advertising after client has disconnected.
      sc = sl_bt_legacy_advertiser_start(advertising_set_handle,
                                         sl_bt_legacy_advertiser_connectable);
      app_assert_status(sc);
      break;

    ///////////////////////////////////////////////////////////////////////////
    // Add additional event handlers here as your application requires!      //
    ///////////////////////////////////////////////////////////////////////////

    case sl_bt_evt_gatt_server_characteristic_status_id:
          if (gattdb_data_distance == evt->data.evt_gatt_server_characteristic_status.characteristic) {
            // A local Client Characteristic Configuration descriptor was changed in
            // the gattdb_report_button characteristic.
            if (evt->data.evt_gatt_server_characteristic_status.client_config_flags
                & sl_bt_gatt_notification) {
              // The client just enabled the notification. Send notification of the
              // current button state stored in the local GATT table.
              app_log_info("Notification enabled.");

              //sc = send_data_distance(distance);
              app_log_status_error(sc);
            } else {
              app_log_info("Notification disabled.\n");
            }
          }
          break;



    // -------------------------------
    // Default event handler.
    default:
      break;
  }
}
static sl_status_t send_data_distance(uint8_t connection,
                                              uint16_t characteristic,
                                              uint32_t distance) {
    sl_status_t sc;
    char data_send[4];  // Mảng để lưu chuỗi 4 ký tự số + ký tự kết thúc chuỗi '\0'

    // Chuyển đổi distance thành chuỗi ASCII 4 chữ số
    snprintf(data_send, sizeof(data_send), "%04u", distance*10);

    // Gửi dữ liệu vào đặc tính
    sc = sl_bt_gatt_server_write_attribute_value( characteristic, 0,
                                              sizeof(data_send),  // Bao gồm ký tự kết thúc chuỗi '\0'
                                               (const uint8_t*)data_send);

    if (sc != SL_STATUS_OK) {
        // Xử lý lỗi nếu có
        app_log("Write failed with status: 0x%04x\n", sc);
    } else {
        // Ghi thành công
        app_log("Write succeeded: %s\n", data_send);
    }

    return sc;
}

