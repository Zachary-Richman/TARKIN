#include <stdio.h>
#include <stdlib.h>
#include "rebound.h"
#include "types.h"
#include "simulation.h"

#include "dynamic_fgets.h"
#include "json_in.h"
#include "creator.h"

int main(void) {
	char *line = dynamic_fgets(stdin);
	Job *parsed_line = parse_job(line);
	struct reb_simulation *sim = create_simulation(parsed_line);
	simulation_debug(sim);
	const StabilityDetection resp = simulation(sim, parsed_line);

	stability_debug(&resp);

	free(line);

	return 0;
}
