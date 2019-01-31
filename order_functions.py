import csv
from flask import request
from time import strftime
def print_receipt(ip_dic,user_dic):
    import win32ui, win32con, win32gui, win32print, traceback

    tarihsaat = strftime("%d/%m/%Y %H:%M:%S")
    active_orders = user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders']
    yazi = 'Table {}\n\n{}\n\n\n'.format(ip_dic[request.remote_addr][0], tarihsaat)
    toplam_y = 0
    iskonto_kontrol = 0
    for item in active_orders:
        if item[0] == 'Discount':
            iskonto_kontrol = 1

    if iskonto_kontrol == 1:
        for item in active_orders[1:-1]:
            yazi = yazi + """{0} {1} x {2} TL ={3} TL\n""".format(
                str(item[0]), str(item[1]), str(item[2]), str(item[1] * item[2]))
            toplam_y = toplam_y + item[1] * item[2]
        yazi = yazi + "\nTotal: {} TL\n".format(toplam_y)
        yazi = yazi + "Discount: {} TL\n".format(-active_orders[-1][1] * active_orders[-1][2])
        yazi = yazi + "Hesap: {} TL\n".format(toplam_y + (active_orders[-1][1] * active_orders[-1][2]))
    else:
        for item in active_orders[1:]:
            yazi = yazi + """{0} {1} x {2} TL ={3} TL\n""".format(
                str(item[0]), str(item[1]), str(item[2]), str(item[1] * item[2]))
            toplam_y = toplam_y + item[1] * item[2]
        yazi = yazi + "\nTotal: {} TL\n".format(toplam_y)

    yazi = yazi + "\nMali değeri yoktur.\n"

    # init, bla bla bla
    printername = win32print.GetDefaultPrinter()
    hprinter = win32print.OpenPrinter(printername)
    # load default settings
    devmode = win32print.GetPrinter(hprinter, 8)["pDevMode"]
    # this is where it gets INTERESTING:
    # after the following two lines, use:
    # dc for win32ui calls like LineTo, SelectObject, ...
    # hdc for DrawTextW, your *MAGIC* function that supports unicode output
    hdc = win32gui.CreateDC("WINSPOOL", printername, devmode)
    dc = win32ui.CreateDCFromHandle(hdc)

    # 1440 twips = 1 inch
    dc.SetMapMode(win32con.MM_TWIPS)
    # 20 twips = 1 pt
    scale_factor = 20

    # start the document, description as unicode
    description = u'Test1'
    dc.StartDoc(description)

    # when working with the printer, enclose any potentially failing calls within a try block,
    # because if you do not properly end the print job (see bottom), after a couple of such failures,
    # you might need to restart windows as it runs out of handles or something and starts
    # behaving in an unpredictable way, some documents fail to print, you cannot open windows, etc.

    try:

        # Use a font
        font = win32ui.CreateFont({
            "name": "Arial Unicode MS",  # a font name
            "height": int(scale_factor * 14),  # 14 pt
            "weight": 400,  # 400 = normal
        })

        # use dc -- SelectObject is a win32ui call
        dc.SelectObject(font)

        # this is the miracle where the unicode text gets to be printed; notice hdc,
        # not dc, for DrawTextW uses a different handle, i have found this in other posts

        win32gui.DrawTextW(hdc, yazi, -1, (0, 0, 4000, -12000), win32con.DT_CENTER)

    except:
        traceback.print_exc()

    # must not forget to tell Windows we're done. This line must get called if StartDoc
    # was called, if you fail to do so, your sys might start behaving unexpectedly
    dc.EndDoc()


def csv_to_matrix(file):
    with open(file, encoding="utf-8") as liste:
        reader = csv.reader(liste, delimiter=';')
        matrix = list(reader)
    return matrix


def update_order_text(ip_dic,user_dic):
    active_orders = user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders']
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
                    border: 1px solid #dddd94;
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
    return order_text


def update_order_text_i(ip_dic, user_dic,active_orders="a"):
    if active_orders == "a":
        active_orders = user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders']
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
                    border: 1px solid #dddd94;
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
                    <th></th>
                    <th>Qty</th>
                    <th>Price</th>

                  </tr>

                """

    for item in active_orders[1:]:
        order_text = order_text + """

                    <tr>
        <td>{0}</td>
        <td>{1}</td>
        <td>{3} TL</td>
         </tr>


                    """.format(
            str(item[0]), str(item[1]), str(item[2]), str(item[1] * item[2]))

    order_text = order_text + """</table>
    </center>
    </body>
    </html>"""
    return order_text


def update_sum(ip_dic,user_dic):
    active_orders = user_dic['table{}'.format(ip_dic[request.remote_addr][0])]['orders']
    toplam = 0
    for item in active_orders:
        toplam = toplam + item[1] * item[2]
    return toplam


def add_text(matrix, color="cccccc"):
    text = """
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
    background-color: #dddddd;
}
</style>
</head>
<body>

<center>
<table>
  <tr>
    <th>Product</th>
    <th>Price</th>
    <th>Add</th>
  </tr>

    """
    for item in matrix:
        # text = text + '<center><p style="font-size:4vw; font-family:verdana">' + item[0] + ' ' + item[1] + 'TL ' + '<a href="{0}ekle1" style="color:grey"> 1+</a>'.format(item[0]) + '<a href="{0}ekle2" style="color:red"> 2+</a>'.format(item[0]) + '<a href="{0}ekle3" style="color:grey"> 3+</a>'.format(item[0]) + '<a href="{0}ekle4" style="color:red"> 4+</a>'.format(item[0]) + '<a href="{0}ekle5" style="color:grey"> 5+</a>'.format(item[0]) + '<a href="{0}ekle6" style="color:red"> 6+</a>'.format(item[0]) + '<a href="{0}ekle7" style="color:grey"> 7+</a>'.format(item[0]) + '<a href="{0}ekle8" style="color:red"> 8+</a>'.format(item[0]) + '</p></center>'
        text = text + """
    <tr>
        <td>{0}</td>
        <td>{1}</td>
        <td><form name="Item_1" action="/siparisekle" method='POST'>
         <select name="{0}" style="font-family:verdana; font-size:4vw; background-color:{color}; color:white;">
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
        <button type="submit" style="font-family:verdana; font-size:4vw; background-color:{color}; color:white; border-radius: 8px;">Add</button>
    </form></td>
    </tr>
        """.format(item[0], item[1], color=color)

    text = text + """
    </table>
</center>
</body>
</html>

    """
    return text

