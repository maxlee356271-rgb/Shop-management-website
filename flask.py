from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import date, timedelta
import csv, sqlite3, os


app = Flask(__name__)
app.secret_key = "purepacking11105"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "stocks.db")
keylist = {}
products = {
            "17丝网格真空袋": [
                "[008a] 15x20(16)",
                "[010a] 17x25(16)",
                "[011a] 20x25(16)",
                "[012a] 20x30(16)",
                "[014a] 25x30(16)-50pc"
            ],
    
            "19丝纹路真空袋": [
                "[001] 7x10",
                "[002] 7x12",
                "[003] 9x13",
                "[004] 10x15",
                "[005] 12x17",
                "[006] 12x20",
                "[007] 13x18",
                "[008b] 15x20",
                "[009b] 15x25",
                "[010b] 17x25",
                "[011b] 20x25",
                "[012b] 20x30",
                "[013] 22x32",
                "[014b] 25x30",
                "[015b] 25x35",
                "[016b] 30x40"
            ],
    
            "22丝纹路真空袋": [
                "[008c] 15x20(22)",
                "[009c] 15x25(22)",
                "[010c] 17x25(22)",
                "[011c] 20x25(22)",
                "[012c] 20x30(22)",
                "[015c] 25x35(22)"
            ],
    
            "16丝PET袋": [
                "[018] 光6x8",
                "[019] 光7x10",
                "[020] 光8x10",
                "[021] 光8x12",
                "[022] 光9x13",
                "[023] 光10x15",
                "[024] 光11x16",
                "[025] 光12x17",
                "[026] 光13x18",
                "[027] 光15x20",
                "[028] 光15x22",
                "[029] 光16x24",
                "[030] 光17x25",
                "[032] 光18x26",
                "[033] 光20x25",
                "[034] 光20x30",
                "[035] 光22x32",
                "[036] 光25x30",
                "[037] 光25x35",
                "[038] 光28x40",
                "[039] 光30x40",
                "[040] 光35x50",
                "[041] 光40x60"
            ],
    
            "16丝镀鋁三边封": [
                "[044] 镀9x13",
                "[045] 镀10x15",
                "[046] 镀12x17",
                "[047] 镀13x18",
                "[048] 镀15x20",
                "[049] 镀18x25",
                "[050] 镀20x30"
            ],
    
            "16丝尼龙真空袋": [
                "[051] 尼12x17(16)",
                "[052] 尼13x18(16)",
                "[053a] 尼15x20(16)",
                "[054] 尼16x23(16)",
                "[055] 尼17x25(16)",
                "[056a] 尼18x26(16)",
                "[057a] 尼20x25(16)",
                "[058] 尼20x28(16)",
                "[059a] 尼20x30(16)",
                "[060a] 尼25x35(16)"
            ],
    
            "24丝尼龙真空袋": [
                "[053b] 尼15x20(24)",
                "[056b] 尼18x26(24)",
                "[057b] 尼20x25(24)",
                "[059b] 尼20x30(24)",
                "[060b] 尼25x35(24)",
                "[060m] 尼30x40(24)"
            ],
    
            "20丝高温蒸煮袋": [
                "[060x] ret 13x18(20)",
                "[061] ret 15x20(20)",
                "[062] ret 18x25(20)",
                "[063] ret 20x30(20)"
            ],
    
            "20丝磨砂自立自封袋": [
                "[064] 立9x15+3(20)",
                "[065] 立11x17+3(20)",
                "[066] 立12x19+3(20)",
                "[067] 立13x20+4(20)",
                "[068] 立14x20+4(20)",
                "[069] 立15x22+4(20)",
                "[070] 立16x23+4(20)",
                "[071] 立17x24+4(20)",
                "[072] 立18x26+4(20)",
                "[073] 立20x30+5(20)",
                "[075] 立24x35+5(20)"
            ],
    
            "20丝磨砂平底自封袋": [
                "[076] 平8x12(20)",
                "[077] 平9x15(20)",
                "[078] 平10x15(20)",
                "[079] 平11x17(20)",
                "[080] 平12x18(20)",
                "[081] 平13x20(20)",
                "[082] 平14x22(20)",
                "[083] 平15x24(20)",
                "[084] 平20x30(20)"
            ],
    
            "24丝白磨砂自立自封袋": [
                "[085] W10x15+3(24)",
                "[086] W13x18+4(24)",
                "[087] W15x22+4(24)",
                "[088] W18x26+4(24)",
                "[089] W20x30+5(24)"
            ],
    
            "24丝黑磨砂自立自封袋": [
                "[090] B10x15+3(24)",
                "[091] B13x18+4(24)",
                "[092] B15x22+4(24)",
                "[093] B18x26+4(24)",
                "[094] B20x30+5(24)"
            ],

            "14丝金CPP阴阳自立自封": [
                "[094a] G10x15+3(14)",
                "[094b] G12x20+4(14)",
                "[094c] G15x22+4(14)",
                "[094d] G18x26+4(14)"
            ],

            "24丝白磨砂消光平底自封": [
                "[095] W10x15(24)",
                "[096] W13x18(24)",
                "[097] W15x22(24)",
                "[098] W18x26(24)",
                "[099] W20x30(24)"
            ],

            "24丝黑磨砂消光平底自封": [
                "[100] B10x15(24)",
                "[101] B13x18(24)",
                "[102] B15x22(24)",
                "[103] B18x26(24)",
                "[104] B20x30(24)"
            ],

            "16丝尼龙自立自封袋": [
                "[105] 液透10x15+3(16)",
                "[106] 液透13x18+4(16)"
            ],

            "12丝珠光膜": [
                "[110] 珠6x10(12)",
                "[112] 珠7x10(12)",
                "[113] 珠7.5x12(12)",
                "[114] 珠8x14(12)",
                "[116] 珠9x13(12)",
                "[117] 珠10x12(12)",
                "[118] 珠10.5x15(12)",
                "[119] 珠11x16(12)",
                "[120] 珠12x18(12)",
                "[121] 珠12x20(12)",
                "[123] 珠14x20(12)",
                "[124] 珠16x24(12)"
            ],

            "高透锁骨夹链袋": [
                "[125] 高透7*11(12)",
                "[126] 高透8.5*13(12)",
                "[128] 高透10.5*15(12)"
            ],

            "16丝镀铝阴阳平底袋": [
                "[129] 镀7*13(14)",
                "[130] 镀8.5*14(14)",
                "[132] 镀10*17.5(14)",
                "[132a] 镀12*20(14)",
                "[133] 镀14*20(14)"
            ],

            "茶包": [
                "[146] 反折口玉米茶包6.5x7",
                "[147] 反折口玉米茶包8x8",
                "[148] 热封滤纸茶包5x6",
                "[149] 热封滤纸茶包6x8",
                "[149a] 热封滤纸茶包7x9",
                "[149b] 热封滤纸茶包8x10"
            ],

            "20丝纯铝风琴茶叶袋": [
                "[150] 茶叶袋9+8*28(20)",
                "[151] 茶叶袋14+8*30(20)",
                "[152] 茶叶袋16+8*38(20)"
            ],

            "16丝镀铝风琴茶叶袋": [
                        "[153] 茶叶袋14+8*30(16)",
                        "[154] 茶叶袋16+8*38(16)"
                    ],

            "其它项目": [
                "[144a] 0.86漏斗",
                "[144b] 1.5漏斗",
                "[144c] 0.86扭盖器",
                "[144d] 1.5扭盖器"
            ]
        }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cal")
def cal():
    return render_template("cal.html")

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return "no-file"
    file = request.files['file']
    if file.filename == '':
        return "wrong-file"
    if not file.filename.endswith(".csv"):
        return "wrong-file"
    return "success"

@app.route("/Type", methods=["POST"])
def shoptype():
    shop_type = request.form["type"]
    if shop_type == "Shopee":
        return "shopee"
    elif shop_type == "Tiktok":
        return "tiktok"
    return

@app.route("/result", methods=["POST"])
def Calculate():
    if 'file' not in request.files:
        return "no-file"
    file = request.files["file"]
    shop_type = request.form["type"]
    if file.filename == '':
        return "wrong-file"
    if not file.filename.endswith(".csv"):
        return "wrong-file"
    if shop_type == "Shopee":
        reader = csv.reader(file.stream.read().decode("utf-8").splitlines())
        next(reader)
        dic = dict()
        dic2 = dict()
        i = 1
        for row in reader:
            name = row[19]
            name = name[6:]
            if "-" in name:
                    index = name.find("-")
                    name = name[:index]
            try:
                quantity = float(row[22])
            except:
                pass
            if "-" not in row[21]:
                try:
                    price = float(row[21])
                except:
                    pass
            else:
                price = 0
            if name not in dic:
                dic[name] = quantity
                dic2[name] = quantity * price
            else:
                dic[name] += quantity
                dic2[name] += quantity * price
        rows = []
        for name in sorted(dic.keys()):
            qty = dic[name]
            total = dic2[name]
            avg = total / qty if qty != 0 else 0
            rows.append([name, qty, total, avg])
        session["rows"] = rows
        return "success"
    elif shop_type == "Tiktok":
        discount = 0
        reader = csv.reader(file.stream.read().decode("utf-8").splitlines())
        next(reader)
        dic3 = dict()
        dic4 = dict()
        for row in reader:
            if row[5] != "":
                name2 = row[5]
            if row[7] != "":
                quantity = row[7]
                quantity = int(quantity.replace(",", ""))
            if row[6] != "":
                price = row[6]
                price = int(price.replace(",", ""))
            if row[8] != "":
                discounts = row[8]
                discounts = int(discounts.replace(",", ""))
            if name2 not in dic3 and name2 != "ส่วนลดพิเศษ" and name2 != "รวม":
                dic3[name2] = quantity
                dic4[name2] = quantity * price
            elif name2 == "ส่วนลดพิเศษ":
                discount += discounts
            elif name2 == "รวม":
                continue
            else:
                dic3[name2] += quantity
                dic4[name2] += quantity * price
            rows = []
            for name2 in sorted(dic3.keys()):
                qty = dic3[name2]
                total = dic4[name2]
                avg = total / qty if qty != 0 else 0
                rows.append([name2, qty, total, avg])
        session["rows"] = rows
        return "success"
@app.route("/result")
def resultpage():
    rows = session.get("rows", [])
    print("Loaded rows:", rows)
    print("Saved rows:", len(rows))
    totalprice = 0
    totalqty = 0
    tps = 0
    tpsname = ""
    tpqty = 0
    tpqtyname = ""
    for row in rows:
        totalprice += row[2]
        totalqty += row[1]
        if row[2] > tps:
            tps = row[2]
            tpsname = row[0]
        if row[1] > tpqty:
            tpqty = row[1]
            tpqtyname = row[0]
    return render_template("result.html", rows=rows, totalprice=totalprice, totalqty=totalqty, tps=tps, tpsname=tpsname, tpqty=tpqty, tpqtyname=tpqtyname)

@app.route("/stocks")
def stock():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""create table if not exists purchase_order (
        id integer primary key AUTOINCREMENT,
        Week integer,
        PO text,
        SKU text,
        Qty integer,
        log text,
        time text,
        endtime text
    )""")
    conn.commit()
    cursor.execute("""
        SELECT time, endtime
        FROM purchase_order
        WHERE Week = 1
        LIMIT 1
    """)
    row = cursor.fetchone()
    weeks = {}
    today = date.today() - timedelta(days=date.today().weekday())
    if row:
        wk1date = date.fromisoformat(row[0])
        timedif = (today - wk1date).days // 7
        if timedif > 0:
            cursor.execute(
                "UPDATE purchase_order "
                "SET Week = Week - ? "
                "WHERE Week > ?",
                (timedif, timedif)
            )
            cursor.execute("""
                UPDATE purchase_order
                SET time = date(time, ?),
                    endtime = date(endtime, ?)
            """, (
                f"-{timedif * 7} days",
                f"-{timedif * 7} days"
            ))
    for i in range(9):
        endweek = today + timedelta(days=6)
        weeks[i] = str(today)[5:] + " - " + str(endweek)[5:]
        today = today + timedelta(days=7)
    conn.commit()
    cursor.execute(
        "select * from purchase_order"
    )
    rows = cursor.fetchall()
    print("rows", rows)
    total = {}
    for row in rows:
        if row[2] not in total:
            total[row[2]] = row[4]
        else:
            total[row[2]] += row[4]
    conn.commit()
    cursor.execute("""
    SELECT Week, PO, time, endtime
    FROM purchase_order
    ORDER BY Week
    """)

    print("BEFORE:")
    for row in cursor.fetchall():
        print(row)
    conn.close()
    return render_template("stocks.html", products=products, rows=rows, total=total, weeks=weeks)

@app.route("/stock", methods=["POST"])
def stockpost():
    targets = request.form.getlist("products")
    counts = request.form.getlist("count")
    keylist = {}
    for target, count in zip(targets, counts):
        for key, value in products.items():
            if target in value:
                print(key)
                if key not in keylist:
                    print("yes")
                    keylist[key] = [[target, count]]
                else:
                    keylist[key] += [[target, count]]
        
    print("list", keylist)
    return (jsonify(keylist))

@app.route("/save-db", methods=["POST"])
def savedb():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    wk = request.form['wk']
    PO = request.form["PO"]
    log = request.form["log"]
    pds = request.form.getlist("pd")
    counts = request.form.getlist("count")
    today = (date.today() + timedelta(days=7*(int(wk)-1))) - timedelta(days=date.today().weekday())
    endtime = today + timedelta(days=6)
    print("today", today)
    print("endtime", endtime)
    for pd, count in zip(pds, counts):
        cursor.execute(
            "insert into purchase_order(Week, PO, SKU, Qty, log, time, endtime) values(?, ?, ?, ?, ?, ?, ?)",
            (wk, PO, pd, int(count), log, today, endtime)
        )
    conn.commit()
    conn.close()
    return "success"

@app.route("/remove-db", methods=["POST"])
def removedb():
    po = request.form["po"]
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "delete from purchase_order where PO = ?",
        (po,)
    )
    conn.commit()
    conn.close()
    return "success"

@app.route("/check-po", methods=["POST"])
def checkpo():
    po = request.form["POcheck"]
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "select * from purchase_order where PO = ?",
        (po,)
    )
    result = cursor.fetchall()

    if result:
        print("exist")
        return "exist"
    else:
        print("no")
        return "no"
@app.route("/get-po", methods=["POST"])
def getpo():
    po = request.form["po"]
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "select SKU, Qty from purchase_order where PO = ?",
        (po,)
    )
    pds = cursor.fetchall()
    pdcolor = {}
    for pd in pds:
        for key, values in products.items():
            if pd[0] in values:
                pdcolor[pd[0]] = [key, pd[1]]
    conn.close()
    return jsonify(pdcolor)

@app.route("/stock-update", methods=["POST"])
def update():
    po = request.form["po"]
    pds = request.form.getlist("pd")
    counts = request.form.getlist("count")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for pd, count in zip(pds, counts):
        count = int(count)
        if count == 0:
            cursor.execute(
                "delete from purchase_order where PO = ? and SKU = ?",
                (po, pd)
            )
        elif count != 0:
            cursor.execute(
                "update purchase_order set Qty = ? where PO = ? and SKU = ?",
                (count, po, pd)
            )
    conn.commit()
    conn.close()
    return "success"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)