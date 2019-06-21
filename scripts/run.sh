#!/bin/sh

WORKFLOW_PROPERTIES_FILE=oozie/workflow/workflow_production.properties;

oozie job -D DOTSITE_USER=jbalaji.site  -config $WORKFLOW_PROPERTIES_FILE -run
