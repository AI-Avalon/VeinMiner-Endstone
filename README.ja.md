# VeinMiner Plugin for Endstone
[English Documentation](README.md)

Endstoneサーバー向けの設定可能な一括破壊（Vein Miner）プラグインです。

Endstone `v0.11.0` 以上が必要です。

## 特徴

- 鉱石、原木、葉っぱの一括破壊
- 起動モード: スニーク時、直立時、または常に有効
- ブロックカテゴリによるツール検証（ツルハシ/斧/ハサミ/クワ）
- エンチャントに対応したドロップ:
  - シルクタッチ: 鉱石ブロックをそのままドロップ
  - 幸運: 対応する鉱石のアイテムドロップ数増加
  - 耐久力: ツールの耐久力消費を軽減
- オートスメルト（自動製錬）機能（幸運エンチャントの要求やホワイトリストの設定が可能）
- XP（経験値）報酬:
  - 鉱石ごとの基本XP
  - 破壊サイズに応じたボーナス倍率
  - オートスメルト有効時の追加XP
- 自動ピックアップ機能（インベントリ超過時の `drop` または `delete` の処理）
- 悪用防止と制限（1分間および1日あたりの上限設定）
- 破壊パターンの制御（`adjacent`, `cube`, `sphere`, `vertical`, `horizontal`）
- 独立したチェーンマイニング（プレイヤーの向いている方向への3x3x奥行きの一括破壊）
- パーティクルおよびサウンドエフェクト（ブロック単位または完了時のみ）
- プレイヤーの統計情報とマイルストーン（記念）の通知
- GitHubのリリースに対するアップデート確認機能
- **多言語対応** (設定ファイルから `language` を `ja_JP` や `en_US` に切り替え可能)

## インストール

```bash
pip install endstone-vein-miner
```

またはソースコードから:

```bash
git clone https://github.com/EuphoriaDevelopmentOrg/VeinMiner-Endstone.git
cd VeinMiner-Endstone
pip install -e .
```

Endstoneサーバーを起動すると、`endstone` エントリポイントを通じてプラグインが自動的に検出されます。

## コマンド

| コマンド | 説明 | 権限 |
|---|---|---|
| `/veinminer` or `/vm` | ヘルプを表示 | `veinminer.command` |
| `/vm reload` | 設定の再読み込み | `veinminer.reload` |
| `/vm stats` | 自身の採掘統計を表示 | `veinminer.stats` |
| `/vm toggle` | 一括破壊の有効/無効を切り替え | `veinminer.toggle` |
| `/vm on` | 一括破壊を有効化 | `veinminer.toggle` |
| `/vm off` | 一括破壊を無効化 | `veinminer.toggle` |
| `/vm status` | 現在のステータスを表示 | `veinminer.toggle` |
| `/vm chain toggle` | チェーンマイニングの有効/無効を切り替え | `veinminer.chain` |
| `/vm chain on` | チェーンマイニングを有効化 | `veinminer.chain` |
| `/vm chain off` | チェーンマイニングを無効化 | `veinminer.chain` |
| `/vm chain status` | チェーンマイニングのステータスを表示 | `veinminer.chain` |

エイリアス: `/vm`, `/vmine`

注意: プラグイン全体の設定コマンド（現在は `/vm reload`）を実行するには、OP権限またはコンソールからの実行が必要です。

## 権限

- `veinminer.use` (デフォルト: true)
- `veinminer.chain` (デフォルト: true)
- `veinminer.command` (デフォルト: op)
- `veinminer.reload` (デフォルト: op)
- `veinminer.stats` (デフォルト: true)
- `veinminer.toggle` (デフォルト: true)
- `veinminer.*` (デフォルト: op)

## 動作に関する注意事項

- ツール検証はカテゴリに基づきます:
  - 鉱石/アメジスト/古代の残骸 -> ツルハシ
  - 原木/幹 -> 斧
  - 葉 -> ハサミ、クワ、斧
- `activation.require-correct-tool = false` に設定されている場合、ツールチェックはスキップされます。
- `auto-pickup.enabled = false` に設定すると、採掘されたアイテムは破壊されたブロックの場所にドロップされます。
- XPはオーブとしてドロップせず、直接プレイヤーに付与されます。
- 幸運やシルクタッチはプラグインによって計算・適用されます。

## 統計情報

統計情報の保存には2つのバックエンドをサポートしています:
- `storage = "yaml"`: プラグインデータフォルダ内の `stats.yml` に保存します。
- `storage = "mysql"`: MySQLテーブル（`<table-prefix>player_stats`, `<table-prefix>player_milestones`）に保存します。

プレイヤーごとに追跡されるデータ:
- 総一括破壊回数
- 一括破壊で採掘した総ブロック数
- 一括破壊での最大ブロック数
- 最後に採掘した日時
- 達成したマイルストーン

## トラブルシューティング

- 一括破壊が発動しない:
  - `veinminer.use` の権限を確認してください。
  - `[activation]` セクションの起動モード（スニーク等）を確認してください。
  - ワールドが `disabled-worlds` に含まれていないか確認してください。
  - `/vm status` を実行して状態を確認してください。
- アイテムが正しくドロップしない、またはオートスメルトが機能しない:
  - `[auto-smelt]` の設定を確認してください。
  - ツールのエンチャントや `require-fortune` の設定を確認してください。
  - ホワイトリストが設定されている場合、対象ブロックが含まれているか確認してください。
- 統計が更新されない:
  - `[statistics].enabled` を確認してください。

## 開発

```bash
pip install -e .
python -m build
```

ソースファイル:
- `src/endstone_vein_miner/vein_miner_plugin.py`
- `src/endstone_vein_miner/vein_miner_command.py`
- `src/endstone_vein_miner/statistics_tracker.py`

## ライセンス

MIT
