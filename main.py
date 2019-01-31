from flask import Flask
import json
from datetime import date, timedelta
import os
from order_functions import *

# import socket
# ip_addr = socket.gethostbyname(socket.gethostname())
# print(ip_addr)


user_file = open('tables.json', encoding='utf-8')
user_str = user_file.read()
user_dic = json.loads(user_str)
ip_dic = {}
hot_bev_l = csv_to_matrix('menus/sicakicecekler.csv')

cold_bev_l = csv_to_matrix('menus/sogukicecekler.csv')
alc_bev_l = csv_to_matrix('menus/alkol.csv')
foods_l = csv_to_matrix('menus/yiyecek.csv')
desserts_l = csv_to_matrix('menus/tatli.csv')
menu_matrix = [hot_bev_l, cold_bev_l, alc_bev_l, foods_l, desserts_l]
menu_dic = {}

for item in menu_matrix:
    for item2 in item:
        dicti = dict([(item2[0], item2[1])])
        menu_dic.update(dicti)

hotbev = add_text(hot_bev_l, '800000')
coldbev = add_text(cold_bev_l, 'blue')
alcoholicbev = add_text(alc_bev_l, '808080')
foods = add_text(foods_l, '008080')
desserts = add_text(desserts_l, 'c69802')

app = Flask(__name__, static_url_path='')


@app.route("/")
def index():
    index_yazi = ''

    for i in range(1, 21):
        if user_dic['table{}'.format(i)]['orders'][0]:
            if i < 6:
                index_yazi = index_yazi + """
                
                <p style="font-size:8vw; font-family:verdana;" ><a href="table{0}" style="color:limegreen">Front Table {0}</a></p>
                """.format(i)
            elif 5 < i < 11:
                index_yazi = index_yazi + """
                
                <p style="font-size:8vw; font-family:verdana;" ><a href="table{0}" style="color:limegreen">Back Table {0}</a></p>
                """.format(i)
            else:
                index_yazi = index_yazi + """
                
                <p style="font-size:8vw; font-family:verdana;" ><a href="table{0}" style="color:limegreen">Table {0}</a></p>
                """.format(i)

        else:
            if i < 6:
                index_yazi = index_yazi + """
                
                <p style="font-size:8vw; font-family:verdana;" ><a href="table{0}" style="color:red">Front Table {0}</a></p>
                """.format(i)
            elif i > 5 and i < 11:
                index_yazi = index_yazi + """
                
                <p style="font-size:8vw; font-family:verdana;" ><a href="table{0}" style="color:red">Back Table {0}</a></p>
                """.format(i)
            else:
                index_yazi = index_yazi + """
                
                <p style="font-size:8vw; font-family:verdana;" ><a href="table{0}" style="color:red">Table {0}</a></p>
                """.format(i)

    index_yazi = index_yazi + """
    <p style="font-size:8vw; font-family:verdana;"><a href="kontrol_sayfasi" style="color:orange;">All Tables</a></p>
    <p style="font-size:8vw; font-family:verdana;"><a href="gunsonu" style="color:black">End Day</a></p>
        
        
    """
    return "<center>{}</center>".format(index_yazi)


@app.route('/kategoriler')
def kategoriler():
    return """
    <h1 style="font-size:8vw;"><a href="hotbev">Hot Beverages</a></h1>
    <h1 style="font-size:8vw;"><a href="coldbev">Cold Beverages</a></h1>
    <h1 style="font-size:8vw;"><a href="alcoholicbev">Alcoholic Beverages</a></h1>
    <h1 style="font-size:8vw;"><a href="foods">Foods</a></h1>
    <h1 style="font-size:8vw;"><a href="desserts">Desserts</a></h1>"""


@app.route('/siparisekle', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        for key, value in result.items():
            urun = key
            adet = value

        return """<meta http-equiv="refresh" content="0; url={0}ekle{1}" />""".format(urun, adet)


@app.route('/iskonto', methods=['POST', 'GET'])
def iskonto():
    if request.method == 'POST':
        active_orders = user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders']
        result = request.form

        for key, value in result.items():
            name = key
            oran = value
        oran = float(oran)
        active_orders.append(["Discount", 1, -1 * oran])

        with open('tables.json', 'w', encoding='utf-8') as json_file:
            json.dump(user_dic, json_file, ensure_ascii=False, indent=4)

        return '<meta http-equiv="refresh" content="0; url={}" />'.format(ip_dic[request.remote_addr][1])


@app.route('/ozelekle', methods=['POST', 'GET'])
def ozelekle():
    if request.method == 'POST':
        if not user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders'][0]:
            user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['hour'] = strftime("%d/%m/%Y %H:%M:%S")
        user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders'][0] = [1, 0, 0]

        result = request.form
        urun = result['urun']
        fiyat = result['fiyat']
        adet = result['adet']

        user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders'].append([urun, int(adet), float(fiyat)])

        with open('tables.json', 'w', encoding='utf-8') as json_file:
            json.dump(user_dic, json_file, ensure_ascii=False, indent=4)

        return '<meta http-equiv="refresh" content="0; url=table{}" />'.format(ip_dic[request.remote_addr][0])


@app.route('/<name>')
def hello_name(name):
    if name[:6] == "table0":
        return '<meta http-equiv="refresh" content="0; url=/" />'
    if name[:5] == "table":  # tablesın sayfaları

        global ip_dic_a
        ip_dic_a = {request.remote_addr: [int(name[5:]), '']}
        ip_dic.update(ip_dic_a)

        comingfrom = 'table{}'.format(ip_dic[request.remote_addr][0])
        ip_dic[request.remote_addr][1] = comingfrom

        global acilmasaati
        acilmasaati = user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['hour']

        if user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders'][0]:
            active_orders = user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders']
            global order_text

            order_text = """
                        <!DOCTYPE html>
            <html>
            <head>
            <style>
            table {
                font-family: verdana;
                font-size:4vw;
                border-collapse: collapse;
                width: 90%;
            }
            
            td, th {
                border: 1px solid #dddddd;
                text-align: center;
                padding: 8px;
            }
            
            tr:nth-child(even) {
                background-color: #dddd94;
            }
            </style>
            </head>
            <body>
            
            <center>
            <table>
              <tr>
                <th>Product</th>
                <th>Qty</th>
                <th>Price</th>
                <th>Add/Drop</th>
              </tr>
            
            """

            for item in active_orders[1:]:
                order_text = order_text + """
                
                <tr>
    <td>{0}</td>
    <td>{1}</td>
    <td>{3} TL</td>
    <td><a href="{0}ekle1" style="color:limegreen;">+1</a> <a href="{0}cikar1" style="color:red">-1</a> <a href="{0}cikar{1}" style="color:990000">0</a></td>
  </tr>
                
                
                """.format(
                    str(item[0]), str(item[1]), str(item[2]), str(item[1] * item[2]))

            order_text = order_text + """</table>
</center>
</body>
</html>"""
            global toplam
            toplam = 0
            for item in active_orders:
                toplam = toplam + item[1] * item[2]

            return """<center>
        <p style="font-size:8vw; font-family:verdana; color:limegreen;">Table {0} <a href="/" style="color:black; font-size:6vw; ">Main Menu</a></p>
        <p style="font-size:4vw; font-family:verdana; color:blue;">Opening date: {3}</p>
        {1}
        <p style="font-size:3vw; font-family:verdana">Total: {2} TL</p>
        <p style="font-size:8vw; font-family:verdana">
        <a href="hotbev" style="color:800000">Hot Beverages</a><br><br>
        <a href="coldbev" style="color:00FFFF">Cold Beverages</a><br><br>
        <a href="alcoholicbev" style="color:808080">Alcoholic Beverages</a><br><br>
        <a href="foods" style="color:008080">Foods</a><br><br>
        <a href="desserts" style="color:FFC300">Desserts</a><br></p>
       

<p style="color:b30086; font-size:8vw; font-family:verdana; ">Add Special Product</p>

<form action = "/ozelekle" method="POST">
    <input type="text" name="urun" placeholder="Product" style="font-family:verdana; font-size:5vw; color:b30086; width: 30%;">
    <input type="number" name="fiyat" placeholder="TL" style="font-family:verdana; font-size:5vw; color:b30086; width: 15%;">
    <select name="adet" style="font-family:verdana; font-size:4vw; background-color:b3086;">
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>  
        <option value="5">5</option>
        <option value="6">6</option>
        <option value="7">7</option>
        <option value="8">8</option>    
        <option value="9">9</option>
    </select>
    <button type="submit" style="font-family:verdana; font-size:5vw; background-color:b30086; border-radius: 8px; color:ffffff">Add</button>
</form>

</p>
<br><br>
        <p style="font-size:8vw; font-family:verdana">
        <a href="sifirla" style="color:red">Close Table(If opened by mistake)</a><br><br>
        <a href="hesapkes" style="color:blue">Get Check</a><br><br>
        <a href="/" style="color:black;">Main Menu</a>
        </p></center>
        
            """.format(ip_dic[request.remote_addr][0], order_text, toplam, acilmasaati)
        else:
            order_text = ''
            toplam = ''
            return """
                    <center><p style="font-size:8vw; font-family:verdana; color:red;">Table {0}</p>
                    <p style="font-size:5vw; font-family:verdana">No orders has entered</p>
                    <p style="font-size:8vw; font-family:verdana">
                    <a href="hotbev" style="color:800000">Hot Beverages</a><br><br>
                    <a href="coldbev" style="color:00FFFF">Cold Beverages</a><br><br>
                    <a href="alcoholicbev" style="color:808080">Alcoholic Beverages</a><br><br>
                    <a href="foods" style="color:008080">Foods</a><br><br>
                    <a href="desserts" style="color:FFC300">Desserts</a><br></p>
                    <p style="color:b30086; font-size:8vw; font-family:verdana; ">Add Special Product</p>

<form action = "/ozelekle" method="POST">
    <input type="text" name="urun" placeholder="Product" style="font-family:verdana; font-size:5vw; color:b30086; width: 30%;">
    <input type="number" name="fiyat" placeholder="TL" style="font-family:verdana; font-size:5vw; color:b30086; width: 15%;">
    <select name="adet" style="font-family:verdana; font-size:5vw; color:b3086;"">
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>  
        <option value="5">5</option>
        <option value="6">6</option>
        <option value="7">7</option>
        <option value="8">8</option>    
        <option value="9">9</option>
    </select>
    <button type="submit" style="font-family:verdana; font-size:5vw; background-color:b30086; border-radius: 8px; color:ffffff">Add</button>
</form>
                    
                    <p style="font-size:8vw; font-family:verdana"><a href="/" style="color:black;">Main Menu</a></p></center>
                        """.format(ip_dic[request.remote_addr][0])

    if name == "hotbev":
        ip_dic[request.remote_addr][1] = name
        order_text = update_order_text(ip_dic,user_dic)

        return """<center>
        <a style="font-size:8vw; font-family:verdana; color:limegreen;" href="table{0}">Table {0}</a>
        {1}
        <br> <br>
        {2}
        """.format(ip_dic[request.remote_addr][0], order_text, hotbev)

    if name == "coldbev":
        ip_dic[request.remote_addr][1] = name
        order_text = update_order_text(ip_dic,user_dic)
        return """<center>
                <a style="font-size:8vw; font-family:verdana; color:limegreen;" href="table{0}">Table {0}</a>
                {1}
        <br> <br>
        {2}
                """.format(ip_dic[request.remote_addr][0], order_text, coldbev)
    if name == "alcoholicbev":
        ip_dic[request.remote_addr][1] = name
        order_text = update_order_text(ip_dic,user_dic)
        return """<center>
                <a style="font-size:8vw; font-family:verdana; color:limegreen;" href="table{0}">Table {0}</a>
                {1}
        <br> <br>
        {2}
                """.format(ip_dic[request.remote_addr][0], order_text, alcoholicbev)
    if name == "foods":
        ip_dic[request.remote_addr][1] = name
        order_text = update_order_text(ip_dic,user_dic)
        return """<center>
                <a style="font-size:8vw; font-family:verdana; color:limegreen;" href="table{0}">Table {0}</a>
                {1}
        <br> <br>
        {2}
                """.format(ip_dic[request.remote_addr][0], order_text, foods)

    if name == "desserts":
        ip_dic[request.remote_addr][1] = name
        order_text = update_order_text(ip_dic,user_dic)
        return """<center>
                <a style="font-size:8vw; font-family:verdana; color:limegreen;" href="table{0}">Table {0}</a>
                <p style="font-size:3vw; font-family:verdana">{1}</p></center>
                {2}
                """.format(ip_dic[request.remote_addr][0], order_text, desserts)

    if name == "hesapkes":
        order_text = update_order_text(ip_dic,user_dic)
        toplam = update_sum(ip_dic,user_dic)
        ip_dic[request.remote_addr][1] = name
        hesapkes_yazi = """<center>
        <p style="color:28cbd2; font-size:8vw; font-family:verdana; ">Discount (TL)</p>
        <form action = "/iskonto" method="POST">
    <input type="number"; name="iskonto" placeholder="TL" style="font-family:verdana; font-size:5vw; color:28cbd2;width: 15%;">
    <button type="submit" style="font-family:verdana; font-size:5vw; background-color:28cbd2; border-radius: 8px; color:ffffff">Add</button>
</form>
<a style="color:ff8000; font-size:8vw; font-family:verdana; " href="yazdir">Print Receipt</a><br><br>
<a href="sifirla_hesapkes" style="color:red; font-size:8vw; font-family:verdana; ">Close Table</a><br><br>
</center>
"""

        return """<center>
                <a style="font-size:8vw; font-family:verdana; color:limegreen;" href="table{0}">Table {0}</a>
                <p style="font-size:4vw; font-family:verdana; color:blue;">Opening date: {4}</p>
                {1}
                <p style="font-size:3vw; font-family:verdana">Total: {2} TL</p></center>
                {3}
                """.format(ip_dic[request.remote_addr][0], order_text, toplam, hesapkes_yazi, acilmasaati)

    if name == "sifirla_hesapkes":

        o_table = user_dic['table{}'.format(ip_dic[request.remote_addr][0])]

        if int(strftime("%H")) < 7:
            yesterday = date.today() - timedelta(1)

            directory = 'Gunsonlari/{0}/{1}'.format(yesterday.strftime("%Y"), yesterday.strftime("%m"))
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open('GunSonlari/{0}/{1}/{2}.csv'.format(yesterday.strftime("%Y"), yesterday.strftime("%m"),
                                                          yesterday.strftime("%d%m%Y")), 'a', encoding='utf-8') as fd:
                writer = csv.writer(fd, delimiter=';')
                for i in range(1, len(o_table['orders'])):
                    writer.writerow(
                        ["Table {}".format(o_table['tableno']), o_table['hour'], strftime("%d/%m/%Y %H:%M:%S"),
                         o_table['orders'][i][0], o_table['orders'][i][1], o_table['orders'][i][2],
                         o_table['orders'][i][1] * o_table['orders'][i][2]])
        else:

            directory = 'Gunsonlari/{0}/{1}'.format(strftime("%Y"), strftime("%m"))
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open('GunSonlari/{0}/{1}/{2}.csv'.format(strftime("%Y"), strftime("%m"), strftime("%d%m%Y")), 'a',
                      encoding='utf-8') as fd:
                writer = csv.writer(fd, delimiter=';')
                for i in range(1, len(o_table['orders'])):
                    writer.writerow(
                        ["Table {}".format(o_table['tableno']), o_table['hour'], strftime("%d/%m/%Y %H:%M:%S"),
                         o_table['orders'][i][0], o_table['orders'][i][1], o_table['orders'][i][2],
                         o_table['orders'][i][1] * o_table['orders'][i][2]])

        user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders'] = [[]]
        user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['hour'] = ''

        with open('tables.json', 'w', encoding='utf-8') as json_file:
            json.dump(user_dic, json_file, ensure_ascii=False, indent=4)

        return '<meta http-equiv="refresh" content="0; url=/" />'

    if name == "sifirla":
        user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders'] = [[]]
        user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['hour'] = ''

        with open('tables.json', 'w', encoding='utf-8') as json_file:
            json.dump(user_dic, json_file, ensure_ascii=False, indent=4)

        return '<meta http-equiv="refresh" content="0; url=/" />'

    if name[len(name) - 5:-1] == 'ekle':
        if not user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders'][0]:
            user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['hour'] = strftime("%d/%m/%Y %H:%M:%S")
        user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders'][0] = [1, 0, 0]
        kontrol = 0
        for item in user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders']:
            if name[:-5] == item[0]:
                item[1] = int(item[1]) + int(name[-1])
                kontrol = kontrol + 1
        if kontrol == 0:
            user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders'].append(
                [name[:-5], int(name[-1]), float(menu_dic[name[:-5]])])

        with open('tables.json', 'w', encoding='utf-8') as json_file:
            json.dump(user_dic, json_file, ensure_ascii=False, indent=4)

        return '<meta http-equiv="refresh" content="0; url={}" />'.format(ip_dic[request.remote_addr][1])

    if name[len(name) - 6:-1] == 'cikar' or name[len(name) - 7:-2] == 'cikar' or name[
                                                                                 len(name) - 8:-3] == 'cikar' or name[
                                                                                                                 len(
                                                                                                                         name) - 9:-4] == 'cikar':

        for item in user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders']:
            if name[:-6] == item[0] or name[:-7] == item[0] or name[:-8] == item[0] or name[:-9] == item[0]:
                if name[-4:].isdigit():
                    item[1] = int(item[1]) - int(name[-4:])
                elif name[-3:].isdigit():
                    item[1] = int(item[1]) - int(name[-3:])
                elif name[-2:].isdigit():
                    item[1] = int(item[1]) - int(name[-2:])
                else:
                    item[1] = int(item[1]) - int(name[-1])
        try:
            for i in range(len(user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders'])):
                if str(user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders'][i][1]) == '0' and str(
                        user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders'][i][0]) != '1':
                    del user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders'][i]
        except:
            print("indexError")

        with open('tables.json', 'w', encoding='utf-8') as json_file:
            json.dump(user_dic, json_file, ensure_ascii=False, indent=4)

        return '<meta http-equiv="refresh" content="0; url=table{}" />'.format(ip_dic[request.remote_addr][0])

    if name == "ayarlar":
        ayarlar = "AYARLAR"
        # return """
        #
        #         <p style="font-size:6vw; font-family:verdana">
        #             <a href="tummasakapat" style="color:800000">Tüm tablesı kapat</a><br><br>
        #             <a href="loadlast" style="color:00FFFF">Son kayıtlı tablesı yükle</a><br><br>
        #             <a href="yenile" style="color:008080">Bir şeyler ters gidiyor</a><br><br>
        #             <a href="gunsonu" style="color:FFC300">Gün sonu kaydet</a><br></p>
        #
        #         """.format(ayarlar)

        return '<meta http-equiv="refresh" content="0; url=gunsonu" />'

    if name == "yazdir":
        print_receipt(ip_dic,user_dic)
        return '<meta http-equiv="refresh" content="0; url={}" />'.format(ip_dic[request.remote_addr][1])

    if name == "gunsonu":

        toplam_gunsonu = 0

        if int(strftime("%H")) < 7:
            yesterday = date.today() - timedelta(1)

            o_gun_satilanlar = csv_to_matrix(
                'GunSonlari/{0}/{1}/{2}.csv'.format(yesterday.strftime("%Y"), yesterday.strftime("%m"),
                                                    yesterday.strftime("%d%m%Y")))
            o_gun_satilanlar = [s for s in o_gun_satilanlar if s]

            for item in o_gun_satilanlar:
                if item:
                    toplam_gunsonu = toplam_gunsonu + float(item[6])

            with open('GunSonlari/{0}/{1}/{2}.csv'.format(yesterday.strftime("%Y"), yesterday.strftime("%m"),
                                                          yesterday.strftime("%d%m%Y")), 'a',
                      encoding='utf-8') as fd:
                writer = csv.writer(fd, delimiter=';')

                writer.writerow(["Total", None, None,
                                 None, None, None,
                                 toplam_gunsonu])

        else:

            o_gun_satilanlar = csv_to_matrix(
                'GunSonlari/{0}/{1}/{2}.csv'.format(strftime("%Y"), strftime("%m"), strftime("%d%m%Y")))
            for item in o_gun_satilanlar:
                if item:
                    try:
                        toplam_gunsonu = toplam_gunsonu + float(item[6])
                    except ValueError:
                        print("value error")

            with open('GunSonlari/{0}/{1}/{2}.csv'.format(strftime("%Y"), strftime("%m"), strftime("%d%m%Y")), 'a',
                      encoding='utf-8') as fd:
                writer = csv.writer(fd, delimiter=';')

                writer.writerow(["Total", None, None,
                                 None, None, None,
                                 toplam_gunsonu])

        return ('<meta http-equiv="refresh" content="0; url=/" />')

    if name == "kontrol_sayfasi":
        kontrol_yazi = '<a href="/" style="font-size:3vw; font-family:verdana">Main Menu</a><br>'

        for item in user_dic:
            if user_dic[item]['orders'][0]:
                kontrol_yazi = kontrol_yazi + '<a style="font-size:5vw; font-family:verdana; color:blue;" href="table{0}">Table {0}</a>'.format(
                    user_dic[item]['tableno'])
                toplam_k = 0
                kontrol_yazi = kontrol_yazi + update_order_text_i(ip_dic,user_dic,user_dic[item]['orders'])
                for item in user_dic[item]['orders']:
                    toplam_k = toplam_k + item[1] * item[2]
                kontrol_yazi = kontrol_yazi + '<p style="font-size:3vw; font-family:verdana">Total: {} TL</p>'.format(
                    toplam_k)

        return '<center>{}</center>'.format(kontrol_yazi)

    else:
        return """<p style="font-size:6vw; font-family:verdana">{} diye bir sayfa yok.<br>
        <a href="/" style="color:800000">Main Menu</a></p>""".format(name)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", threaded=True)
