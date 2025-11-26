variable "project_id" {
  description = "The ID of the Google Cloud project"
  type        = string
}

variable "region" {
  description = "The region to deploy resources to"
  type        = string
  default     = "asia-northeast1"
}

variable "function_name" {
  description = "The name of the Cloud Function"
  type        = string
  default     = "stop-cloudsql-instances"
}

variable "scheduler_job_name" {
  description = "The name of the Cloud Scheduler job"
  type        = string
  default     = "stop-cloudsql-daily"
}
