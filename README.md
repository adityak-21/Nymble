# Data Transmission Firmware

## Completed this assignment

## Problem Statement

You have to write firmware to transmit a given piece of text from:

1. Your PC to MCU via UART, then from
2. Your MCU to PC via UART

You have to measure the speed of this data transmission.

Please find the following text:


Sure, here's the updated README.md file with the added line:

markdown
Copy code
# Data Transmission Firmware

## Completed this assignment

## Problem Statement

You have to write firmware to transmit a given piece of text from:

1. Your PC to MCU via UART, then from
2. Your MCU to PC via UART

You have to measure the speed of this data transmission.

Please find the following text:

“Finance Minister Arun Jaitley Tuesday hit out at former RBI governor Raghuram Rajan for predicting that the next banking crisis would be triggered by MSME lending, saying postmortem is easier than taking action when it was required. Rajan, who had as the chief economist at IMF warned of impending financial crisis of 2008, in a note to a parliamentary committee warned against ambitious credit targets and loan waivers, saying that they could be the sources of next banking crisis. Government should focus on sources of the next crisis, not just the last one.

In particular, government should refrain from setting ambitious credit targets or waiving loans. Credit targets are sometimes achieved by abandoning appropriate due diligence, creating the environment for future NPAs," Rajan said in the note." Both MUDRA loans as well as the Kisan Credit Card, while popular, have to be examined more closely for potential credit risk. Rajan, who was RBI governor for three years till September 2016, is currently.”


### Details

1. The above text consists of close to 1000 characters (including spaces) which can be represented as 1000 bytes.
2. This data needs to be sent from your PC to an MCU by UART (2400 baud rate).
3. Upon receiving this data, the MCU stores it in the EEPROM memory as and when it is receiving data. Not all at once.
4. After the entire text data set has been transferred from the PC to the MCU, the MCU starts retrieving the stored data from EEPROM and sends it to the PC.
5. On the PC side, your code needs to print the data being received on the console screen of PC.
6. **During any transmission of data to and from the PC, the console needs to print the live real-time data transmission speed in bits/second.** Do not source it from the baud rate. That is an incorrect approach. See the actual number of bits traveling on the UART bus per second.

## Instructions

- You can use any MCU of your choice.
  - Easiest to use is Arduino which is readily available.
- MCU Code needs to be strictly written in Embedded C/C++. Not in Arduino etc. language.
- You can choose any language for the PC side code.

