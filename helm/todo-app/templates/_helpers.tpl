{{/*
Expand the name of the chart.
*/}}
{{- define "todo-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "todo-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s" $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "todo-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-app.labels" -}}
helm.sh/chart: {{ include "todo-app.chart" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels for frontend
*/}}
{{- define "todo-app.frontend.selectorLabels" -}}
app.kubernetes.io/name: todo-frontend
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Selector labels for backend
*/}}
{{- define "todo-app.backend.selectorLabels" -}}
app.kubernetes.io/name: todo-backend
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Selector labels for postgres
*/}}
{{- define "todo-app.postgres.selectorLabels" -}}
app.kubernetes.io/name: todo-postgres
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
