#include "json_in.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "types.h"


Job *parse_job(const char *json) {
	cJSON *parsed_json = cJSON_Parse(json);
	if(parsed_json == NULL) return NULL;

	// pull metadata
	cJSON *job_metadata = cJSON_GetObjectItemCaseSensitive(parsed_json, "metadata");
	if(job_metadata == NULL) return NULL;

	const uint32_t job_condition_raw = cJSON_GetObjectItemCaseSensitive(job_metadata, "condition")->valueint;
	// is 0 or 1, need to convert to the enum later

	JobMetadata metadata = (JobMetadata){
		.schema_version = cJSON_GetObjectItemCaseSensitive(job_metadata, "schema_version")->valueint,
		.job_id = cJSON_GetObjectItemCaseSensitive(job_metadata, "job_id")->valueint,
		.system_id = cJSON_GetObjectItemCaseSensitive(job_metadata, "system_id")->valueint,
		.condition = job_condition_raw == 1 ? CONDITION_PERTURBED : CONDITION_CONTROL
	};

	// pull configuration
	cJSON *config = cJSON_GetObjectItemCaseSensitive(parsed_json, "configuration");
	cJSON *star_config = cJSON_GetObjectItemCaseSensitive(config, "star");
	cJSON *integrator_config = cJSON_GetObjectItemCaseSensitive(config, "integrator");

	Star star = (Star){
		.mass = cJSON_GetObjectItemCaseSensitive(star_config, "mass")->valuedouble,
		.radius = cJSON_GetObjectItemCaseSensitive(star_config, "radius")->valuedouble
	};

	const cJSON *integrator_name = cJSON_GetObjectItemCaseSensitive(integrator_config, "integrator");
	char *integrator_name_copy = malloc(strlen(integrator_name->valuestring) + 1);
	strcpy(integrator_name_copy, integrator_name->valuestring); // strcpy_s would be better but this will ultimately run on a linux box

	IntegratorConfig integrator = (IntegratorConfig){
		.integrator = integrator_name_copy,
		.duration = cJSON_GetObjectItemCaseSensitive(integrator_config, "duration")->valuedouble,
		.timestep = cJSON_GetObjectItemCaseSensitive(integrator_config, "timestep")->valuedouble
	};

	JobConfiguration configuration = (JobConfiguration){
		.star = star,
		.integrator = integrator
	};

	// the planets
	const uint32_t num_planets = cJSON_GetObjectItemCaseSensitive(parsed_json, "planet_count")->valueint;
	OrbitalBody *bodies = malloc(num_planets * sizeof(OrbitalBody));
	const cJSON *planets = cJSON_GetObjectItemCaseSensitive(parsed_json, "planets");

	const cJSON *item = NULL; // iter pointer
	uint32_t planet_index = 0;
	cJSON_ArrayForEach(item, planets) {
		if(planet_index >= num_planets) break;

		OrbitalBody body = (OrbitalBody){};

		body.mass = cJSON_GetObjectItemCaseSensitive(item, "mass")->valuedouble;
		body.a = cJSON_GetObjectItemCaseSensitive(item, "a")->valuedouble;
		body.e = cJSON_GetObjectItemCaseSensitive(item, "e")->valuedouble;
		body.inc = cJSON_GetObjectItemCaseSensitive(item, "inc")->valuedouble;
		body.Omega = cJSON_GetObjectItemCaseSensitive(item, "Omega")->valuedouble;
		body.omega = cJSON_GetObjectItemCaseSensitive(item, "omega")->valuedouble;
		body.M = cJSON_GetObjectItemCaseSensitive(item, "M")->valuedouble;
		bodies[planet_index] = body;
		planet_index++;
	}

	// now perturber
	const cJSON *perturber_data = cJSON_GetObjectItemCaseSensitive(parsed_json, "perturber");
	OrbitalBody perturber = (OrbitalBody){};

	if(cJSON_GetArraySize(perturber_data) != 0) {
		perturber.mass = cJSON_GetObjectItemCaseSensitive(perturber_data, "mass")->valuedouble;
		perturber.a = cJSON_GetObjectItemCaseSensitive(perturber_data, "a")->valuedouble;
		perturber.e = cJSON_GetObjectItemCaseSensitive(perturber_data, "e")->valuedouble;
		perturber.inc = cJSON_GetObjectItemCaseSensitive(perturber_data, "inc")->valuedouble;
		perturber.Omega = cJSON_GetObjectItemCaseSensitive(perturber_data, "Omega")->valuedouble;
		perturber.omega = cJSON_GetObjectItemCaseSensitive(perturber_data, "omega")->valuedouble;
		perturber.M = cJSON_GetObjectItemCaseSensitive(perturber_data, "M")->valuedouble;
	} else {
		perturber.mass = 0.0;
		perturber.a = 0.0;
		perturber.e = 0.0;
		perturber.inc = 0.0;
		perturber.Omega = 0.0;
		perturber.omega = 0.0;
		perturber.M = 0.0;
	}

	Job *job = malloc(sizeof(Job));
	job->metadata = metadata;
	job->configuration = configuration;
	job->planets = bodies;
	job->perturber = perturber;
	job->planet_count = num_planets;

	return job;
}

void free_job(Job *Job) {
	if (Job == NULL) return;

	free(Job->planets);
	free(Job->configuration.integrator.integrator);
	free(Job);
}