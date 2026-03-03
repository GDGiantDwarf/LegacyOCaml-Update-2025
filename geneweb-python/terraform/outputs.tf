output "service_url" {
  description = "Public URL of the deployed service"
  value       = render_web_service.gwd.url
}

output "service_id" {
  description = "Render service ID"
  value       = render_web_service.gwd.id
}
