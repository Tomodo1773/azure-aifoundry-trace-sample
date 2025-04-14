# Azure AI Foundry Trace Sample

このプロジェクトは、Azure AI Inference SDKおよびLangChainを使用してAI推論を実行し、そのトレース情報をAzure Monitor (Application Insights) に送信する方法を示すサンプルコードを提供します。

## ファイル説明

* **`01_ai_inference_monitor_otel.py`**:
    Azure AI Inference SDK（`azure-ai-inference`）とAzure Monitor OpenTelemetry Exporter（`azure-monitor-opentelemetry`）を直接使用して、チャット補完APIの呼び出しをトレースし、Azure Monitorに送信する基本的なサンプルです。`configure_azure_monitor`を利用して設定を行います。
* **`02_ai_inference_custom_opentelemetry.py`**:
    Azure AI Inference SDKを使用しつつ、OpenTelemetryのTracerProviderやExporterをより明示的に設定するサンプルです。`AIInferenceInstrumentor().instrument()` を呼び出して、SDKの自動計装を有効にし、トレース情報をAzure Monitorおよびコンソールに出力します。
* **`03_langchain_azure_ai_model.py`**:
    LangChainのAzure AI統合 (`langchain-azure-ai`) を使用するサンプルです。`AzureAIChatCompletionsModel` を介してAzure AI Inferenceのエンドポイントを利用し、`AzureAIInferenceTracer` コールバックを使用してLangChainの実行トレースをAzure Monitorに送信します。

## 前提事項

* Python3.8以降
* Azureサブスクリプション
* Azure AI Studioプロジェクト
* Azure AI Inferenceエンドポイント（例: `DeepSeek-V3`モデルがデプロイされている）
* Application Insightsリソース（Azure AI Studioプロジェクトに関連付けられているもの）

## セットアップ手順

1. **リポジトリのクローン:**

    ```bash
    git clone <repository-url>
    cd azure-aifoundry-trace-sample
    ```

2. **依存関係のインストール:**

uv` を利用して仮想環境を作成し、依存関係のインストールを行います。

```bash
uv sync
```

3. **環境変数の設定:**

`.env.sample` ファイルをコピーして `.env` ファイルを作成します。

```bash
cp .env.sample .env
```

`.env` ファイルを開き、以下の環境変数を設定します。

* `PROJECT_CONNECTION_STRING`: Azure AI Studioプロジェクトの接続文字列。
* `AZURE_INFERENCE_ENDPOINT`: Azure AI InferenceエンドポイントのURL。
* `AZURE_INFERENCE_CREDENTIAL`: Azure AI InferenceエンドポイントのAPIキー。

4.  **サンプルの実行:**

各Pythonスクリプトを実行します。

```bash
python 01_ai_inference_monitor_otel.py
python 02_ai_inference_custom_opentelemetry.py
python 03_langchain_azure_ai_model.py
```
