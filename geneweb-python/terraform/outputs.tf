output "service_url" {
  description = "Public URL of the deployed gwd service"
  value       = render_web_service.gwd.url
}

output "service_id" {
  description = "Render gwd service ID"
  value       = render_web_service.gwd.id
}

output "admin_service_url" {
  description = "Public URL of the deployed gwsetup service"
  value       = render_web_service.gwsetup.url
}

output "admin_service_id" {
  description = "Render gwsetup service ID"
  value       = render_web_service.gwsetup.id
}
