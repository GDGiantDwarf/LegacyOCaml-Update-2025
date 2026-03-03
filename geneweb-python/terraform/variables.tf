variable "render_api_key" {
  description = "Render API key (from https://dashboard.render.com/account/api-keys)"
  type        = string
  sensitive   = true
}

variable "render_owner_id" {
  description = "Render owner/team ID (visible in the Render dashboard URL)"
  type        = string
}

variable "service_name" {
  description = "Name of the Render web service"
  type        = string
  default     = "geneweb-gwd"
}

variable "region" {
  description = "Render region: oregon, frankfurt, ohio, singapore, virginia"
  type        = string
  default     = "frankfurt"
}

variable "repo_url" {
  description = "GitHub repository URL for the project"
  type        = string
}
