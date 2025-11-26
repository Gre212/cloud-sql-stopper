resource "google_service_account" "function_sa" {
  account_id   = "cloudsql-stopper-sa"
  display_name = "Cloud SQL Stopper Service Account"
}

resource "google_project_iam_member" "cloudsql_editor" {
  project = var.project_id
  role    = "roles/cloudsql.editor"
  member  = "serviceAccount:${google_service_account.function_sa.email}"
}

resource "google_cloud_run_service_iam_member" "invoker" {
  project  = var.project_id
  location = var.region
  service  = google_cloudfunctions2_function.function.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.scheduler_sa.email}"
}

resource "google_service_account" "scheduler_sa" {
  account_id   = "cloudsql-scheduler-sa"
  display_name = "Cloud SQL Scheduler Service Account"
}
