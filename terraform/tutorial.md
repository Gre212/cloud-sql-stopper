# Cloud SQL 自動停止ツールのデプロイ

このチュートリアルでは、Cloud SQL インスタンスを毎日自動的に停止するツールをデプロイします。

## プロジェクトの設定

まず、デプロイ先の Google Cloud プロジェクトを設定します。

<walkthrough-project-setup></walkthrough-project-setup>

## プロジェクトの確認

まず、リソースを作成する対象プロジェクトが正しいかを確認します。  
**本番環境など、データベースを止めてはいけない環境には決してデプロイしないでください。**

```bash
echo "Current Project: $GOOGLE_CLOUD_PROJECT"
```

もしプロジェクトが未指定であったり、異なるプロジェクトの場合は以下のコマンドから正しいプロジェクトを設定します。

```bash
gcloud config set project <walkthrough-project-id/>
```

## Terraform の初期化

Terraform を初期化し、必要なプラグインをダウンロードします。

```bash
terraform init
```

## デプロイの実行

Terraform を使用してリソースをデプロイします。

```bash
terraform apply -var="project_id=$GOOGLE_CLOUD_PROJECT"
```

確認プロンプトが表示されたら、`yes` と入力して Enter キーを押してください。

## 完了

以上でセットアップが完了しました！

このプロジェクト内のデータベースは22時になると自動で停止するようになります。  
Cloud Scheduler のジョブ `stop-cloudsql-daily` が作成されていることを確認してください。

もし停止したくないデータベースがある場合は、対象のデータベースに `auto_stop: false` のラベルを設定してください。