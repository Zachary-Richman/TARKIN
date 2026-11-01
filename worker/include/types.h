#ifndef TYPES_H
#define TYPES_H

#include <stdint.h>

typedef struct {
  double mass;
  double a;
  double e;
  double inc;
  double Omega;
  double omega;
  double M;
} OrbitalBody;

typedef enum {
  CONDITION_CONTROL,
  CONDITION_PERTURBED
} JobCondition; // control system or perturbed system

typedef struct{
  double mass; // kg
  double radius; // m
} Star;

typedef struct{
  char *integrator;
  double duration; // s
  double timestep; // s
} IntegratorConfig;

typedef struct {
  uint32_t schema_version;
  uint64_t job_id;
  uint64_t system_id;
  JobCondition condition;
} JobMetadata;

typedef struct{
  Star star;
  IntegratorConfig integrator;
} JobConfiguration;

typedef struct{
  JobMetadata metadata;
  JobConfiguration configuration;
  OrbitalBody *planets;
  OrbitalBody perturber;
  uint32_t planet_count; // for later
} Job;


#endif //TYPES_H
