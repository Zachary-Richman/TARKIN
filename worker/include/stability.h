#ifndef STABILITY_H
#define STABILITY_H
#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

#include "types.h"
#include "rebound.h"


/*
Detection Hierarchy (priority order):
1. Inner-Planet Close Encounters:
2. Outer-Planet Close Encounters:
3. High Eccentricity: e_i > 0.9
 */

// to begin, some definitions :)
typedef enum {
 STABLE,
 CLOSE_ENCOUNTER_INNER,
 CLOSE_ENCOUNTER_OUTER,
 HIGH_ECCENTRICITY,
 EJECTION
} StabilityEventType;

typedef struct {
 StabilityEventType type;
 double time;
 int body_index;
 double value;
 double threshold;
} StabilityDetection;

static OrbitalBody *get_body(Job *job, const uint32_t index) { // helper for adding in the extra perturber if exists
	if (index < job->planet_count) {
		return &job->planets[index];
	}
	return &job->perturber;
}


static double distance(const struct reb_particle *p1, const struct reb_particle *p2) {
	const double d_x = p1->x - p2->x;
	const double d_y = p1->y - p2->y;
	const double d_z = p1->z - p2->z;

	return sqrt(d_x * d_x + d_y * d_y + d_z * d_z);
}

inline double *mutual_hill_radius(Job *bodies) {
	const uint32_t planet_count = bodies->planet_count;
	const bool has_perturber = bodies->metadata.condition == CONDITION_PERTURBED;
	const uint32_t body_count = planet_count + (has_perturber ? 1 : 0);
	const uint32_t pair_count = body_count * (body_count - 1) / 2;
	double *values = malloc(sizeof(*values) * pair_count);
	if (values == NULL) return NULL;
		for (uint32_t i = 0; i < body_count; i++) {
    		for (uint32_t j = i + 1; j < body_count; j++) {
				const double star_m = bodies->configuration.star.mass;

				const OrbitalBody *body_i = get_body(bodies, i);
				const OrbitalBody *body_j = get_body(bodies, j);

				const double body_i_a = body_i->a;
				const double body_j_a = body_j->a;

				const double a_avg = (body_i_a + body_j_a) / 2;
				const double m_sum = body_i->mass + body_j->mass;

				const double R_mH = a_avg * cbrt(m_sum / (3 * star_m));

				const uint32_t index = i * (2 * body_count - i - 1) / 2 + (j - i - 1);
				values[index] = R_mH;
    		}
	  }
	return values;
};


inline StabilityDetection stability_detection(struct reb_simulation *sim, const JobCondition job_condition,
											  const double *mutual_hill_radii, const uint32_t original_planet_count) {
	reb_simulation_synchronize(sim);

	// struct reb_particle *star = &sim->particles[0];
	const uint32_t num_particles =
			(uint32_t) (sim->N - sim->N_var); // REMOVES ADDED PARTICLES FROM MEGNO, if they exist (safety measure)

	// distinguish the inner planets, for classification
	const struct reb_particle *inner_planets = &sim->particles[1];
	uint32_t inner_planet_count = num_particles - 1; // use for iteration
	if (job_condition == CONDITION_PERTURBED)
		inner_planet_count--;

	// check to make sure the particles still exist
	if (original_planet_count != num_particles) {
		return (StabilityDetection){.type = EJECTION,
									.time = sim->t,
									.body_index = -1, // should not be processed
									.value = num_particles,
									.threshold = original_planet_count};
	}

	// Check inners (R_mH)
	for (uint32_t i = 0; i < inner_planet_count; i++) {
		for (uint32_t j = i + 1; j < inner_planet_count; j++) {
			const double d = distance(&inner_planets[i], &inner_planets[j]);
			// fucked up
			const double R_mH = mutual_hill_radii[i * (2 * (inner_planet_count + (job_condition == CONDITION_PERTURBED)) - i - 1) / 2 + (j - i - 1)];

			if (d < R_mH) {
				return (StabilityDetection){.type = CLOSE_ENCOUNTER_INNER,
											.time = sim->t,
											.body_index = (uint32_t) (i + 1),
											.value = d,
											.threshold = R_mH};
			}
		}
	}

	// check outer to outers (R_mH)
	if (job_condition == CONDITION_PERTURBED) {
		for (uint32_t i = 0; i < inner_planet_count; i++) {
			const uint32_t outer_index = num_particles - 1;
			const double d = distance(&inner_planets[i], &sim->particles[outer_index]);

			const double R_mH = mutual_hill_radii[i * (2 * inner_planet_count - i + 1) / 2 + (inner_planet_count - i - 1)];

			if (d < R_mH) {
				return (StabilityDetection){.type = CLOSE_ENCOUNTER_OUTER,
											.time = sim->t,
											.body_index = (uint32_t) (i + 1),
											.value = d,
											.threshold = R_mH};
			}
		}
	}

	// using the eccentricity of 0.9, realistically it would be much lower if unstable,
	// however, once reaching beyond e_max it should compound into e > 0.9
	for (uint32_t i = 0; i < inner_planet_count; i++) {
		// convert to orbit
		const struct reb_orbit o = reb_orbit_from_particle(sim->G, sim->particles[i + 1], sim->particles[0]);
		if (o.e > 0.9)
			return (StabilityDetection){.type = HIGH_ECCENTRICITY,
										.time = sim->t,
										.body_index = (uint32_t) (i + 1),
										.value = o.e,
										.threshold = 0.9
			};
	}

	return (StabilityDetection){
			.type = STABLE, .time = sim->t, .body_index = -1, .value = -1, .threshold = -1};
}


inline void stability_free(double *mutual_hill_radii) {
	free(mutual_hill_radii);
}




#endif //STABILITY_H