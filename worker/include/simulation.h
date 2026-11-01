#ifndef SIMULATION_H
#define SIMULATION_H
#include "rebound.h"
#include "stability.h"

void simulation_debug(struct reb_simulation *sim);

void stability_debug(const StabilityDetection *detection);

StabilityDetection simulation(struct reb_simulation *sim, Job *job);

#endif //SIMULATION_H
