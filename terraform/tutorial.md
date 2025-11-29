# Cloud SQL 自動停止ツールのデプロイ

このチュートリアルでは、Cloud SQL インスタンスを毎日自動的に停止するツールをデプロイします。

## プロジェクトの設定

まず、デプロイ先の Google Cloud プロジェクトを設定します。

<walkthrough-project-setup></walkthrough-project-setup>

## プロジェクトの確認

まず、リソースを作成する対象プロジェクトが正しいかを確認します。  
**本番環境や、本番用 Cloud SQL インスタンスが含まれるプロジェクトには絶対にデプロイしないでください。これ以降の手順を実施すると、プロジェクト内のすべてのDBが停止される処理が設定されます。**

デプロイするプロジェクトが以下のプロジェクトで正しいかを改めて確認してください。

```bash
<walkthrough-project-id/>
```

誤っている場合はこの画面の「前へ」で前の画面に戻り、プロジェクトを選択し直してください。

## Terraform の初期化

Terraform を初期化し、必要なプラグインをダウンロードします。

```bash
terraform init
```

## デプロイの実行

Terraform を使用してリソースをデプロイします。

```bash
terraform apply -var="project_id=<walkthrough-project-id/>"
```

確認プロンプトが表示されたら、`yes` と入力して Enter キーを押してください。

## 完了

以上でセットアップが完了しました！

このプロジェクト内のデータベースは22時になると自動で停止するようになります。  
Cloud Scheduler のジョブ `stop-cloudsql-daily` が作成されていることを確認してください。

もし停止したくないデータベースがある場合は、対象のデータベースに `auto_stop: false` のラベルを設定してください。