resource "google_storage_bucket" "function_bucket" {
  name     = "${var.project_id}-function-source"
  location = var.region
  uniform_bucket_level_access = true
}

data "archive_file" "function_source" {
  type        = "zip"
  source_dir  = "../src"
  output_path = "/tmp/function-source.zip"
}

resource "google_storage_bucket_object" "function_source" {
  name   = "function-source-${data.archive_file.function_source.output_md5}.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = data.archive_file.function_source.output_path
}

resource "google_cloudfunctions2_function" "function" {
  name        = var.function_name
  location    = var.region
  description = "Stops Cloud SQL instances daily"

  build_config {
    runtime     = "python310"
    entry_point = "stop_cloud_sql_instances"
    source {
      storage_source {
        bucket = google_storage_bucket.function_bucket.name
        object = google_storage_bucket_object.function_source.name
      }
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "256M"
    timeout_seconds    = 60
    service_account_email = google_service_account.function_sa.email
  }
}

output "function_uri" {
  value = google_cloudfunctions2_function.function.service_config[0].uri
}
