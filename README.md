# flask-jdck-upload-docker
```
docker run -dit \
   -p 9001:5000 \
   --name jdckupload \
   --hostname jdckupload \
   --env address="xxx.xxx.xxx.xxx:xxxx"
   --env client_id="xxx"
   --env client_secret="xxx"
   --restart always \
   zjjscwt/jdckupload:latest
```
