# EFS-PDF-Viewer
This is a PDF viewer through which you can just view the pdf and not download it.
* The PDF viewer has screen shot protection for every hot keys in case you hit the space bar and the screen remains black cleck any other key it will go back to normal.
* If you accidently click tab key then just move your mouse in the middle of the screen and click it will go back to normal
## Installation

Install Python3 in your environment
```bash
sudo apt install python3-pip
```
Install Flask
```bash
sudo apt install python3-flask
```
Clone the repository

```bash
git clone <git_url>
```
Install Nginx Server

```bash
sudo apt install nginx
```
Configure Reverse proxy.

```bash

cd /etc/nginx/sites-enabled

server {
    listen 80;
    listen [::]:80;
    server_name <YOUR INSTANCE IP>;
        
    location / {
        proxy_pass http://127.0.0.1:5000;
        include proxy_params;
    }
}
sudo systemctl restart nginx

sudo systemctl status nginx

```

## Usage 
Change the PDF_PATH to the mount point of your EFS and then run the below command.
```bash
python3 app.py
```

