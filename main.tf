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
  project     = "dez2024"
  region      = "us-central1"
    # How to store key file:
    # 1. use Secret Manager/ Key Vault
    # 2. save the path in this file: `credentials = "./keys/my-creds.json"`
    # 3. save the path in this ENV variable `GOOGLE_CREDENTIALS`
    #  `export GOOGLE_CREDENTIALS='/workspaces/DataEngineerZoomCamp2024/keys/my-creds.json'`
  credentials = "./keys/my-creds.json"
}
