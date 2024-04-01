resource "digitalocean_droplet" "my_droplet" {
  image  = "ubuntu-20-04-x64"
  name   = "buscainstrumentos-scraper"
  region = "fra1"
  size   = "s-1vcpu-1gb"
  backups = false
  monitoring = true
  ssh_keys = ["4b:f6:47:9b:a3:cc:6a:0a:5b:9f:8d:47:4e:8c:44:5f"]
}
