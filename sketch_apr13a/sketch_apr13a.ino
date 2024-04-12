#include <avr/io.h>
#include <avr/eeprom.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>

#define F_CPU		16000000UL
#define UART_BAUDRATE	2400
#define UBRR_VAL	(((F_CPU / (UART_BAUDRATE * 16UL))) - 1)
#define MAX_EEPROM_SIZE	1024
#define EXPECTED_BYTES	1011
#define BUFFER_SIZE	256 /* Should be smaller than available RAM */

volatile uint16_t total_bytes = 0;
volatile uint8_t rx_complete = 0, tx_complete = 0;

/* Temporary buffer to store the EEPROM data */
uint8_t tx_buffer[BUFFER_SIZE];
uint8_t buffer_head = 0;
uint8_t buffer_tail = 0;

void uart_init() {
	/* Baud rate */
	UBRR0 = UBRR_VAL;

	/* Configure the data frame: 8-data bits, no parity, 1 stop bit. Enable the RX interrupt. */
	UCSR0C = (3 << UCSZ00);
	UCSR0B = (1 << RXEN0) | (1 << TXEN0) | (1 << RXCIE0);

	sei();  /* Enable global interrupts */
}

/* Disable the RX interrupt */
void disable_rx_isr()
{
	uint8_t val = UCSR0B;

	val &= ~(1 << RXCIE0);
	UCSR0B = val;
}

/* Enable the UDRE interrupt */
void enable_udre_isr()
{
	UCSR0B |= 1 << UDRIE0;
}

/* Disable the UDRE interrupt */
void disable_udre_isr()
{
	uint8_t val = UCSR0B;

	val &= ~(1 << UDRIE0);
	UCSR0B = val;
}

/* Fire an ISR on a byte receival from the host */
ISR(USART_RX_vect) {
	static uint16_t eeprom_addr = 0;
	uint8_t rx_byte = UDR0;

	eeprom_write_byte((uint8_t*)eeprom_addr++, rx_byte);

	total_bytes++;
	if (total_bytes == EXPECTED_BYTES || total_bytes == MAX_EEPROM_SIZE) {
		disable_rx_isr();

		total_bytes = 0;
		rx_complete = 1;
	}
}

/* Fire an ISR after UDR becomes empty */
ISR(USART_UDRE_vect) {
	if (buffer_head != buffer_tail) {
		UDR0 = tx_buffer[buffer_tail];
		buffer_tail = (buffer_tail + 1) % BUFFER_SIZE;
	} else {
		disable_udre_isr();
		tx_complete = 1;
	}
}

void prepare_buffer(void)
{
	static uint16_t eeprom_addr = 0;
	uint16_t max_addr = (EXPECTED_BYTES < MAX_EEPROM_SIZE) ? EXPECTED_BYTES : MAX_EEPROM_SIZE;
	uint8_t was_empty = (buffer_head == buffer_tail);  /* Check if the buffer was empty before adding new data */

	while ((buffer_head + 1) % BUFFER_SIZE != buffer_tail && eeprom_addr < max_addr) {
		tx_buffer[buffer_head] = eeprom_read_byte((uint8_t*)eeprom_addr++);
		buffer_head = (buffer_head + 1) % BUFFER_SIZE;
	}

	if (was_empty && buffer_head != buffer_tail && !(UCSR0B & (1 << UDRIE0)))
		enable_udre_isr();
}

int main(void) {
	uint16_t eeprom_addr = 0;
	uint8_t byte;

	uart_init();

	/*
	 * Ensure all data has been received.
	 * To ensure power savings, sleep mode can also be exploited. Its not used for now.
	 */
        while (!rx_complete) {}

	prepare_buffer();
	if (buffer_head != buffer_tail)
		enable_udre_isr();

	/*
	 * Ensure all data has been transmitted.
	 * To ensure power savings, sleep mode can also be exploited. Its not used for now.
	 */
	while (!tx_complete)
		prepare_buffer();

	return 0;
}
