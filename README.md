# FastAPI + Next.js フルスタックアプリケーション

認証機能、CRUD操作、クリーンアーキテクチャを備えたFastAPI（バックエンド）とNext.js（フロントエンド）で構築されたモダンなフルスタックWebアプリケーションです。

## 🚀 機能

### バックエンド (FastAPI)

- **FastAPI** v0.115.12 with async support
- **PostgreSQL** 17 database with **SQLModel** ORM
- **Alembic** for database migrations
- **JWT** authentication with role-based access control (RBAC)
- **UUID** primary keys for all tables
- **Enum** types for status and role management
- **Docker** containerization with Docker Compose
- **Factory Boy** and **Faker** for data seeding
- 包括的なAPIバリデーションとエラーハンドリング

### フロントエンド (Next.js)

- **Next.js** 15.3.2 with App Router
- **TypeScript** for type safety
- **Tailwind CSS** v4 for styling
- **shadcn/ui** component library
- **Axios** for API communication with interceptors
- **React Context API** for authentication state management
- 保護されたルートとロールベースUI
- レスポンシブデザイン

## 📋 前提条件

- Docker and Docker Compose
- Node.js 20+ and npm (フロントエンドのローカル開発用)
- Make (オプション、Makefileコマンド使用時)
- Git

## 🛠️ インストール & セットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd fastapi
```

### 2. 環境変数の設定

```bash
cp backend/.env.example backend/.env
```

`.env`ファイルを設定で更新してください：

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/fastapi_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Makeを使ったクイックスタート（推奨）

```bash
make fresh
```

このコマンドは以下を実行します：

- Dockerコンテナのビルド
- 全サービスの開始
- データベースマイグレーションの実行
- ダミーデータでのデータベースシード

### 代替方法：手動セットアップ

```bash
cd backend
docker-compose up -d --build
docker-compose exec backend alembic upgrade head
docker-compose exec backend python scripts/seed_db.py
```

## 🔗 アプリケーションへのアクセス

- **フロントエンド**: <http://localhost:3000>
- **バックエンドAPI**: <http://localhost:8000>
- **APIドキュメント**: <http://localhost:8000/docs>
- **代替APIドキュメント**: <http://localhost:8000/redoc>

## 🔐 デフォルト認証情報

- **管理者ユーザー**: <admin@example.com> / admin123
- **一般ユーザー**: シードスクリプトで作成、パスワード: password123

## 📁 プロジェクト構造

```
fastapi/
├── backend/
│   ├── app/
│   │   ├── api/           # APIエンドポイント
│   │   ├── core/          # コア機能（設定、セキュリティ）
│   │   ├── db/            # データベース設定
│   │   ├── models/        # SQLModelモデル
│   │   └── utils/         # ユーティリティ関数とファクトリ
│   ├── alembic/           # データベースマイグレーション
│   ├── scripts/           # ユーティリティスクリプト
│   ├── tests/             # テストファイル
│   ├── docker-compose.yml
│   ├── Dockerfile.dev
│   └── requirements.txt
└── frontend/
    ├── app/               # Next.js app directory
    │   ├── (auth)/       # 認証ページ
    │   ├── (dashboard)/  # 保護されたダッシュボードページ
    │   └── api/          # APIルート
    ├── components/        # Reactコンポーネント
    ├── contexts/          # Reactコンテキスト
    ├── services/          # APIサービス層
    ├── types/             # TypeScript型定義
    ├── hooks/             # カスタムReactフック
    ├── lib/               # ユーティリティライブラリ
    └── public/            # 静的アセット
```

## 🧑‍💻 開発

### 一般的なコマンド（Makeを使用）

```bash
make up          # 全サービスの開始
make down        # 全サービスの停止
make logs        # ログの表示
make migrate     # データベースマイグレーションの実行
make seed        # ダミーデータでのデータベースシード
make test        # テストの実行
make format      # コードのフォーマット
make lint        # コードのリント
make fresh       # クリーンスタート（全てを再ビルド）
```

### シェルアクセス

```bash
make shell-backend   # バックエンドコンテナへのアクセス
make shell-frontend  # フロントエンドコンテナへのアクセス
make shell-db       # PostgreSQLシェルへのアクセス
```

### バックエンド開発

```bash
# コードのフォーマット
make format

# コードのリント
make lint

# テストの実行
make test

# カバレッジ付きテストの実行
make test-cov
```

### フロントエンド開発

```bash
cd frontend

# 依存関係のインストール
npm install

# 開発サーバーの実行
npm run dev

# 本番用ビルド
npm run build

# リントの実行
npm run lint
```

## 🗄️ データベーススキーマ

### Usersテーブル

- `id` (UUID): プライマリキー
- `email` (String): 一意のメールアドレス
- `full_name` (String): ユーザーのフルネーム
- `role` (Enum): ユーザーロール（admin/user/guest）
- `is_active` (Boolean): アカウントステータス
- `hashed_password` (String): 暗号化パスワード
- `created_at` (DateTime): アカウント作成タイムスタンプ
- `updated_at` (DateTime): 最終更新タイムスタンプ

### Itemsテーブル

- `id` (UUID): プライマリキー
- `title` (String): アイテムタイトル
- `description` (String): アイテム説明
- `price` (Float): アイテム価格
- `quantity` (Integer): 利用可能数量
- `category` (Enum): アイテムカテゴリ（electronics/clothing/books/food/other）
- `status` (Enum): アイテムステータス（draft/published/archived）
- `is_available` (Boolean): 利用可能ステータス
- `owner_id` (UUID): Usersテーブルへの外部キー
- `created_at` (DateTime): 作成タイムスタンプ
- `updated_at` (DateTime): 最終更新タイムスタンプ

## 🚦 APIエンドポイント

### 認証

- `POST /api/v1/auth/login` - ユーザーログイン
- `POST /api/v1/auth/logout` - ユーザーログアウト
- `POST /api/v1/auth/change-password` - パスワード変更

### ユーザー

- `GET /api/v1/users/` - ユーザー一覧（管理者のみ）
- `GET /api/v1/users/me` - 現在のユーザー取得
- `GET /api/v1/users/{id}` - IDによるユーザー取得
- `POST /api/v1/users/` - ユーザー作成
- `PATCH /api/v1/users/{id}` - ユーザー更新
- `DELETE /api/v1/users/{id}` - ユーザー削除（管理者のみ）

### アイテム

- `GET /api/v1/items/` - 全アイテムの一覧（フィルター付き）
- `GET /api/v1/items/my` - ユーザーのアイテム一覧
- `GET /api/v1/items/{id}` - IDによるアイテム取得
- `POST /api/v1/items/` - アイテム作成
- `PATCH /api/v1/items/{id}` - アイテム更新
- `DELETE /api/v1/items/{id}` - アイテム削除
- `POST /api/v1/items/{id}/publish` - アイテム公開

## 🐛 トラブルシューティング

### よくある問題

1. **ポートが既に使用中**

   ```bash
   make down
   make up
   ```

2. **データベース接続エラー**
   - PostgreSQLコンテナが実行中か確認: `docker-compose ps`
   - .envファイルのDATABASE_URLを確認
   - コンテナログを確認: `docker-compose logs db`

3. **マイグレーションエラー**

   ```bash
   make clean
   make fresh
   ```

4. **フロントエンドビルドエラー**

   ```bash
   cd frontend
   rm -rf node_modules .next
   npm install
   npm run dev
   ```

## 🧪 テスト

### バックエンドテスト

```bash
make test                              # 全テストの実行
make test-cov                         # カバレッジレポート付きテスト
docker-compose exec backend pytest -v  # 詳細出力
```

### フロントエンドテスト

```bash
cd frontend
npm test
```

## 📝 ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。

## 🤝 コントリビューション

1. リポジトリをフォーク
2. フィーチャーブランチを作成（`git checkout -b feature/amazing-feature`）
3. 変更をコミット（`git commit -m 'Add some amazing feature'`）
4. テストとリントを実行
5. ブランチにプッシュ（`git push origin feature/amazing-feature`）
6. プルリクエストを開く

## 📧 サポート

質問やサポートについては、GitHubでissueを開いてください。
