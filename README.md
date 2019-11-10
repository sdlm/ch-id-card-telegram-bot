# ch-id-card-telegram-bot
Telegram bot for extract fields from chinese id cards

For run bot:
```
    docker run 
        -v src:/app/src 
        -e TELEGRAM_CHANNEL_TOKEN='...' 
        -e CHINESE_ID_CARD_API_HOST='localhost:8000' 
        --name ch-id-bot_1
        ch-id-bot
    
    docker rm -f ch-id-bot_1
```

For run test server:
```
    docker run 
        -p 8000:8000 
        --name flask-test-app_1 
        flask_test_app
        
    docker rm -f flask-test-app_1
```
