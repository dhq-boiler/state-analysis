# State Analysis

A [Claude Code](https://claude.com/claude-code) skill for generating and viewing state/screen transition diagrams using Mermaid `stateDiagram-v2`.

## What is State Analysis?

State Analysis automatically generates **state transition diagrams** and **screen transition diagrams** from your codebase or natural language descriptions:

- **Screen transition diagrams**: States = screens/pages, transitions = user actions
- **State transition diagrams**: States = object/system states, transitions = events/triggers

It analyzes routing definitions, state management, and navigation calls in your code to produce Mermaid `stateDiagram-v2` diagrams, and provides a browser-based viewer with [Mermaid Live Editor](https://mermaid.live) integration.

## Key Features

- **Codebase analysis**: Auto-extracts states and transitions from routing, state management, and navigation code
- **Natural language input**: Describe your flow in plain text and get a diagram
- **Browser viewer**: Renders diagrams locally with mermaid.js CDN
- **Mermaid Live Editor links**: One-click to edit any diagram in mermaid.live
- **Structured output**: Follows consistent `stateDiagram-v2` rules (direction, naming, labeling, grouping)

## Installation

### Claude Code CLI

```bash
claude skill add --from https://github.com/dhq-boiler/state-analysis
```

### Manual Installation

Copy `SKILL.md` and `scripts/` to `~/.claude/skills/state-analysis/`.

## Usage

Invoke by asking Claude Code to generate a state or screen transition diagram:

```
Generate a state diagram for the authentication flow
```

```
Create a screen transition diagram from this project's routing definitions
```

```
Describe the order lifecycle as a state diagram: pending → confirmed → shipped → delivered, with cancellation possible before shipping
```

### Viewing diagrams

Use `/state-analysis:show` to find and display all previously generated state diagrams in your project:

```
/state-analysis:show
```

The viewer opens in your browser with rendered diagrams, source file references, and links to the Mermaid Live Editor.

### Output formats

The viewer supports multiple output formats:

| Format | Description |
|--------|-------------|
| `html` | (default) Renders diagrams with mermaid.js and opens in browser |
| `md`   | Generates a consolidated Markdown file with all mermaid code blocks |
| `pdf`  | Generates PDF via headless Chromium (Edge/Chrome). Falls back to HTML if no browser found |

You can also use the viewer script directly:

```bash
python scripts/viewer.py --format <html|md|pdf> [--output <path>] <file1.md> <file2.md> ...
```

---

## 日本語ドキュメント

### State Analysis とは？

State Analysis は、コードベースの解析や自然言語の記述から**状態遷移図**・**画面遷移図**を自動生成する Claude Code スキルです。

- **画面遷移図**: 状態 = 画面/ページ、遷移 = ユーザーアクション
- **状態遷移図**: 状態 = オブジェクト/システムの状態、遷移 = イベント/トリガー

ルーティング定義、状態管理、ナビゲーション呼び出しを解析して Mermaid `stateDiagram-v2` 形式の図を生成し、ブラウザビューアと [Mermaid Live Editor](https://mermaid.live) 連携を提供します。

### 主な特徴

- **コードベース解析**: ルーティング・状態管理・ナビゲーションコードから状態と遷移を自動抽出
- **自然言語入力**: フローをテキストで記述するだけで図を生成
- **ブラウザビューア**: mermaid.js CDN を使ってローカルで図をレンダリング
- **Mermaid Live Editor 連携**: ワンクリックで mermaid.live 上で編集可能
- **構造化出力**: 一貫した `stateDiagram-v2` ルール（方向、命名、ラベル、グループ化）に従う

### インストール

#### Claude Code CLI

```bash
claude skill add --from https://github.com/dhq-boiler/state-analysis
```

#### 手動インストール

`SKILL.md` と `scripts/` を `~/.claude/skills/state-analysis/` にコピーしてください。

### 使い方

Claude Code に状態遷移図や画面遷移図の生成を依頼してください：

```
認証フローの状態遷移図を生成して
```

```
このプロジェクトのルーティング定義から画面遷移図を作って
```

```
注文のライフサイクルを状態遷移図にして：保留中 → 確認済み → 発送済み → 配達完了、発送前ならキャンセル可能
```

#### 図の表示

`/state-analysis:show` で、プロジェクト内の既存の状態遷移図をすべて検索・表示できます：

```
/state-analysis:show
```

ブラウザビューアが開き、レンダリングされた図、ソースファイルへの参照、Mermaid Live Editor へのリンクが表示されます。

#### 出力フォーマット

ビューアは複数の出力フォーマットに対応しています：

| フォーマット | 説明 |
|------------|------|
| `html` | （デフォルト）mermaid.js で図をレンダリングしブラウザで表示 |
| `md`   | すべての mermaid コードブロックを統合した Markdown ファイルを生成 |
| `pdf`  | ヘッドレス Chromium（Edge/Chrome）で PDF を生成。ブラウザが見つからない場合は HTML にフォールバック |

ビューアスクリプトを直接使用することもできます：

```bash
python scripts/viewer.py --format <html|md|pdf> [--output <path>] <file1.md> <file2.md> ...
```

## License

MIT
