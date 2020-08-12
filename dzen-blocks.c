#include <stdio.h>
#include <stdlib.h>

#define DELIMETER ':'

int
main(int argc, char *argv[]) {
	/* help dialog */
	if (argv[1] == "h" || argc != 2) {
		printf("Usage: dzen-blocks [config]\n");
		return -1;
	}

	char *path = argv[1];

	/* file spec is just key[DELIMITER]value
	 * ini is nice, but kind of overkill
	 * for this
	 */
	FILE    *conf;
	char    *line = NULL;
	int     line_count = 0;
	size_t  line_buf_size = 0;
	ssize_t line_size;

	conf = fopen(path, "r");
	if (conf == NULL) {
		printf("File doesn't exist.\n");
		return -1;
	}

	line_size = getline(&line, &line_buf_size, conf);

	while (line_size >= 0) {
		line_count++;

		/* find the delimiter */
		int i = 0;
		int idx = -1;
		while (line[i] != '\0') {
			i++;
			if (line[i - 1] == DELIMETER) {
				idx = i - 1;
				break;
			}
		}

		if (idx != -1) {
			/* assign key, value using delimiter */
			char *key   = (char*)
			              malloc(sizeof(char) *
			              idx - 1);
			char *value = (char*)
			              malloc(sizeof(char) *
			              line_size - (idx - 1));

			int i = 0;
			for (i = 0; i < idx; i++)
				key[i] = line[i];
			key[i] = '\0';
			for (int i = idx; i < line_size; i++)
				value[i] = line[i];
			value[i] = '\0';

			printf("%s\n", key  );
			printf("%s\n", value);
			free(key);
			free(value);
		}

		line_size = getline(&line, &line_buf_size, conf);
	}

	fclose(conf);
	return 0;
}
