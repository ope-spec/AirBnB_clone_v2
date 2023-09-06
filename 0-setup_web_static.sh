#!/usr/bin/env bash
# This script sets up a web server for the deployment of web_static.

# Install Nginx if it's not already installed
if ! sudo command -v nginx &> /dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary folders if they don't exist
web_static_dir="/data/web_static"
web_static_current="${web_static_dir}/current"
web_static_test="${web_static_dir}/releases/test"

sudo mkdir -p "$web_static_dir" "$web_static_test"
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee "${web_static_test}/index.html" > /dev/null

# Create or recreate symbolic link
if [ -L "$web_static_current" ]; then
    sudo rm -f "$web_static_current"
fi
sudo ln -s "$web_static_test" "$web_static_current"

# Give ownership to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu "$web_static_dir"

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
config_contents=$(cat <<EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \$hostname;
    root   /var/www/html;
    index  index.html index.htm;

	location /hbnb_static {
        alias $web_static_current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }

    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}
EOF
)

echo "$config_contents" | sudo tee "$config_file" > /dev/null

# Restart Nginx
sudo service nginx restart
