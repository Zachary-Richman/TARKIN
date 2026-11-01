// in the sake of cross compatability, getline() will not be used
// inspired by: https://codereview.stackexchange.com/questions/202490/dynamic-fgets-in-c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *dynamic_fgets(FILE *stream) {
	size_t capacity = 128; // Start with a modest chunk size
	size_t length = 0;
	char *buffer = malloc(capacity);

	if (!buffer) return NULL;

	// Use a temporary buffer chunk smaller than or equal to remaining capacity
	char chunk[128];

	while (fgets(chunk, sizeof(chunk), stream)) {
		size_t chunk_len = strlen(chunk);

		// Check if we need to resize the main buffer
		if (length + chunk_len + 1 > capacity) {
			capacity *= 2; // Double the capacity
			char *new_buffer = realloc(buffer, capacity);
			if (!new_buffer) {
				free(buffer);
				return NULL; // Memory allocation failed
			}
			buffer = new_buffer;
		}

		// Copy chunk content into our dynamic buffer
		strcpy(buffer + length, chunk);
		length += chunk_len;

		// If we found a newline, the entire line has been read
		if (buffer[length - 1] == '\n') {
			break;
		}
	}

	// Handle case where EOF is hit immediately with no data read
	if (length == 0) {
		free(buffer);
		return NULL;
	}

	return buffer;
}