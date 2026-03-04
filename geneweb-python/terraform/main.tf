terraform {
  required_providers {
    render = {
      source  = "render-oss/render"
      version = "~> 1.4"
    }
  }
  required_version = ">= 1.5"
}

provider "render" {
  api_key  = var.render_api_key
  owner_id = var.render_owner_id
}

resource "render_web_service" "gwd" {
  name          = var.service_name
  plan          = "free"
  region        = var.region
  start_command = "cd geneweb-python && uvicorn geneweb.web.server.server:create_app --host 0.0.0.0 --port $PORT --factory"

  runtime_source = {
    native_runtime = {
      auto_deploy_trigger = "commit"
      branch              = "main"
      build_command       = "pip install -r geneweb-python/requirements.txt"
      repo_url            = var.repo_url
      runtime             = "python"
    }
  }

  env_vars = {
    "PYTHONPATH" = { value = "geneweb-python" }
  }
}

resource "render_web_service" "gwsetup" {
  name          = var.admin_service_name
  plan          = "free"
  region        = var.region
  start_command = "cd geneweb-python && uvicorn geneweb.web.admin.server:create_app --host 0.0.0.0 --port $PORT --factory"

  runtime_source = {
    native_runtime = {
      auto_deploy_trigger = "commit"
      branch              = "main"
      build_command       = "pip install -r geneweb-python/requirements.txt"
      repo_url            = var.repo_url
      runtime             = "python"
    }
  }

  env_vars = {
    "PYTHONPATH" = { value = "geneweb-python" }
  }
}
