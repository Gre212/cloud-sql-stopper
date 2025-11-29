# Cloud SQL 自動停止ツールのデプロイ

このチュートリアルでは、Cloud SQL インスタンスを毎日自動的に停止するツールをデプロイします。

## プロジェクトの設定

まず、デプロイ先の Google Cloud プロジェクトを設定します。

<walkthrough-project-setup></walkthrough-project-setup>

## ディレクトリの移動

Terraform の設定ファイルがあるディレクトリに移動します。

```bash
cd terraform
```

## Terraform の初期化

Terraform を初期化し、必要なプラグインをダウンロードします。

```bash
terraform init
```

## デプロイの実行

Terraform を使用してリソースをデプロイします。
`YOUR_PROJECT_ID` は自動的に現在のプロジェクト ID に置き換えられます。

```bash
terraform apply -var="project_id=<walkthrough-project-id/>"
```

確認プロンプトが表示されたら、`yes` と入力して Enter キーを押してください。

## 完了

以上でセットアップが完了しました。このプロジェクト内のデータベースは22時になると自動で停止するようになります。
Cloud Scheduler のジョブ `stop-cloudsql-daily` が作成されていることを確認してください。

もし停止したくないデータベースがある場合は、対象のデータベースに `auto_stop: false` のラベルを設定してください。