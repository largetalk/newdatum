=====================
使用lua开发的blog
=====================

curl http://localhost:8080/users/

curl -i -X POST -d '{"username":"abc","email":"abc@123.com","password":"123","address":"china"}' http://localhost:8080/users/

curl -i http://localhost:8080/users/?username=abc&password=123
