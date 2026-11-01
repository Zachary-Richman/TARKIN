#ifndef STABILITY_H
#define STABILITY_H

#include <stdint.h>
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

static OrbitalBody *get_body(Job *job, const uint32_t index);


static double distance(const struct reb_particle *p1, const struct reb_particle *p2);

inline double *mutual_hill_radius(Job *bodies);


inline StabilityDetection stability_detection(struct reb_simulation *sim, const JobCondition job_condition,
											  const double *mutual_hill_radii, const uint32_t original_planet_count);


inline void stability_free(double *mutual_hill_radii)




#endif //STABILITY_H