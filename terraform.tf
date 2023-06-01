terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  token  =  var.token
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  zone      = "ru-central1-a"
}

resource "yandex_vpc_network" "test-network" {
  name = "test-network"
}
 
resource "yandex_vpc_subnet" "my-subnet" {
  name           = "from-terraform-subnet"
  zone           = "ru-central1-a"
  network_id     = "${yandex_vpc_network.test-network.id}"
  v4_cidr_blocks = ["10.10.10.0/24"]
}

resource "yandex_mdb_postgresql_database" "db" {
  cluster_id = "${yandex_mdb_postgresql_cluster.postgresql.id}"
  name       = "db"
  owner      = "${yandex_mdb_postgresql_user.user.name}"
}

resource "yandex_mdb_postgresql_user" "user" {
  cluster_id = "${yandex_mdb_postgresql_cluster.postgresql.id}"
  name       = "user"
  password   = var.postgre_password
}

resource "yandex_mdb_postgresql_cluster" "postgresql" {
  name        = "postgresql"
  environment = "PRODUCTION"
  network_id  = "${yandex_vpc_network.test-network.id}"

  config {
    version = 15
    resources {
      resource_preset_id = "s2.micro"
      disk_type_id       = "network-ssd"
      disk_size          = 16
    }
  }

  host {
    zone      = "ru-central1-a"
    subnet_id = "${yandex_vpc_subnet.my-subnet.id}"
  }
}


resource "yandex_mdb_redis_cluster" "redis" {
  name        = "redis"
  environment = "PRODUCTION"
  network_id  = "${yandex_vpc_network.foo.id}"

  config {
    password = var.redis_password
    version  = "7.0"
  }

  resources {
    resource_preset_id = "b2.nano"
    disk_size          = 4
  }

  host {
    zone      = "ru-central1-a"
    subnet_id = "${yandex_vpc_subnet.my-subnet.id}"
  }
}

resource "yandex_storage_bucket" "frontendapp" {
  bucket = "frontendapp"
  acl    = "public-read"

  website {
    index_document = "index.html"
  }

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST", "DELETE"]
    allowed_origins = ["*"]
  }
}

resource "yandex_storage_object" "index" {
  bucket = "frontendapp"
  source = "/frontend/table/build/index.html"
}

resource "yandex_storage_object" "manifest" {
  bucket = "frontendapp"
  source = "/frontend/table/build/asset-manifest.json"
}

resource "yandex_storage_object" "css" {
  bucket = "frontendapp"
  source = "/frontend/table/build/static/css/*.css"
}

resource "yandex_storage_object" "js" {
  bucket = "frontendapp"
  source = "/frontend/table/build/static/js/*.js"
}

resource "yandex_storage_object" "media" {
  bucket = "frontendapp"
  source = "/frontend/table/build/static/media/*.svg"
}

resource "yandex_container_registry" "backend" {
  name      = "backend"
  folder_id = var.folder_id
}

resource "yandex_container_registry_iam_binding" "puller" {
  registry_id = "${yandex_container_registry.backend.id}"
  role        = "container-registry.images.puller"

  members = [
    "system:allUsers",
  ]
}

resource "yandex_serverless_container" "app" {
  name               = "app"
  memory             = 1024
  execution_timeout  = "10s"
  cores              = 1
  core_fraction      = 100
  image {
    url = "cr.yandex/${yandex_container_registry.backend.id}/backend:latest"
    environment = {
      "REDIS_HOST": "${var.redis_host}",
      "POSTGRESQL_PORT": "${var.postgresql_port}",
      "REDIS_PORT": "${var.redis_port}",
      "POSTGRESQL_PASSWORD": "${var.postgresql_password}",
      "POSTGRESQL_HOST": "${var.postgresql_host}",
      "POSTGRESQL_DATABASE": "${var.postgresql_db}",
      "REDIS_PASSWORD": "${var.redis_db}",
      "POSTGRESQL_USER": "${var.postgresql_user}"
    }
  }
}
