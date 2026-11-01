#include <stdio.h>
#include "rebound.h"
#include "stability.h"
#define STABILITY_CHECK_INTERVAL 100

void simulation_debug(struct reb_simulation *sim) {
	reb_simulation_synchronize(sim);

	printf("===== REBOUND SIMULATION =====\n");
	printf("Particles: %p\n", sim->N);
	printf("Time:      %.12e\n", sim->t);
	printf("G:         %.12e\n", sim->G);
	printf("Timestep:  %.12e\n", sim->dt);

	printf("\n===== PARTICLES =====\n");

	for (uint32_t i = 0; i < sim->N; i++) {
		struct reb_particle p = sim->particles[i];

		printf("\nParticle %u\n", i);
		printf("Mass: %.12e\n", p.m);
		printf("Position: (%.12e, %.12e, %.12e)\n",
			   p.x, p.y, p.z);
		printf("Velocity: (%.12e, %.12e, %.12e)\n",
			   p.vx, p.vy, p.vz);
	}

	printf("==============================\n");
}

void stability_debug(const StabilityDetection *detection) {

	const char *type_name;

	switch (detection->type) {
		case STABLE:
			type_name = "STABLE";
		break;
		case CLOSE_ENCOUNTER_INNER:
			type_name = "CLOSE_ENCOUNTER_INNER";
		break;
		case CLOSE_ENCOUNTER_OUTER:
			type_name = "CLOSE_ENCOUNTER_OUTER";
		break;
		case HIGH_ECCENTRICITY:
			type_name = "HIGH_ECCENTRICITY";
		break;
		case EJECTION:
			type_name = "EJECTION";
		break;
		default:
			type_name = "UNKNOWN";
		break;
	}

	fprintf(stderr, "\n===== STABILITY DETECTION =====\n");
	fprintf(stderr, "Type:      %s\n", type_name);
	fprintf(stderr, "Time:      %.12e seconds\n", detection->time);
	fprintf(stderr, "Body:      %d\n", detection->body_index);
	fprintf(stderr, "Value:     %.12e\n", detection->value);
	fprintf(stderr, "Threshold: %.12e\n", detection->threshold);
	fprintf(stderr, "================================\n");
}

StabilityDetection simulation(struct reb_simulation *sim, Job *job) {
	const double duration = job->configuration.integrator.duration;
	double *rmh = mutual_hill_radius(job);
	const JobCondition job_condition = job->metadata.condition;
	const uint32_t init_planet_count = 1 + job->planet_count + (job->metadata.condition == CONDITION_PERTURBED);


	while(sim->t < duration) { // SKIP: logic for overflow of duration (e.g., % 100 != 0)
		reb_simulation_steps(sim, STABILITY_CHECK_INTERVAL);

		StabilityDetection check = stability_detection(sim, job_condition, rmh, init_planet_count);
		if(check.type != STABLE) {
			stability_free(rmh);
			return check;
		}
	}
	stability_free(rmh);


	return (StabilityDetection) {
		.type = STABLE,
		.time = sim->t,
		.body_index = -1,
		.value = -1,
		.threshold = -1
	};
};
