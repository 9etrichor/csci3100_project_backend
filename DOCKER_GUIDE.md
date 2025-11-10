# Django Backend Docker Setup Guide / Django 後端 Docker 設置指南

## English Version

### Overview
A production-ready Django REST API backend with PostgreSQL database, JWT authentication, and complete Docker containerization. This setup provides a robust foundation for web applications with user management and secure API endpoints.

### Tech Stack
- **Framework**: Django 5.2.7 with Django REST Framework
- **Database**: PostgreSQL with custom user model
- **Authentication**: JWT (JSON Web Tokens)
- **Containerization**: Docker & Docker Compose
- **Package Management**: pip (universal compatibility)

### Features
- User registration and authentication
- JWT-based token authentication system
- Custom user model with score field
- RESTful API endpoints
- Docker containerization for easy deployment
- Production-ready settings with security considerations

### Quick Start

#### Prerequisites
- Docker & Docker Compose
- Git

#### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/9etrichor/csci3100_project_backend.git
   cd csci3100_project_backend
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings (defaults work for development)
   ```

3. **Run database migrations**:
   ```bash
   docker-compose --profile migrate up migrate
   ```

4. **Start the application**:
   ```bash
   docker-compose up web
   ```

The API will be available at `http://localhost:8000`.

### API Endpoints

#### Authentication
- `POST /api/auth/register/` - User registration
  ```json
  {
    "username": "testuser",
    "password": "testpass123"
  }
  ```
- `POST /api/auth/login/` - User login (returns JWT tokens)
- `POST /api/auth/token/refresh/` - Refresh JWT access token

#### Users
- `GET /api/users/` - List all users (authenticated)
- `GET /api/users/{id}/` - User details (authenticated)

### Docker Commands

- **Start all services**: `docker-compose up`
- **Run migrations**: `docker-compose --profile migrate up migrate`
- **Stop services**: `docker-compose down`
- **View logs**: `docker-compose logs web`
- **Rebuild**: `docker-compose up --build`
- **Clean restart**: `docker-compose down --volumes && docker-compose --profile migrate up migrate`

### Troubleshooting

#### Common Issues

**"uv: executable file not found"**
- **Cause**: Old Docker images with outdated commands
- **Solution**: Clean Docker cache and rebuild
  ```bash
  docker system prune -a --volumes
  docker-compose build --no-cache
  ```

**"password authentication failed for user django_user"**
- **Cause**: Stale database credentials in persistent volume
- **Solution**: Reset database volume
  ```bash
  docker-compose down --volumes
  docker-compose --profile migrate up migrate
  ```

**"SECRET_KEY not found"**
- **Cause**: Environment variables not loaded during build
- **Solution**: Ensure `.env` file exists with proper values

**Port 8000 already in use**
- **Solution**: Change port in `docker-compose.yml` or stop conflicting service

#### Development Tips
- Use `docker-compose up -d web` for detached mode
- Check container logs with `docker-compose logs -f web`
- Access container shell with `docker-compose exec web bash`
- Database is accessible at `localhost:5432` (if exposed)

### Project Structure
```
csci3100_project_backend/
├── backend_project/          # Django project settings
│   ├── settings.py          # Main configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI application
├── users/                    # Custom user app
│   ├── models.py            # User model with score field
│   ├── views.py             # API views
│   ├── serializers.py       # DRF serializers
│   └── urls.py              # App URL patterns
├── Dockerfile                # Container build instructions
├── docker-compose.yml        # Service orchestration
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── .dockerignore            # Docker build exclusions
└── README.md                # This documentation
```

### Environment Variables

Create a `.env` file with:
```env
# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DB_NAME=backend_db
DB_USER=django_user
DB_PASSWORD=secure_password
DB_HOST=db
DB_PORT=5432

# PostgreSQL settings (for Docker)
POSTGRES_DB=backend_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=secure_password
```

### Security Considerations
- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use strong passwords for database
- Configure proper `ALLOWED_HOSTS`
- Consider using environment-specific settings files

---

## 中文版本

### 概述
一個生產就緒的 Django REST API 後端，包含 PostgreSQL 資料庫、JWT 認證，以及完整的 Docker 容器化。此設置為 Web 應用程式提供了穩固的基礎，包含用戶管理和安全的 API 端點。

### 技術棧
- **框架**: Django 5.2.7 搭配 Django REST Framework
- **資料庫**: PostgreSQL 搭配自定義用戶模型
- **認證**: JWT (JSON Web Tokens)
- **容器化**: Docker & Docker Compose
- **套件管理**: pip (通用相容性)

### 功能特色
- 用戶註冊和認證
- 基於 JWT 的令牌認證系統
- 自定義用戶模型（包含分數欄位）
- RESTful API 端點
- Docker 容器化以便於部署
- 生產就緒的設置包含安全性考量

### 快速開始

#### 必要條件
- Docker & Docker Compose
- Git

#### 安裝步驟

1. **複製倉庫**：
   ```bash
   git clone https://github.com/9etrichor/csci3100_project_backend.git
   cd csci3100_project_backend
   ```

2. **設置環境變數**：
   ```bash
   cp .env.example .env
   # 編輯 .env 文件設定您的偏好（預設值適用於開發環境）
   ```

3. **執行資料庫遷移**：
   ```bash
   docker-compose --profile migrate up migrate
   ```

4. **啟動應用程式**：
   ```bash
   docker-compose up web
   ```

API 將在 `http://localhost:8000` 上運行。

### API 端點

#### 認證
- `POST /api/auth/register/` - 用戶註冊
  ```json
  {
    "username": "testuser",
    "password": "testpass123"
  }
  ```
- `POST /api/auth/login/` - 用戶登入（返回 JWT 令牌）
- `POST /api/auth/token/refresh/` - 刷新 JWT 訪問令牌

#### 用戶
- `GET /api/users/` - 列出所有用戶（需要認證）
- `GET /api/users/{id}/` - 用戶詳情（需要認證）

### Docker 命令

- **啟動所有服務**: `docker-compose up`
- **執行遷移**: `docker-compose --profile migrate up migrate`
- **停止服務**: `docker-compose down`
- **查看日誌**: `docker-compose logs web`
- **重建**: `docker-compose up --build`
- **清理重啟**: `docker-compose down --volumes && docker-compose --profile migrate up migrate`

### 故障排除

#### 常見問題

**"uv: executable file not found"**
- **原因**: 舊的 Docker 映像包含過時的命令
- **解決方案**: 清理 Docker 快取並重建
  ```bash
  docker system prune -a --volumes
  docker-compose build --no-cache
  ```

**"password authentication failed for user django_user"**
- **原因**: 持久化卷中的過時資料庫憑證
- **解決方案**: 重置資料庫卷
  ```bash
  docker-compose down --volumes
  docker-compose --profile migrate up migrate
  ```

**"SECRET_KEY not found"**
- **原因**: 建置期間未載入環境變數
- **解決方案**: 確保 `.env` 文件存在且包含正確值

**端口 8000 已被使用**
- **解決方案**: 在 `docker-compose.yml` 中更改端口或停止衝突服務

#### 開發提示
- 使用 `docker-compose up -d web` 以分離模式運行
- 使用 `docker-compose logs -f web` 查看容器日誌
- 使用 `docker-compose exec web bash` 訪問容器 shell
- 資料庫可在 `localhost:5432` 訪問（如果已暴露）

### 專案結構
```
csci3100_project_backend/
├── backend_project/          # Django 專案設定
│   ├── settings.py          # 主要配置
│   ├── urls.py              # URL 路由
│   └── wsgi.py              # WSGI 應用程式
├── users/                    # 自定義用戶應用
│   ├── models.py            # 包含分數欄位的用戶模型
│   ├── views.py             # API 視圖
│   ├── serializers.py       # DRF 序列化器
│   └── urls.py              # 應用 URL 模式
├── Dockerfile                # 容器建置指令
├── docker-compose.yml        # 服務協調
├── requirements.txt          # Python 依賴
├── .env.example             # 環境模板
├── .dockerignore            # Docker 建置排除
└── README.md                # 本文檔
```

### 環境變數

創建 `.env` 文件包含：
```env
# Django 設定
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 資料庫設定
DB_NAME=backend_db
DB_USER=django_user
DB_PASSWORD=secure_password
DB_HOST=db
DB_PORT=5432

# PostgreSQL 設定 (Docker 用)
POSTGRES_DB=backend_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=secure_password
```

### 安全性考量
- 在生產環境中更改 `SECRET_KEY`
- 在生產環境中設定 `DEBUG=False`
- 為資料庫使用強密碼
- 配置適當的 `ALLOWED_HOSTS`
- 考慮使用環境特定的設定文件

---

## 聯絡與支援 / Contact & Support

**English**: For issues or questions, please check the troubleshooting section or create an issue in the repository.

**中文**: 如有問題或疑問，請查看故障排除部分或在倉庫中創建問題。

**Repository**: https://github.com/9etrichor/csci3100_project_backend

**Branch**: `dockerize` (contains the complete Docker setup)
