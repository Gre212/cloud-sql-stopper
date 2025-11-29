# Cloud SQL Auto-Stop

Cloud SQL インスタンスを毎日指定した時間（デフォルト 22:00 JST）に自動停止するツールです。
コスト削減のために、開発環境などの停止忘れを防ぎます。

## 特徴
- **自動停止**: 指定した時間に `RUNNING` 状態のインスタンスを停止します。
- **除外設定**: `auto_stop: false` ラベルが付与されたインスタンスは停止しません。
- **簡単デプロイ**: Terraform を使用して簡単にデプロイできます。

## Cloud Shell でデプロイ

### 1. プロジェクトの選択

Cloud Shellを開く前に、使用するプロジェクトを明示的に選択してください：

1. [GCPコンソール](https://console.cloud.google.com/)にアクセス
2. 画面上部のプロジェクトセレクター（通常「プロジェクト名」または「プロジェクトを選択」と表示）をクリック
3. **「プロジェクトを選択」ダイアログ**が開くので、以下を確認：
   - Cloud SQLインスタンスが存在するプロジェクトを選択
   - 複数のプロジェクトがある場合は、検索ボックスで絞り込み可能
4. 選択後、画面上部にプロジェクト名とプロジェクトIDが表示されることを確認
   - 例: `My Project (my-project-123456)`

### 2. Cloud Shell での実行

以下のボタンをクリックすると、Google Cloud Shell が開き、このリポジトリがクローンされます。

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.png)](https://ssh.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/Gre212/cloud-sql-stopper&cloudshell_tutorial=tutorial.md)

### 3. デプロイ実行

Cloud Shellでは、プロジェクトIDが環境変数として自動的に設定されています：

```bash
# 現在のプロジェクトを確認
echo "Current Project: $GOOGLE_CLOUD_PROJECT"

# もし違うプロジェクトが設定されている場合は変更
# gcloud config set project YOUR-PROJECT-ID

# terraform ディレクトリに移動
cd terraform

# Terraformを初期化
terraform init

# Cloud Shellの環境変数を使用してデプロイ
terraform apply -var="project_id=$GOOGLE_CLOUD_PROJECT"
```

#### 補足: スクリプトの直接実行

デプロイせずにスクリプトを直接実行してテストする場合：

```bash
# Cloud Shellで直接実行（プロジェクトIDは自動取得）
python src/main.py

# プロジェクトが正しく設定されているか確認
gcloud config get-value project
# または
echo $GOOGLE_CLOUD_PROJECT
```

**注意**: `src/main.py` は `google.auth.default()` を使用しているため、Cloud Shell環境では自動的に `GOOGLE_CLOUD_PROJECT` 環境変数からプロジェクトIDを取得します。

## 手動デプロイ手順（ローカル環境）

ローカル環境からデプロイする場合：

1. `terraform` ディレクトリに移動します。
2. `terraform init` を実行します。
3. `terraform apply -var="project_id=YOUR_PROJECT_ID"` を実行します。
