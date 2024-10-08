/*******************************************************************************
 * Timer0.h
 *
 *  Created on: 17 July 2024
 *      Author: Bach
 *      Email: nguyenbachhp2003@gmail.com
 *******************************************************************************/

#ifndef TIMER0_H_
#define TIMER0_H_

/**************************************************************
 * Includes
 **************************************************************/
#include "app.h"

/**************************************************************
 * Defines
 **************************************************************/

/**************************************************************
 * Macros
 **************************************************************/

/**************************************************************
 * Typedefs
 **************************************************************/

/**************************************************************
 * Globals
 **************************************************************/

/**************************************************************
 * Externs
 **************************************************************/

/**************************************************************
 * Function
 **************************************************************/
void Timer0_Init(void);
void Timer0_Enable(void);
void Timer0_Disable(void);
void TIMER0_IRQHandler(void);
#endif /* TIMER0_H_ */
