resource "digitalocean_droplet" "my_droplet" {
  image  = "ubuntu-20-04-x64"
  name   = "example-ubuntu-droplet"
  region = "fra1"
  size   = "s-1vcpu-1gb"
  backups = false
  monitoring = true
  ssh_keys = ["8d:fb:69:bb:b3:9f:18:69:45:c5:0d:81:14:23:95:63"]
}
