# Cloud SQL Auto-Stop

Cloud SQL インスタンスを毎日指定した時間（デフォルト 22:00 JST）に自動停止するツールです。
コスト削減のために、開発環境などの停止忘れを防ぎます。

## 特徴
- **自動停止**: 指定した時間に `RUNNING` 状態のインスタンスを停止します。
- **除外設定**: `auto_stop: false` ラベルが付与されたインスタンスは停止しません。
- **簡単デプロイ**: Terraform を使用して簡単にデプロイできます。

## Cloud Shell でデプロイ

### 1. プロジェクトの選択

以下のリンクから、対象とするプロジェクトを選択します。
**!!!本番環境へのデプロイは非推奨です。開発環境など、DBを止めたいプロジェクトにのみ適用してください!!!**

[Project Selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=ja)

### 2. Cloud Shell での実行

以下のボタンをクリックすると、Google Cloud Shell が開き、このリポジトリがクローンされます。

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.png)](https://ssh.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/Gre212/cloud-sql-stopper&cloudshell_tutorial=tutorial.md&cloudshell_workspace=terraform)

### 3. チュートリアルに沿って実行

表示されるチュートリアルに沿ってコマンドを実行します。

```bash
# 現在のプロジェクトを確認
echo "Current Project: $GOOGLE_CLOUD_PROJECT"

# Terraformを初期化
terraform init

# Cloud Shellの環境変数を使用してデプロイ
terraform apply -var="project_id=$GOOGLE_CLOUD_PROJECT"
```

#### 補足: プロジェクトの指定方法

Cloud ShellではプロジェクトIDが環境変数として自動的に設定されているため、その変数を利用してプロジェクトを指定します。
もし意図しないプロジェクトが設定されていた場合は、修正してください。

```bash
# 現在のプロジェクトを確認
echo "Current Project: $GOOGLE_CLOUD_PROJECT"

# もし違うプロジェクトが設定されている場合は変更
# gcloud config set project YOUR-PROJECT-ID
```

#### 補足: スクリプトの直接実行

デプロイせずにスクリプトを直接実行してテストする場合

```bash
# Cloud Shellで直接実行（プロジェクトIDは自動取得）
python src/main.py

# プロジェクトが正しく設定されているか確認
gcloud config get-value project
# または
echo $GOOGLE_CLOUD_PROJECT
```

## 手動デプロイ手順（ローカル環境）

ローカル環境からデプロイする場合は、

1. `terraform` ディレクトリに移動する
2. `terraform init` を実行
3. `terraform apply -var="project_id=YOUR_PROJECT_ID"` を実行
