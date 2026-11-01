#include "creator.h"
#include <math.h>

#include "types.h"
#include "rebound.h"

static double mean_to_true_anomaly(const double M, const double e) {
	double E = M;
	double delta;

	// Newton-Raphson iteration
	do {
		delta = (E - e * sin(E) - M) / (1 - e * cos(E));
		E -= delta;
	} while (fabs(delta) > 1e-12);

	return 2 * atan2(
		sqrt(1 + e) * sin(E / 2),
		sqrt(1 - e) * cos(E / 2)
	);
}


inline struct reb_simulation *create_simulation(const Job *job) { // job is converted into the type from json_in.h (not yet made)
	struct reb_simulation *sim = reb_simulation_create();
	if (sim == NULL) return NULL;
	reb_simulation_set_integrator(sim, job->configuration.integrator.integrator);
	sim->dt = job->configuration.integrator.timestep;
	sim->G = 6.67430e-11; // so we rockin with the SI units

	struct reb_particle star = {0};
	star.m = job->configuration.star.mass;
	star.r = job->configuration.star.radius;
	reb_simulation_add(sim, star);


	for(uint32_t i = 0; i < job->planet_count; i++) {
		struct reb_particle particle = reb_particle_from_orbit(
			sim->G,
			star,
			job->planets[i].mass, // mass
			job->planets[i].a, // semi-major axis
			job->planets[i].e, // eccentricity
			job->planets[i].inc, // inclination,
			job->planets[i].Omega, // Omega
			job->planets[i].omega, // omega
			mean_to_true_anomaly(job->planets[i].M, job->planets[i].e)
		);

		reb_simulation_add(sim, particle);
	}

	if (job->metadata.condition == CONDITION_PERTURBED) {
		struct reb_particle particle = reb_particle_from_orbit(
		sim->G,
		star,
		job->perturber.mass, // mass
		job->perturber.a, // semi-major axis
		job->perturber.e, // eccentricity
		job->perturber.inc, // inclination,
		job->perturber.Omega, // Omega
		job->perturber.omega, // omega
		mean_to_true_anomaly(job->perturber.M, job->perturber.e)
	);

		reb_simulation_add(sim, particle);
	}

	return sim;
}
