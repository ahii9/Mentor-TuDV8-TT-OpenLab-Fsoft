/*******************************************************************************
 * Timer0.h
 *
 *  Created on: 17 July 2024
 *      Author: Bach
 *      Email: nguyenbachhp2003@gmail.com
 *******************************************************************************/
/**************************************************************
 * Includes
 **************************************************************/
#include "Timer0.h"
/**************************************************************
 * Defines
 **************************************************************/
#define TIMER0_FREQUENCY  100000  //HZ
/**************************************************************
 * Macros
 **************************************************************/

/**************************************************************
 * Typedefs
 **************************************************************/
bool Timer0_OF = false;
/**************************************************************
 * Globals
 **************************************************************/

/**************************************************************
 * Externs
 **************************************************************/

/**************************************************************
 * Function
 **************************************************************/
void Timer0_Init(void)
{

  TIMER_Init_TypeDef timerInit = TIMER_INIT_DEFAULT;
  //Disable timer after init
  timerInit.enable = false;

  //enable clock timer0
  CMU_ClockEnable(cmuClock_TIMER0, true);

  //init the timer
  TIMER_Init(TIMER0, &timerInit);

  //Time top value
  uint32_t timerfreq    = CMU_ClockFreqGet(cmuClock_TIMER0) / (timerInit.prescale + 1);
  uint32_t timerTopval  = timerfreq / TIMER0_FREQUENCY;
  TIMER_TopSet(TIMER0, timerTopval);

  //Interrupt
  TIMER_IntEnable(TIMER0, TIMER_IEN_OF);
  NVIC_EnableIRQ(TIMER0_IRQn);

}
/*******************************************************************************
 * Function
 * Name:Timer Enable
 * Decrible:
 */
void Timer0_Enable(void) {
  uint32_t flags = TIMER_IntGet(TIMER0);
  TIMER_IntClear(TIMER0, flags);
  TIMER_Enable(TIMER0, true);
}
/*******************************************************************************
 * Function
 * Name:Timer Enable
 * Decrible:
 */
void Timer0_Disable(void) {
  uint32_t flags = TIMER_IntGet(TIMER0);
  TIMER_IntClear(TIMER0, flags);
  TIMER_Enable(TIMER0, false);
}
/*******************************************************************************
 * Timer_IRQHandler
 */
void TIMER0_IRQHandler(void) {
  uint32_t flags = TIMER_IntGet(TIMER0);
  TIMER_IntClear(TIMER0, flags);
  Timer0_OF = true;
}
