resource "google_cloud_scheduler_job" "job" {
  name             = var.scheduler_job_name
  description      = "Trigger Cloud Function to stop Cloud SQL instances"
  schedule         = "0 22 * * *"
  time_zone        = "Asia/Tokyo"
  attempt_deadline = "320s"

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions2_function.function.service_config[0].uri
    
    oidc_token {
      service_account_email = google_service_account.scheduler_sa.email
    }
  }
}
