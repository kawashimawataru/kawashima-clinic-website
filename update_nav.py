import os
import re

def update_file(filepath, is_symptoms=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # ヘッダーにお知らせを追加
    # 医院案内の後ろに追加、ただし既にある場合は追加しない
    prefix = "../" if is_symptoms else ""
    
    header_pattern = f'<a href="{prefix}about.html" class="nav-link">医院案内</a>'
    header_replacement = f'<a href="{prefix}about.html" class="nav-link">医院案内</a>\n                <a href="{prefix}news.html" class="nav-link">お知らせ</a>'
    
    if f'href="{prefix}news.html" class="nav-link">お知らせ</a>' not in content:
        content = content.replace(header_pattern, header_replacement)

    # フッターの修正
    # 診療案内ブロックと医院情報ブロックをまとめて置換
    # パターンマッチングが難しいので、特定の文字列範囲を探す
    
    # 診療案内ブロックの開始を探す
    start_marker = '<h4>診療案内</h4>'
    # 医院情報ブロックの終了を探す（医院情報の次のブロックの開始を目印にするか、医院情報の閉じタグを探す）
    # 構造:
    # <div>
    #   <h4>診療案内</h4>
    #   ...
    # </div>
    # <div>
    #   <h4>医院情報</h4>
    #   ...
    # </div>
    
    # 正規表現でブロック全体をキャプチャ
    # 注意: 空白や改行を含む
    
    footer_pattern = re.compile(
        r'<div>\s*<h4>診療案内</h4>.*?</div>\s*<div>\s*<h4>医院情報</h4>.*?</div>\s*</div>',
        re.DOTALL
    )
    
    # マッチしない場合、インデントが違う可能性もあるので柔軟に
    # しかし正規表現が複雑になりすぎる。
    # 単純なreplaceメソッドの連鎖で対応する。
    
    # 1. 診療案内ブロックの削除と開始位置のマーキング
    # ただし単純削除だとdivが残ったり崩れたりする。
    
    # 戦略変更: footer-linksの中身を書き換えるのではなく、ブロックごと書き換える
    
    # まず診療案内ブロックを探す
    if '<h4>診療案内</h4>' in content and '<h4>医院情報</h4>' in content:
        # 開始位置: <h4>診療案内</h4> の前の <div>
        # 終了位置: <h4>医院情報</h4> のブロックの終わり
        
        # 文字列操作で置換
        # index.htmlなどのファイル構造に依存するが、基本的に同じはず
        
        # 診療案内の前のdivを探す
        idx_medical = content.find('<h4>診療案内</h4>')
        if idx_medical != -1:
            idx_start = content.rfind('<div>', 0, idx_medical)
            
            # 医院情報の後のdiv閉じを探す
            idx_clinic = content.find('<h4>医院情報</h4>')
            # 医院情報のdiv閉じ: <h4>医院情報</h4> -> </div> -> </div>
            # 単純に文字列で見つける
            
            # 医院情報ブロックの中身
            # <h4>医院情報</h4> ... </div> ... </div>
            
            # 手動で範囲を指定するのは危険なので、大まかな文字列置換を試みる
            
            old_footer_block_pattern = r'<div>\s*<h4>診療案内</h4>\s*<div class="footer-links">[\s\S]*?</div>\s*</div>\s*<div>\s*<h4>医院情報</h4>\s*<div class="footer-links">[\s\S]*?</div>\s*</div>'
            
            new_footer_block = f'''<div>
          <h4>メニュー</h4>
          <div class="footer-links">
            <a href="{prefix}index.html">ホーム</a>
            <a href="{prefix}medical.html">診療案内</a>
            <a href="{prefix}hours.html">診療時間・アクセス</a>
            <a href="{prefix}about.html">医院案内</a>
            <a href="{prefix}news.html">お知らせ</a>
          </div>
        </div>'''

            content = re.sub(old_footer_block_pattern, new_footer_block, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

# ルートディレクトリのHTMLファイル
root_files = [f for f in os.listdir('.') if f.endswith('.html')]
for file in root_files:
    update_file(file, is_symptoms=False)

# symptomsディレクトリのHTMLファイル
if os.path.exists('symptoms'):
    symptoms_files = [os.path.join('symptoms', f) for f in os.listdir('symptoms') if f.endswith('.html')]
    for file in symptoms_files:
        update_file(file, is_symptoms=True)
