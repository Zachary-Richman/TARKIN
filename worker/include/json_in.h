//
// Created by zjric on 11/1/2026.
//

#ifndef JSON_IN_H
#define JSON_IN_H

#include "types.h"
#include "cJSON.h"

Job *parse_job(const cJSON *json);

void free_job(Job *Job);

#endif //JSON_IN_H
