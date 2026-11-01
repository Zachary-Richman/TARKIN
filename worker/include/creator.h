#ifndef CREATOR_H
#define CREATOR_H

#include <math.h>

#include "types.h"
#include "rebound.h"
static double mean_to_true_anomaly(const double M, const double e);


inline struct reb_simulation *create_simulation(const Job *job) ;

#endif //CREATOR_H
