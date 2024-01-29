terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  # "Project" -> "Cloud Overview" -> "Dashboard" -> "Project ID"
  project = var.project

  # List of GCP codes: https://cloud.google.com/about/locations
  region = var.region

  # How to store key file:
  # 1. use Secret Manager/ Key Vault
  # 2. save as a variable in `variables.tf`
  # 3. save the path in this file: `credentials = "./keys/my-creds.json"`
  # 4. save the path in this ENV variable `GOOGLE_CREDENTIALS`
  #  `export GOOGLE_CREDENTIALS='/workspaces/DataEngineerZoomCamp2024/keys/my-creds.json'`
  credentials = file(var.credentials)
}

resource "google_storage_bucket" "demo-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo-dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}