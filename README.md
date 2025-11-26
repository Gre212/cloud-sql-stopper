# Cloud SQL Auto-Stop

Cloud SQL インスタンスを毎日指定した時間（デフォルト 22:00 JST）に自動停止するツールです。
コスト削減のために、開発環境などの停止忘れを防ぎます。

## 特徴
- **自動停止**: 指定した時間に `RUNNING` 状態のインスタンスを停止します。
- **除外設定**: `auto_stop: false` ラベルが付与されたインスタンスは停止しません。
- **簡単デプロイ**: Terraform を使用して簡単にデプロイできます。

## Cloud Shell でデプロイ

以下のボタンをクリックすると、Google Cloud Shell が開き、このリポジトリがクローンされ、デプロイのチュートリアルが開始されます。

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.png)](https://ssh.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/Gre212/cloud-sql-stopper&cloudshell_tutorial=tutorial.md)

**注意**: `YOUR_GITHUB_REPO_URL` をこのリポジトリの実際の URL に置き換えてください。

## 手動デプロイ手順

1. `terraform` ディレクトリに移動します。
2. `terraform init` を実行します。
3. `terraform apply -var="project_id=YOUR_PROJECT_ID"` を実行します。
