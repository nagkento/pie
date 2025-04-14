from PIL import Image, ImageDraw
import sqlite3
import pyodbc
"""
DBから要素名とその件数を取得{辞書？}
[(1,mesh, xxx, 5), (), ()]

"""

# np.arrayを使った方が良いか
def draw_pie(all_values, image_size, output_png):
    # キャンバスの作成
    # ＃＃＃＃＃＃＃＃＃＃これで白紙の画像が返ってくる
    img = Image.new('RGBA', image_size, 'white')
    # 白紙の画像を引数として
    draw = ImageDraw.Draw(img)

    # データ解析
    sum_values = 0
    for i in all_values:
        sum_values += i[2]
    
    print(sum_values)
    
    num_list = [a[2] for a in all_values]
    max_value = max(num_list)
    # 最大半径
    max_radius = min(image_size) // 2 - 10  # 余白10px
    
    # 描画中心
    cx, cy = image_size[0] // 2, image_size[1] // 2
    start_angle = 0
    
    # RGB形式でも可能
    colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'magenta', 'yellow']
    
    for i, value in enumerate(all_values):
        # セクタの割合（角度）を算出
        angle = 360 * value[2]/sum_values
        angle_end = start_angle + angle
        
        radius = int(max_radius * (value[2]/max_value))
        
        # セクタの描画範囲
        bbox = [
            cx - radius, cy - radius,
            cx + radius, cy + radius
        ]
        
        # 色設定
        color = colors[i % len(colors)]

        # セクタ描画
        #　↑で設定した情報を元にキャンバスに描画
        draw.pieslice(bbox, start=start_angle, end=angle_end, fill=color, outline='black')
        
        # これをすることで、描画したセクタの次に描画される位置が決まる
        start_angle = angle_end
        
    img.save(output_png)
    
    
# データベース接続
conn = sqlite3.connect("example.db")
cur = conn.cursor()

data = [("apple", 8), 
        ("greap", 6),
        ("orange", 9),
        ("melon", 11)]

cur.execute('create table if not exists mng_data (rid integer primary key autoincrement, name text, counts insteger)')
cur.executemany('insert into mng_data (name, counts) values (?, ?)', data) 
conn.commit()

sql ="select * from mng_data"
cur.execute(sql)
all_values = cur.fetchall()# [(1,mesh, xxx, 5), (), ()]
print(all_values)



# meshを引数とした関数を呼ぶ
mesh = "000-jp-494906" + ".png"
draw_pie(all_values, image_size =(500,500), output_png = mesh)

cur.execute('drop table mng_data')
conn.close()

        