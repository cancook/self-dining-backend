# self-dining-backend

## feat
1. Django Model 생성 완료
2. AWS EC2, RDS 생성 완료
3. YouTube Data 백종원, 자취요리신 데이터 RDS 저장 완료
4. Pandas to_csv 로 csv 파일 생성 완료
5. 가비아 도메인 구매 완료 self-dining.shop
6. sshtunnel <br> settings.py
   ```
   from sshtunnel import SSHTunnelForwarder
   # # SSH
   # ! AWS EC2 에서는 주석처리
   server = SSHTunnelForwarder(
      (os.getenv('AWS_EC2_IP'), 22),
      ssh_username=os.getenv('AWS_EC2_USERNAME'),
      ssh_pkey='~/.ssh/8th-team2.pem',
      remote_bind_address=(
         os.getenv('POSTGRES_HOST'), 5432
      )
   )
   server.stop()
   server.start()

   DATABASES = {
      'default': {
         'ENGINE': 'django.db.backends.postgresql',
         # ! 로컬 환경에서는 아래와 같이 설정
         'HOST': '127.0.0.1',
         # ! AWS EC2 에서는 아래와 같이 설정
         # 'HOST': os.getenv('POSTGRES_HOST'),
         'NAME': os.getenv('POSTGRES_NAME'),
         'USER': os.getenv('POSTGRES_USER'),
         'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
         # ! 로컬 환경에서는 아래와 같이 설정
         'PORT': server.local_bind_port,
         # ! AWS EC2 에서는 아래와 같이 설정
         # 'PORT': 5432,
      }
   }
   ```
   youtube.py
   ```
   with SSHTunnelForwarder(
        (os.getenv('AWS_EC2_IP'), 22),
        ssh_username=os.getenv('AWS_EC2_USERNAME'),
        ssh_pkey='~/.ssh/8th-team2.pem',
        remote_bind_address=(
            os.getenv('POSTGRES_HOST'), 5432
        )
    ) as tunnel:
        if tunnel.is_active:
            print("AWS EC2 SSH 터널이 성공적으로 연결되었습니다.")
        else:
            print("AWS EC2 SSH 터널 연결에 실패하였습니다.")

        postgres_password = os.getenv('POSTGRES_PASSWORD')
        postgres_port = tunnel.local_bind_port # * 외부에서는 5432, 내부에서는 랜덤으로 할당되는 포트번호
   ```
7. I realized gunicorn <br>
      1. poetry add gunicorn
   1. I am using Python Poetry so I am not using requirements.txt<br>
     ㄴ poetry export -f requirements.txt > requirements.txt<br>
     ㄴ sudo apt install python3-virtualenv<br>
     ㄴ virtualenv venv<br>
     ㄴ pip install -r requirements.txt
   2. sudo vi /etc/systemd/system/gunicorn.service
   ```
   [Unit]
   Description=gunicorn daemon
   After=network.target

   [Service]
   User=ubuntu
   Group=ubuntu
   WorkingDirectory=/home/ubuntu/code/self-dining-backend
   EnvironmentFile=/home/ubuntu/code/self-dining-backend/.env
   ExecStart=/home/ubuntu/.local/bin/gunicorn \
         --workers 1 \
         --bind unix:/tmp/gunicorn.sock \
         config.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```
   4. sudo systemctl daemon-reload
   5. sudo systemctl status gunicorn-service
8. letsencrypt
   1. sudo add-apt-repository ppa:certbot/certbot
   2. sudo apt install python3-certbot-nginx
   3. sudo vi /etc/nginx/sites-available/self-dining # 도메인 추가
   4. sudo service nginx reload and status
   5. sudo ufw status # 방화벽 비활성화 확인
   6. sudo certbot --nginx -d self-dining.shop
   
## TODO
1. AWS EC2
   1. 내부에서 Docker 사용
   2. Nginx 설정 Frontend, Backend
   3. SSL 인증서 발급 HTTPS 적용
2. YouTube Data 백종원, 자취요리신 데이터 리펙터링
3. Django config/settings/ local.py, dev.py 설정파일 생성
