from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import json, os, secrets, string, requests
from datetime import datetime, timedelta
from time import time

app = Flask(__name__)
CORS(app)
app.secret_key = secrets.token_hex(32)

BOT_TOKEN = "8466851320:AAGc77X4DnPQRNkw7rVUhlpJVIcBlOcSlDA"
CHAT_ID = "8588555065"
OWNER_ID = 8588555065
LINK4M_API_KEY = "65c47d157fbdff4d79625e57"
PARTNER_ID = "70406595609"
PARTNER_KEY = "add9c7d61cb54ff1b447e2188c71a8c2"
DATA_FILE = "/tmp/data.json"

def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {"free_keys": {}, "licenses": {}, "used_keys": {}, "keys_history": []}

def save_data(d):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
    except:
        pass

data = load_data()

def generate_key():
    c = string.ascii_uppercase + string.digits
    r = lambda l: ''.join(secrets.choice(c) for _ in range(l))
    return f"QANH-{r(10)}-{r(10)}-{r(10)}-{r(5)}"

pending_verify = {}

# ===== HTML =====
HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QANH SHOP</title>
    <style>
        :root{--gold:#FFD700;--green:#00ff00;--red:#ff4444}
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Arial;color:#fff;min-height:100vh;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e)}
        .navbar{background:rgba(26,26,46,0.95);padding:15px 20px;display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid var(--gold)}
        .navbar .logo{font-size:22px;font-weight:bold;color:var(--gold)}
        .navbar .balance{background:rgba(0,0,0,0.5);border:1px solid var(--gold);border-radius:20px;padding:8px 15px;color:var(--gold);font-weight:bold;cursor:pointer;font-size:14px}
        .navbar .btn-nav{background:var(--gold);color:#000;border:none;border-radius:20px;padding:8px 18px;font-weight:bold;cursor:pointer;font-size:13px}
        .container{max-width:500px;margin:0 auto;padding:20px}
        .card{background:rgba(26,26,46,0.9);border-radius:15px;padding:20px;margin-bottom:15px;border:1px solid rgba(255,255,255,0.1)}
        .card h2{color:var(--gold);margin-bottom:10px;font-size:18px}
        .card .price{font-size:32px;font-weight:bold;color:var(--gold)}
        .card .duration{color:#aaa;margin:5px 0}
        .card ul{list-style:none;margin:10px 0}
        .card ul li{padding:4px 0;color:#ccc;font-size:14px}
        .btn-card{display:block;width:100%;padding:14px;border:none;border-radius:10px;font-size:16px;font-weight:bold;cursor:pointer;text-align:center;margin-top:10px}
        .btn-card:disabled{opacity:0.5}
        .btn-green{background:#00cc00;color:#fff}
        .btn-gold{background:#FFD700;color:#000}
        .btn-blue{background:#0088cc;color:#fff}
        .btn-purple{background:#9933ff;color:#fff}
        .btn-recharge{background:#00ff88;color:#000;font-size:18px;padding:18px}
        .badge{padding:3px 10px;border-radius:20px;font-size:11px;font-weight:bold}
        .badge-free{background:#00cc00;color:#fff}
        .badge-vip{background:var(--gold);color:#000}
        .badge-hot{background:#ff6600;color:#fff;animation:pulse 1s infinite}
        @keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}
        .tabs{display:flex;margin-bottom:15px;border-radius:10px;overflow:hidden}
        .tab{flex:1;text-align:center;padding:12px;background:rgba(26,26,46,0.9);border:1px solid rgba(255,255,255,0.1);cursor:pointer;font-weight:bold;color:#aaa}
        .tab.active{background:var(--gold);color:#000}
        .hidden{display:none!important}
        .modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:1000;justify-content:center;align-items:center}
        .modal.active{display:flex}
        .modal-content{background:rgba(26,26,46,0.98);border-radius:15px;padding:25px;width:90%;max-width:420px;text-align:center;border:1px solid var(--gold)}
        .modal-content h3{color:var(--gold);margin-bottom:15px}
        .modal-content input,.modal-content select{width:100%;padding:12px;margin:8px 0;border-radius:8px;border:1px solid #333;background:#0f0f1f;color:#fff;font-size:14px}
        .close-btn{float:right;color:var(--gold);font-size:24px;cursor:pointer;background:none;border:none}
        .key-display{font-size:14px;color:var(--green);font-family:monospace;background:#000;padding:15px;border-radius:8px;margin:10px 0;word-break:break-all;border:1px dashed var(--green)}
        .copy-btn{background:var(--gold);color:#000;border:none;padding:12px;border-radius:8px;cursor:pointer;font-weight:bold;width:100%}
        table{width:100%;border-collapse:collapse;font-size:13px}
        th{background:var(--gold);color:#000;padding:10px}
        td{padding:10px;border-bottom:1px solid rgba(255,255,255,0.1);text-align:center}
        .key-link{color:var(--green);cursor:pointer;text-decoration:underline}
        .loading{display:inline-block;width:30px;height:30px;border:3px solid #333;border-top:3px solid var(--gold);border-radius:50%;animation:spin 1s linear infinite}
        @keyframes spin{0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}
        .alert-box{background:rgba(255,0,0,0.1);border:1px solid var(--red);border-radius:10px;padding:15px;margin:10px 0;color:var(--red)}
        .success-box{background:rgba(0,255,0,0.1);border:1px solid var(--green);border-radius:10px;padding:15px;margin:10px 0;color:var(--green)}
        .toast{position:fixed;top:20px;right:20px;z-index:10000;padding:15px 20px;border-radius:10px;color:#fff;font-weight:bold;animation:slideIn 0.5s}
        .toast-success{background:#00cc00}.toast-error{background:#ff4444}
        @keyframes slideIn{from{transform:translateX(100%)}to{transform:translateX(0)}}
    </style>
</head>
<body>
<div class="navbar">
    <div class="logo">QANH SHOP</div>
    <div class="user-info">
        <div class="balance" id="balanceDisplay">0d</div>
        <button class="btn-nav" id="authBtn" onclick="showAuthModal()">DANG NHAP</button>
    </div>
</div>
<div class="container">
    <div class="card" style="border-color:#00ff88">
        <h2>NAP TIEN</h2>
        <select id="rcType"><option value="">Chon nha mang</option><option value="VIETTEL">Viettel</option><option value="MOBIFONE">Mobifone</option><option value="VINAPHONE">Vinaphone</option></select>
        <select id="rcAmount"><option value="">Chon menh gia</option><option value="10000">10k</option><option value="20000">20k</option><option value="50000">50k</option><option value="100000">100k</option><option value="200000">200k</option><option value="500000">500k</option></select>
        <input type="text" id="rcPin" placeholder="Ma the">
        <input type="text" id="rcSerial" placeholder="Serial">
        <button class="btn-card btn-recharge" onclick="recharge()">NAP NGAY</button>
        <div id="rcResult"></div>
    </div>
    <div class="card" style="border-color:#00cc00">
        <h2>KEY FREE <span class="badge badge-free">MIEN PHI</span></h2>
        <div class="price">0d</div><div class="duration">1 ngay</div>
        <button class="btn-card btn-green" id="btnFreeKey" onclick="getFreeKey()">NHAN KEY FREE</button>
        <div id="verifyStatus"></div>
    </div>
    <div class="card" style="border-color:#9933ff">
        <h2>KEY 1 TUAN <span class="badge badge-hot">HOT</span></h2>
        <div class="price">50k</div><div class="duration">7 ngay</div>
        <button class="btn-card btn-purple" onclick="buyKey('week')">MUA NGAY</button>
    </div>
    <div class="card" style="border-color:#0088cc">
        <h2>KEY 1 THANG <span class="badge badge-vip">VIP</span></h2>
        <div class="price">150k</div><div class="duration">30 ngay</div>
        <button class="btn-card btn-blue" onclick="buyKey('month')">MUA NGAY</button>
    </div>
    <div class="card" style="border-color:#FFD700">
        <h2>KEY VINH VIEN <span class="badge badge-vip">PREMIUM</span></h2>
        <div class="price">250k</div><div class="duration">Khong gioi han</div>
        <button class="btn-card btn-gold" onclick="buyKey('forever')">MUA NGAY</button>
    </div>
</div>
<div class="modal" id="authModal"><div class="modal-content">
    <span class="close-btn" onclick="document.getElementById('authModal').classList.remove('active')">x</span>
    <h3>DANG NHAP / DANG KY</h3>
    <input type="text" id="authEmail" placeholder="Email">
    <input type="password" id="authPassword" placeholder="Mat khau">
    <button class="btn-card btn-gold" onclick="doAuth()">DANG NHAP</button>
</div></div>
<div class="modal" id="keyModal"><div class="modal-content">
    <span class="close-btn" onclick="document.getElementById('keyModal').classList.remove('active')">x</span>
    <h3 style="color:#0f0">THANH CONG!</h3>
    <p id="keyMessage"></p>
    <div class="key-display" id="keyDisplay"></div>
    <button class="copy-btn" onclick="copyKey()">COPY KEY</button>
</div></div>
<script>
var API=window.location.origin;
var PARTNER_ID='"""+PARTNER_ID+"""';
var PARTNER_KEY='"""+PARTNER_KEY+"""';
var ADMIN_EMAIL='admin@qanhshop.com';
var ADMIN_PASS='QanhAdmin@2025#Secret!';
var currentUser=null;
var userKeys=[];
var userRecharges=[];
var allUsers=[];
var keyPrices={week:50000,month:150000,forever:250000};
var keyNames={week:'KEY 1 TUAN',month:'KEY 1 THANG',forever:'KEY VINH VIEN'};
var keyDurations={week:'7 NGAY',month:'30 NGAY',forever:'VINH VIEN'};
var verifyInterval=null;
var currentVerifyToken=null;
try{
    currentUser=JSON.parse(localStorage.getItem('quanh_user'))||null;
    userKeys=JSON.parse(localStorage.getItem('quanh_keys'))||[];
    userRecharges=JSON.parse(localStorage.getItem('quanh_recharges'))||[];
    allUsers=JSON.parse(localStorage.getItem('quanh_all_users'))||[];
}catch(e){currentUser=null;userKeys=[];userRecharges=[];allUsers=[];}

function saveAll(){
    try{
        if(currentUser)localStorage.setItem('quanh_user',JSON.stringify(currentUser));
        localStorage.setItem('quanh_keys',JSON.stringify(userKeys));
        localStorage.setItem('quanh_recharges',JSON.stringify(userRecharges));
        localStorage.setItem('quanh_all_users',JSON.stringify(allUsers));
    }catch(e){}
}

function updateUI(){
    if(!currentUser){document.getElementById('authBtn').innerText='DANG NHAP';document.getElementById('balanceDisplay').innerText='0d';}
    else{document.getElementById('authBtn').innerText=currentUser.name||'User';document.getElementById('balanceDisplay').innerText=(currentUser.balance||0).toLocaleString()+'d';}
}

function showToast(msg,type){
    var t=document.createElement('div');
    t.className='toast toast-'+(type||'success');
    t.innerText=msg;
    document.body.appendChild(t);
    setTimeout(function(){t.remove()},2500);
}

function showAuthModal(){
    if(currentUser){if(confirm('Dang xuat?')){currentUser=null;localStorage.removeItem('quanh_user');updateUI();}return;}
    document.getElementById('authModal').classList.add('active');
}

function doAuth(){
    var email=document.getElementById('authEmail').value.trim();
    var pass=document.getElementById('authPassword').value.trim();
    if(!email||!pass){showToast('Dien day du!','error');return;}
    if(email===ADMIN_EMAIL&&pass===ADMIN_PASS){
        currentUser={name:'Admin',email:ADMIN_EMAIL,password:pass,balance:999999999,isAdmin:true};
        saveAll();document.getElementById('authModal').classList.remove('active');updateUI();showToast('Admin!');return;
    }
    var found=false;
    for(var i=0;i<allUsers.length;i++){if(allUsers[i].email===email){if(allUsers[i].password!==pass){showToast('Sai mat khau!','error');return;}currentUser=allUsers[i];found=true;break;}}
    if(!found){currentUser={name:email.split('@')[0],email:email,password:pass,balance:0,isAdmin:false};allUsers.push(currentUser);}
    saveAll();document.getElementById('authModal').classList.remove('active');updateUI();showToast('Thanh cong!');
}

function recharge(){
    if(!currentUser){showToast('Dang nhap!','error');showAuthModal();return;}
    var telco=document.getElementById('rcType').value;
    var amount=parseInt(document.getElementById('rcAmount').value);
    var pin=document.getElementById('rcPin').value.trim();
    var serial=document.getElementById('rcSerial').value.trim();
    if(!telco||!amount||!pin||!serial){showToast('Dien day du!','error');return;}
    document.getElementById('rcResult').innerHTML='<div class="loading"></div>';
    var xhr=new XMLHttpRequest();
    xhr.open('POST','https://api.shoppay.vn/card/charge',true);
    xhr.setRequestHeader('Content-Type','application/json');
    xhr.onload=function(){
        try{
            var data=JSON.parse(xhr.responseText);
            if(data.status===1){
                currentUser.balance=(currentUser.balance||0)+amount;
                for(var i=0;i<allUsers.length;i++){if(allUsers[i].email===currentUser.email){allUsers[i].balance=currentUser.balance;break;}}
                userRecharges.unshift({type:telco,amount:amount,time:new Date().toLocaleString(),status:'OK'});
                saveAll();updateUI();
                document.getElementById('rcResult').innerHTML='<div class="success-box">Nap thanh cong '+amount.toLocaleString()+'d!</div>';
                document.getElementById('rcPin').value='';document.getElementById('rcSerial').value='';
            }else{document.getElementById('rcResult').innerHTML='<div class="alert-box">'+(data.message||'Loi')+'</div>';}
        }catch(e){document.getElementById('rcResult').innerHTML='<div class="alert-box">Loi!</div>';}
    };
    xhr.onerror=function(){document.getElementById('rcResult').innerHTML='<div class="alert-box">Loi ket noi!</div>';};
    xhr.send(JSON.stringify({partner_id:PARTNER_ID,partner_key:PARTNER_KEY,telco:telco,amount:amount,pin:pin,serial:serial}));
}

function buyKey(type){
    if(!currentUser){showToast('Dang nhap!','error');showAuthModal();return;}
    var price=keyPrices[type];
    if((currentUser.balance||0)<price){showToast('Khong du!','error');return;}
    if(!confirm('Mua '+keyNames[type]+' gia '+price.toLocaleString()+'d?'))return;
    currentUser.balance-=price;
    for(var i=0;i<allUsers.length;i++){if(allUsers[i].email===currentUser.email){allUsers[i].balance=currentUser.balance;break;}}
    saveAll();updateUI();
    var xhr=new XMLHttpRequest();
    xhr.open('GET',API+'/api/buy-key?type='+type,true);
    xhr.onload=function(){
        try{
            var data=JSON.parse(xhr.responseText);
            if(data.status==='success'){
                userKeys.unshift({key:data.key,type:keyNames[type],duration:keyDurations[type],time:new Date().toLocaleString()});
                saveAll();
                document.getElementById('keyDisplay').innerText=data.key;
                document.getElementById('keyMessage').innerText='Mua '+keyNames[type]+' thanh cong!';
                document.getElementById('keyModal').classList.add('active');
                showToast('Mua thanh cong!');
            }else{currentUser.balance+=price;saveAll();updateUI();showToast('Loi!','error');}
        }catch(e){currentUser.balance+=price;saveAll();updateUI();}
    };
    xhr.send();
}

function getFreeKey(){
    if(!currentUser){showToast('Dang nhap!','error');showAuthModal();return;}
    var btn=document.getElementById('btnFreeKey');
    btn.disabled=true;btn.innerText='Dang tao...';
    var xhr=new XMLHttpRequest();
    xhr.open('GET',API+'/api/get-free-link?email='+encodeURIComponent(currentUser.email),true);
    xhr.onload=function(){
        try{
            var data=JSON.parse(xhr.responseText);
            if(data.status==='success'&&data.link4m){
                currentVerifyToken=data.token;
                document.getElementById('verifyStatus').innerHTML='<div class="success-box">HOAN THANH NHIEM VU DE NHAN KEY!</div>';
                window.open(data.link4m,'_blank');
                startVerifyCheck();
            }else if(data.status==='error'){
                document.getElementById('verifyStatus').innerHTML='<div class="alert-box">'+data.message+'</div>';
            }
        }catch(e){}
        btn.disabled=false;btn.innerText='NHAN KEY FREE';
    };
    xhr.send();
}

function startVerifyCheck(){
    var count=0;
    if(verifyInterval)clearInterval(verifyInterval);
    verifyInterval=setInterval(function(){
        count++;
        var xhr=new XMLHttpRequest();
        xhr.open('GET',API+'/api/check-verify?token='+currentVerifyToken,true);
        xhr.onload=function(){
            try{
                var data=JSON.parse(xhr.responseText);
                if(data.status==='verified'&&data.key){
                    clearInterval(verifyInterval);
                    document.getElementById('verifyStatus').innerHTML='<div class="success-box">DA HOAN THANH!</div>';
                    userKeys.unshift({key:data.key,type:'FREE (Verified)',duration:'1 NGAY',time:new Date().toLocaleString()});
                    saveAll();
                    document.getElementById('keyDisplay').innerText=data.key;
                    document.getElementById('keyMessage').innerText='Key Free da xac thuc!';
                    document.getElementById('keyModal').classList.add('active');
                }else if(count>=60){clearInterval(verifyInterval);}
            }catch(e){}
        };
        xhr.send();
    },5000);
}

function copyKey(){
    var key=document.getElementById('keyDisplay').innerText;
    navigator.clipboard.writeText(key).then(function(){showToast('Da copy!');}).catch(function(){prompt('Copy:',key);});
}

updateUI();
</script>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/buy-key')
def api_buy_key():
    key_type = request.args.get('type', 'week')
    key = generate_key()
    bot_cmds = {'week': '1w', 'month': 'vip 1thang', 'forever': 'vip vinhvien'}
    try:
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                     json={'chat_id': CHAT_ID, 'text': '/taokey ' + bot_cmds.get(key_type, '1w')}, timeout=5)
    except: pass
    if key_type == 'week':
        data.setdefault("licenses", {})[key] = {"created_by": OWNER_ID, "expire_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")}
    elif key_type == 'month':
        data.setdefault("licenses", {})[key] = {"created_by": OWNER_ID, "expire_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")}
    else:
        data.setdefault("licenses", {})[key] = {"created_by": OWNER_ID, "expire_date": None}
    data.setdefault("keys_history", []).append({"key": key, "type": key_type, "time": datetime.now().isoformat()})
    save_data(data)
    return jsonify({"status": "success", "key": key})

@app.route('/api/get-free-link')
def api_get_free_link():
    email = request.args.get('email', 'user')
    token = secrets.token_hex(16)
    callback_url = f"https://shopvip-zykg.onrender.com/verify/{token}"
    try:
        api_url = f"https://link4m.co/api-shorten/v2?api={LINK4M_API_KEY}&url={callback_url}"
        res = requests.get(api_url, timeout=10)
        link_data = res.json()
        if link_data.get('status') == 'success':
            pending_verify[token] = {"email": email, "time": time(), "verified": False, "key": None}
            return jsonify({"status": "success", "link4m": link_data.get('shortenedUrl'), "token": token})
        return jsonify({"status": "error", "message": "Loi tao link link4m"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/verify/<token>')
def verify_page(token):
    if token not in pending_verify:
        return "<h1>Link khong hop le</h1>", 404
    key = generate_key()
    today = datetime.now().strftime("%Y-%m-%d")
    data.setdefault("free_keys", {})[key] = {"created_by": OWNER_ID, "expire": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"), "email": pending_verify[token]["email"], "date": today, "verified": True}
    data.setdefault("keys_history", []).append({"key": key, "type": "free_verified", "time": datetime.now().isoformat()})
    save_data(data)
    try:
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', json={'chat_id': CHAT_ID, 'text': '/taokey free 1ngay'}, timeout=5)
    except: pass
    pending_verify[token]["verified"] = True
    pending_verify[token]["key"] = key
    return '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Xac Thuc</title><style>body{background:#0f0c29;color:#fff;text-align:center;padding:50px;font-family:Arial}h2{color:#0f0}.key{color:#0f0;background:#000;padding:15px;border-radius:10px;border:1px dashed #0f0;font-family:monospace;font-size:18px}button{background:#0f0;color:#000;padding:12px 25px;border:none;border-radius:8px;font-weight:bold;font-size:16px;margin:10px}</style></head><body><h2>HOAN THANH NHIEM VU!</h2><div class="key">'+key+'</div><button onclick="navigator.clipboard.writeText(\''+key+'\')">COPY KEY</button><p style="color:#aaa">Dung /kichhoat '+key.substring(0,20)+'... trong bot</p></body></html>'

@app.route('/api/check-verify')
def api_check_verify():
    token = request.args.get('token', '')
    if token in pending_verify and pending_verify[token].get("verified"):
        return jsonify({"status": "verified", "key": pending_verify[token]["key"]})
    return jsonify({"status": "pending"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)            json.dump(d, f, ensure_ascii=False, indent=2)
    except: pass

data = load_data()

def generate_key():
    chars = string.ascii_uppercase + string.digits
    def rand(l): return ''.join(secrets.choice(chars) for _ in range(l))
    return f"QANH-{rand(10)}-{rand(10)}-{rand(10)}-{rand(5)}"

# ===== HTML =====
HTML = r'''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QANH SHOP - Key Uy Tín</title>
    <style>
        :root{--gold:#FFD700;--green:#00ff00;--red:#ff4444;--blue:#0088ff;--purple:#9933ff}
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Arial,sans-serif;color:#fff;min-height:100vh;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e)}
        .navbar{background:rgba(26,26,46,0.95);padding:15px 20px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:100;border-bottom:2px solid var(--gold);flex-wrap:wrap;gap:10px}
        .navbar .logo{font-size:22px;font-weight:bold;color:var(--gold)}
        .navbar .user-info{display:flex;align-items:center;gap:10px}
        .navbar .balance{background:rgba(0,0,0,0.5);border:1px solid var(--gold);border-radius:20px;padding:8px 15px;color:var(--gold);font-weight:bold;cursor:pointer;font-size:14px}
        .navbar .btn-nav{background:var(--gold);color:#000;border:none;border-radius:20px;padding:8px 18px;font-weight:bold;cursor:pointer;font-size:13px}
        .container{max-width:500px;margin:0 auto;padding:20px}
        .card{background:rgba(26,26,46,0.9);border-radius:15px;padding:20px;margin-bottom:15px;border:1px solid rgba(255,255,255,0.1)}
        .card h2{color:var(--gold);margin-bottom:10px;font-size:18px}
        .card .price{font-size:32px;font-weight:bold;color:var(--gold)}
        .card .duration{color:#aaa;margin:5px 0}
        .card ul{list-style:none;margin:10px 0}
        .card ul li{padding:4px 0;color:#ccc;font-size:14px}
        .card ul li::before{content:"✓ ";color:var(--green)}
        .btn-card{display:block;width:100%;padding:14px;border:none;border-radius:10px;font-size:16px;font-weight:bold;cursor:pointer;text-align:center;margin-top:10px}
        .btn-card:disabled{opacity:0.5;cursor:not-allowed}
        .btn-green{background:linear-gradient(135deg,#00cc00,#008800);color:#fff}
        .btn-gold{background:linear-gradient(135deg,#FFD700,#FFA500);color:#000}
        .btn-blue{background:linear-gradient(135deg,#0088cc,#004488);color:#fff}
        .btn-purple{background:linear-gradient(135deg,#9933ff,#6600cc);color:#fff}
        .btn-recharge{background:linear-gradient(135deg,#00ff88,#00cc66);color:#000;font-size:18px;padding:18px}
        .badge{padding:3px 10px;border-radius:20px;font-size:11px;font-weight:bold}
        .badge-free{background:#00cc00;color:#fff}
        .badge-vip{background:var(--gold);color:#000}
        .badge-hot{background:#ff6600;color:#fff;animation:pulse 1s infinite}
        @keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}
        .tabs{display:flex;margin-bottom:15px;border-radius:10px;overflow:hidden}
        .tab{flex:1;text-align:center;padding:12px;background:rgba(26,26,46,0.9);border:1px solid rgba(255,255,255,0.1);cursor:pointer;font-weight:bold;color:#aaa}
        .tab.active{background:var(--gold);color:#000}
        .hidden{display:none!important}
        .modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:1000;justify-content:center;align-items:center}
        .modal.active{display:flex}
        .modal-content{background:rgba(26,26,46,0.98);border-radius:15px;padding:25px;width:90%;max-width:420px;text-align:center;max-height:85vh;overflow-y:auto;border:1px solid var(--gold)}
        .modal-content h3{color:var(--gold);margin-bottom:15px;font-size:20px}
        .modal-content input,.modal-content select{width:100%;padding:12px;margin:8px 0;border-radius:8px;border:1px solid #333;background:#0f0f1f;color:#fff;font-size:14px}
        .modal-content .close-btn{float:right;color:var(--gold);font-size:24px;cursor:pointer;background:none;border:none}
        .key-display{font-size:14px;color:var(--green);font-family:monospace;background:#000;padding:15px;border-radius:8px;margin:10px 0;word-break:break-all;border:1px dashed var(--green)}
        .copy-btn{background:var(--gold);color:#000;border:none;padding:12px;border-radius:8px;cursor:pointer;font-weight:bold;width:100%}
        table{width:100%;border-collapse:collapse;font-size:13px}
        th{background:var(--gold);color:#000;padding:10px}
        td{padding:10px;border-bottom:1px solid rgba(255,255,255,0.1);text-align:center}
        .key-link{color:var(--green);cursor:pointer;text-decoration:underline}
        .loading-spinner{display:inline-block;width:30px;height:30px;border:3px solid #333;border-top:3px solid var(--gold);border-radius:50%;animation:spin 1s linear infinite}
        @keyframes spin{0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}
        .alert-box{background:rgba(255,0,0,0.1);border:1px solid var(--red);border-radius:10px;padding:15px;margin:10px 0;color:var(--red)}
        .success-box{background:rgba(0,255,0,0.1);border:1px solid var(--green);border-radius:10px;padding:15px;margin:10px 0;color:var(--green)}
        .info-text{color:#888;font-size:12px;margin-top:10px}
        .toast{position:fixed;top:20px;right:20px;z-index:10000;padding:15px 20px;border-radius:10px;color:#fff;font-weight:bold;max-width:350px;animation:slideIn 0.5s}
        .toast-success{background:#00cc00}.toast-error{background:#ff4444}
        @keyframes slideIn{from{transform:translateX(100%)}to{transform:translateX(0)}}
        .verify-box{background:rgba(255,215,0,0.1);border:2px solid var(--gold);border-radius:10px;padding:15px;margin:10px 0;text-align:center}
        .verify-box .waiting{color:var(--gold);font-size:16px;font-weight:bold}
    </style>
</head>
<body>
    <div class="navbar">
        <div class="logo">QANH SHOP</div>
        <div class="user-info">
            <div class="balance" id="balanceDisplay" onclick="document.getElementById('rechargeSection').scrollIntoView({behavior:'smooth'})">0d</div>
            <button class="btn-nav" id="authBtn" onclick="showAuthModal()">DANG NHAP</button>
        </div>
    </div>

    <div class="container">
        <div class="tabs">
            <div class="tab active" onclick="switchTab('shop')">SHOP KEY</div>
            <div class="tab" onclick="switchTab('history')">LICH SU</div>
        </div>

        <div id="shopTab">
            <div class="card" style="border-color:#00ff88;border-width:2px" id="rechargeSection">
                <h2>NAP TIEN</h2>
                <select id="rcType"><option value="">Chon nha mang</option><option value="VIETTEL">Viettel</option><option value="MOBIFONE">Mobifone</option><option value="VINAPHONE">Vinaphone</option></select>
                <select id="rcAmount"><option value="">Chon menh gia</option><option value="10000">10,000d</option><option value="20000">20,000d</option><option value="50000">50,000d</option><option value="100000">100,000d</option><option value="200000">200,000d</option><option value="500000">500,000d</option></select>
                <input type="text" id="rcPin" placeholder="Ma the...">
                <input type="text" id="rcSerial" placeholder="Serial...">
                <button class="btn-card btn-recharge" id="btnRecharge" onclick="recharge()">NAP NGAY</button>
                <div id="rcResult" style="margin-top:10px"></div>
            </div>

            <div class="card" style="border-color:#00cc00">
                <h2>KEY FREE <span class="badge badge-free">MIEN PHI</span></h2>
                <div class="price">0d</div><div class="duration">1 ngay</div>
                <ul><li>Dung thu mien phi</li></ul>
                <button class="btn-card btn-green" id="btnFreeKey" onclick="getFreeKey()">NHAN KEY FREE</button>
                <div id="verifyStatus" style="margin-top:10px"></div>
                <p class="info-text">HOAN THANH NHIEM VU tren link4m de nhan key</p>
            </div>

            <div class="card" style="border-color:#9933ff">
                <h2>KEY 1 TUAN <span class="badge badge-hot">HOT</span></h2>
                <div class="price">50,000d</div><div class="duration">7 ngay</div>
                <ul><li>VIP 7 ngay</li></ul>
                <button class="btn-card btn-purple" id="btnWeek" onclick="buyKey('week')">MUA NGAY</button>
            </div>

            <div class="card" style="border-color:#0088cc">
                <h2>KEY 1 THANG <span class="badge badge-vip">VIP</span></h2>
                <div class="price">150,000d</div><div class="duration">30 ngay</div>
                <ul><li>VIP 30 ngay</li></ul>
                <button class="btn-card btn-blue" id="btnMonth" onclick="buyKey('month')">MUA NGAY</button>
            </div>

            <div class="card" style="border-color:#FFD700">
                <h2>KEY VINH VIEN <span class="badge badge-vip">PREMIUM</span></h2>
                <div class="price">250,000d</div><div class="duration">Khong gioi han</div>
                <ul><li>Premium tron doi</li></ul>
                <button class="btn-card btn-gold" id="btnForever" onclick="buyKey('forever')">MUA NGAY</button>
            </div>
        </div>

        <div id="historyTab" class="hidden">
            <div class="card"><h2>LICH SU KEY</h2><table><thead><tr><th>Key</th><th>Loai</th><th>Han</th></tr></thead><tbody id="keyHistory"><tr><td colspan="3">Chua co</td></tr></tbody></table></div>
            <div class="card"><h2>LICH SU NAP</h2><table><thead><tr><th>Loai</th><th>Tien</th><th>TT</th></tr></thead><tbody id="rechargeHistory"><tr><td colspan="3">Chua co</td></tr></tbody></table></div>
        </div>
    </div>

    <div class="modal" id="authModal"><div class="modal-content">
        <span class="close-btn" onclick="document.getElementById('authModal').classList.remove('active')">x</span>
        <h3>DANG NHAP / DANG KY</h3>
        <input type="text" id="authEmail" placeholder="Email">
        <input type="password" id="authPassword" placeholder="Mat khau">
        <button class="btn-card btn-gold" id="btnAuth" onclick="doAuth()">DANG NHAP</button>
        <p class="info-text">Chua co tai khoan? Tu dong dang ky!</p>
    </div></div>

    <div class="modal" id="keyModal"><div class="modal-content">
        <span class="close-btn" onclick="document.getElementById('keyModal').classList.remove('active')">x</span>
        <h3 style="color:#0f0">THANH CONG!</h3>
        <p id="keyMessage"></p>
        <div class="key-display" id="keyDisplay"></div>
        <button class="copy-btn" id="btnCopy" onclick="copyKey()">COPY KEY</button>
        <p class="info-text">Dung /kichhoat KEY trong bot Telegram</p>
    </div></div>

<script>
var API = window.location.origin;
var PARTNER_ID = "''' + PARTNER_ID + '''";
var PARTNER_KEY = "''' + PARTNER_KEY + '''";
var ADMIN_EMAIL = "admin@qanhshop.com";
var ADMIN_PASS = "QanhAdmin@2025#Secret!";
var currentUser = null;
var userKeys = [];
var userRecharges = [];
var allUsers = [];
var keyPrices = {week: 50000, month: 150000, forever: 250000};
var keyNames = {week: 'KEY 1 TUAN', month: 'KEY 1 THANG', forever: 'KEY VINH VIEN'};
var keyDurations = {week: '7 NGAY', month: '30 NGAY', forever: 'VINH VIEN'};
var verifyInterval = null;
var currentVerifyToken = null;

try {
    currentUser = JSON.parse(localStorage.getItem('quanh_user')) || null;
    userKeys = JSON.parse(localStorage.getItem('quanh_keys')) || [];
    userRecharges = JSON.parse(localStorage.getItem('quanh_recharges')) || [];
    allUsers = JSON.parse(localStorage.getItem('quanh_all_users')) || [];
} catch(e) { currentUser = null; userKeys = []; userRecharges = []; allUsers = []; }

function saveAll() {
    try {
        if (currentUser) localStorage.setItem('quanh_user', JSON.stringify(currentUser));
        localStorage.setItem('quanh_keys', JSON.stringify(userKeys));
        localStorage.setItem('quanh_recharges', JSON.stringify(userRecharges));
        localStorage.setItem('quanh_all_users', JSON.stringify(allUsers));
    } catch(e) {}
}

function updateUI() {
    if (!currentUser) {
        document.getElementById('authBtn').innerText = 'DANG NHAP';
        document.getElementById('balanceDisplay').innerText = '0d';
    } else {
        document.getElementById('authBtn').innerText = currentUser.name || 'User';
        document.getElementById('balanceDisplay').innerText = (currentUser.balance || 0).toLocaleString() + 'd';
    }
    updateHistory();
}

function showToast(msg, type) {
    var t = document.createElement('div');
    t.className = 'toast toast-' + (type || 'success');
    t.innerText = msg;
    document.body.appendChild(t);
    setTimeout(function() { t.style.opacity = '0'; t.style.transition = 'opacity 0.5s'; setTimeout(function() { t.remove(); }, 500); }, 2500);
}

function switchTab(tab) {
    document.querySelectorAll('.tab')[0].classList.toggle('active', tab === 'shop');
    document.querySelectorAll('.tab')[1].classList.toggle('active', tab === 'history');
    document.getElementById('shopTab').classList.toggle('hidden', tab !== 'shop');
    document.getElementById('historyTab').classList.toggle('hidden', tab !== 'history');
    if (tab === 'history') updateHistory();
}

function showAuthModal() {
    if (currentUser) {
        if (confirm('Dang xuat?')) { currentUser = null; localStorage.removeItem('quanh_user'); updateUI(); showToast('Da dang xuat!'); }
        return;
    }
    document.getElementById('authEmail').value = '';
    document.getElementById('authPassword').value = '';
    document.getElementById('authModal').classList.add('active');
}

function doAuth() {
    var email = document.getElementById('authEmail').value.trim();
    var pass = document.getElementById('authPassword').value.trim();
    if (!email || !pass) { showToast('Dien day du!', 'error'); return; }
    
    if (email === ADMIN_EMAIL && pass === ADMIN_PASS) {
        currentUser = { name: 'Admin', email: ADMIN_EMAIL, password: pass, balance: 999999999, isAdmin: true };
        saveAll();
        document.getElementById('authModal').classList.remove('active');
        updateUI();
        showToast('Admin!');
        return;
    }
    
    var found = false;
    for (var i = 0; i < allUsers.length; i++) {
        if (allUsers[i].email === email) {
            if (allUsers[i].password !== pass) { showToast('Sai mat khau!', 'error'); return; }
            currentUser = allUsers[i];
            found = true;
            break;
        }
    }
    if (!found) {
        currentUser = { name: email.split('@')[0], email: email, password: pass, balance: 0, isAdmin: false };
        allUsers.push(currentUser);
    }
    saveAll();
    document.getElementById('authModal').classList.remove('active');
    updateUI();
    showToast('Thanh cong!');
}

// ===== NẠP TIỀN =====
function recharge() {
    if (!currentUser) { showToast('Dang nhap!', 'error'); showAuthModal(); return; }
    var telco = document.getElementById('rcType').value;
    var amount = parseInt(document.getElementById('rcAmount').value);
    var pin = document.getElementById('rcPin').value.trim();
    var serial = document.getElementById('rcSerial').value.trim();
    if (!telco || !amount || !pin || !serial) { showToast('Dien day du!', 'error'); return; }
    
    document.getElementById('rcResult').innerHTML = '<div class="loading-spinner"></div>';
    
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://api.shoppay.vn/card/charge', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        try {
            var data = JSON.parse(xhr.responseText);
            if (data.status === 1) {
                currentUser.balance = (currentUser.balance || 0) + amount;
                for (var i = 0; i < allUsers.length; i++) { if (allUsers[i].email === currentUser.email) { allUsers[i].balance = currentUser.balance; break; } }
                userRecharges.unshift({type: telco, amount: amount, time: new Date().toLocaleString(), status: 'OK'});
                saveAll();
                updateUI();
                document.getElementById('rcResult').innerHTML = '<div class="success-box">Nap thanh cong ' + amount.toLocaleString() + 'd!</div>';
                document.getElementById('rcPin').value = ''; document.getElementById('rcSerial').value = '';
            } else {
                document.getElementById('rcResult').innerHTML = '<div class="alert-box">' + (data.message || 'Loi') + '</div>';
            }
        } catch(e) { document.getElementById('rcResult').innerHTML = '<div class="alert-box">Loi!</div>'; }
    };
    xhr.onerror = function() { document.getElementById('rcResult').innerHTML = '<div class="alert-box">Loi ket noi!</div>'; };
    xhr.send(JSON.stringify({partner_id: PARTNER_ID, partner_key: PARTNER_KEY, telco: telco, amount: amount, pin: pin, serial: serial}));
}

// ===== MUA KEY =====
function buyKey(type) {
    if (!currentUser) { showToast('Dang nhap!', 'error'); showAuthModal(); return; }
    var price = keyPrices[type];
    if ((currentUser.balance || 0) < price) { showToast('Khong du! Can ' + price.toLocaleString() + 'd', 'error'); return; }
    if (!confirm('Mua ' + keyNames[type] + ' gia ' + price.toLocaleString() + 'd?')) return;
    
    currentUser.balance -= price;
    for (var i = 0; i < allUsers.length; i++) { if (allUsers[i].email === currentUser.email) { allUsers[i].balance = currentUser.balance; break; } }
    saveAll();
    updateUI();
    
    var xhr = new XMLHttpRequest();
    xhr.open('GET', API + '/api/buy-key?type=' + type, true);
    xhr.onload = function() {
        try {
            var data = JSON.parse(xhr.responseText);
            if (data.status === 'success') {
                userKeys.unshift({key: data.key, type: keyNames[type], duration: keyDurations[type], time: new Date().toLocaleString()});
                saveAll();
                document.getElementById('keyDisplay').innerText = data.key;
                document.getElementById('keyMessage').innerText = 'Mua ' + keyNames[type] + ' thanh cong!';
                document.getElementById('keyModal').classList.add('active');
                updateHistory();
                showToast('Mua thanh cong!');
            } else {
                currentUser.balance += price;
                saveAll();
                updateUI();
                showToast('Loi!', 'error');
            }
        } catch(e) { currentUser.balance += price; saveAll(); updateUI(); }
    };
    xhr.send();
}

// ===== KEY FREE + LINK4M =====
function getFreeKey() {
    if (!currentUser) { showToast('Dang nhap!', 'error'); showAuthModal(); return; }
    var btn = document.getElementById('btnFreeKey');
    btn.disabled = true; btn.innerText = 'Dang tao link...';
    
    var xhr = new XMLHttpRequest();
    xhr.open('GET', API + '/api/get-free-link?email=' + encodeURIComponent(currentUser.email), true);
    xhr.onload = function() {
        try {
            var data = JSON.parse(xhr.responseText);
            if (data.status === 'success' && data.link4m) {
                currentVerifyToken = data.token;
                document.getElementById('verifyStatus').innerHTML = '<div class="verify-box"><p class="waiting">HOAN THANH NHIEM VU DE NHAN KEY!</p><p style="color:#aaa;font-size:12px">Vui long xem het noi dung tren link4m</p></div>';
                window.open(data.link4m, '_blank');
                startVerifyCheck();
            } else if (data.status === 'success' && data.key) {
                userKeys.unshift({key: data.key, type: 'FREE', duration: '1 NGAY', time: new Date().toLocaleString()});
                saveAll();
                document.getElementById('keyDisplay').innerText = data.key;
                document.getElementById('keyMessage').innerText = 'Key Free cua ban!';
                document.getElementById('keyModal').classList.add('active');
                document.getElementById('verifyStatus').innerHTML = '';
                updateHistory();
            } else {
                document.getElementById('verifyStatus').innerHTML = '<div class="alert-box">' + (data.message || 'Loi') + '</div>';
            }
        } catch(e) { document.getElementById('verifyStatus').innerHTML = '<div class="alert-box">Loi ket noi!</div>'; }
        btn.disabled = false; btn.innerText = 'NHAN KEY FREE';
    };
    xhr.onerror = function() { btn.disabled = false; btn.innerText = 'NHAN KEY FREE'; };
    xhr.send();
}

function startVerifyCheck() {
    var count = 0;
    if (verifyInterval) clearInterval(verifyInterval);
    verifyInterval = setInterval(function() {
        count++;
        var xhr = new XMLHttpRequest();
        xhr.open('GET', API + '/api/check-verify?token=' + currentVerifyToken, true);
        xhr.onload = function() {
            try {
                var data = JSON.parse(xhr.responseText);
                if (data.status === 'verified' && data.key) {
                    clearInterval(verifyInterval);
                    document.getElementById('verifyStatus').innerHTML = '<div class="success-box">DA HOAN THANH NHIEM VU!</div>';
                    userKeys.unshift({key: data.key, type: 'FREE (Verified)', duration: '1 NGAY', time: new Date().toLocaleString()});
                    saveAll();
                    document.getElementById('keyDisplay').innerText = data.key;
                    document.getElementById('keyMessage').innerText = 'Key Free da xac thuc!';
                    document.getElementById('keyModal').classList.add('active');
                    updateHistory();
                } else if (count >= 60) {
                    clearInterval(verifyInterval);
                    document.getElementById('verifyStatus').innerHTML = '<div class="alert-box">Het thoi gian! Vui long thu lai.</div>';
                }
            } catch(e) {}
        };
        xhr.send();
    }, 5000);
}

function copyKey() {
    var key = document.getElementById('keyDisplay').innerText;
    navigator.clipboard.writeText(key).then(function() {
        showToast('Da copy! /kichhoat ' + key.substring(0, 20) + '...');
    }).catch(function() { prompt('Copy:', key); });
}

function updateHistory() {
    var kh = document.getElementById('keyHistory');
    if (userKeys.length === 0) { kh.innerHTML = '<tr><td colspan="3">Chua co</td></tr>'; return; }
    var h = '';
    for (var i = 0; i < userKeys.length; i++) {
        h += '<tr><td class="key-link" onclick="document.getElementById(\'keyDisplay\').innerText=\'' + userKeys[i].key + '\';document.getElementById(\'keyModal\').classList.add(\'active\')">' + userKeys[i].key.substring(0, 25) + '...</td><td>' + userKeys[i].type + '</td><td>' + userKeys[i].duration + '</td></tr>';
    }
    kh.innerHTML = h;
    
    var rh = document.getElementById('rechargeHistory');
    if (userRecharges.length === 0) { rh.innerHTML = '<tr><td colspan="3">Chua co</td></tr>'; return; }
    var h2 = '';
    for (var i = 0; i < userRecharges.length; i++) {
        h2 += '<tr><td>' + userRecharges[i].type + '</td><td>' + (userRecharges[i].amount || 0).toLocaleString() + 'd</td><td style="color:#0f0">' + userRecharges[i].status + '</td></tr>';
    }
    rh.innerHTML = h2;
}

updateUI();
</script>
</body>
</html>
'''

# ===== API ROUTES =====
pending_verify = {}  # token -> {email, time, verified, key}

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/buy-key')
def api_buy_key():
    key_type = request.args.get('type', 'week')
    key = generate_key()
    bot_cmds = {'week': '1w', 'month': 'vip 1thang', 'forever': 'vip vinhvien'}
    bot_cmd = bot_cmds.get(key_type, '1w')
    
    try:
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                     json={'chat_id': CHAT_ID, 'text': f'/taokey {bot_cmd}'}, timeout=5)
    except: pass
    
    today = (datetime.now() + timedelta(days=7 if key_type == 'week' else (30 if key_type == 'month' else 36500))).strftime("%Y-%m-%d")
    data.setdefault("licenses", {})[key] = {"created_by": OWNER_ID, "expire_date": None if key_type == 'forever' else today}
    data.setdefault("keys_history", []).append({"key": key, "type": key_type, "time": datetime.now().isoformat()})
    save_data(data)
    
    return jsonify({"status": "success", "key": key})

@app.route('/api/get-free-link')
def api_get_free_link():
    email = request.args.get('email', 'user')
    today = datetime.now().strftime("%Y-%m-%d")
    
    for k, v in data.get("free_keys", {}).items():
        if v.get("email") == email and v.get("date") == today:
            return jsonify({"status": "error", "message": "Hom nay da nhan key free roi!"})
    
    token = secrets.token_hex(16)
    callback_url = f"https://shopvip-zykg.onrender.com/verify/{token}"
    
    try:
        api_url = f"https://link4m.co/api-shorten/v2?api={LINK4M_API_KEY}&url={callback_url}"
        res = requests.get(api_url, timeout=10)
        link_data = res.json()
        
        if link_data.get('status') == 'success':
            pending_verify[token] = {"email": email, "time": time(), "verified": False, "key": None}
            return jsonify({"status": "success", "link4m": link_data.get('shortenedUrl'), "token": token})
        else:
            return jsonify({"status": "error", "message": "Loi tao link link4m!"})
    except Exception as e:
        return jsonify({"status": "error", "message": "Loi ket noi link4m: " + str(e)})

@app.route('/verify/<token>')
def verify_page(token):
    """Trang verify - user đến đây SAU KHI hoàn thành nhiệm vụ link4m"""
    if token not in pending_verify:
        return "<h1>Link khong hop le!</h1>", 404
    
    info = pending_verify[token]
    
    # Tạo key THẬT và lưu vào data
    key = generate_key()
    today = datetime.now().strftime("%Y-%m-%d")
    
    data.setdefault("free_keys", {})[key] = {
        "created_by": OWNER_ID,
        "expire": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "email": info["email"],
        "date": today,
        "verified": True
    }
    data.setdefault("keys_history", []).append({"key": key, "type": "free_verified", "time": datetime.now().isoformat()})
    save_data(data)
    
    # Gửi lệnh cho bot
    try:
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                     json={'chat_id': CHAT_ID, 'text': '/taokey free 1ngay'}, timeout=5)
    except: pass
    
    pending_verify[token]["verified"] = True
    pending_verify[token]["key"] = key
    
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Xac Thuc Thanh Cong</title>
    <style>body{{background:#0f0c29;color:#fff;text-align:center;padding:50px;font-family:Arial}}h2{{color:#0f0}}.key{{color:#0f0;background:#000;padding:15px;border-radius:10px;border:1px dashed #0f0;font-family:monospace;font-size:18px;margin:15px 0}}button{{background:#0f0;color:#000;padding:12px 25px;border:none;border-radius:8px;cursor:pointer;font-weight:bold;font-size:16px}}</style></head>
    <body><h2>HOAN THANH NHIEM VU!</h2><p>Key Free cua ban (1 ngay):</p>
    <div class="key">{key}</div>
    <button onclick="navigator.clipboard.writeText('{key}').then(function(){{alert('Da copy!')}})">COPY KEY</button>
    <p style="color:#aaa;margin-top:15px">Dung /kichhoat {key[:20]}... trong bot Telegram</p>
    <script>setTimeout(function(){{if(window.opener)window.opener.location.reload()}},2000)</script></body></html>'''

@app.route('/api/check-verify')
def api_check_verify():
    token = request.args.get('token', '')
    if token in pending_verify:
        if pending_verify[token].get("verified") and pending_verify[token].get("key"):
            key = pending_verify[token]["key"]
            # Không xóa token để có thể check lại
            return jsonify({"status": "verified", "key": key})
        return jsonify({"status": "pending"})
    return jsonify({"status": "error"})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        pass

data = load_data()

def generate_key():
    chars = string.ascii_uppercase + string.digits
    def rand(l):
        return ''.join(secrets.choice(chars) for _ in range(l))
    return f"QANH-{rand(10)}-{rand(10)}-{rand(10)}-{rand(5)}"

# ===== HTML =====
HTML = '''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QANH SHOP - Key Uy Tín</title>
    <style>
        :root{--gold:#FFD700;--green:#00ff00;--red:#ff4444;--blue:#0088ff;--purple:#9933ff}
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Segoe UI',Arial,sans-serif;color:#fff;min-height:100vh;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);background-attachment:fixed}
        .navbar{background:rgba(26,26,46,0.95);padding:15px 20px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:100;border-bottom:2px solid var(--gold);flex-wrap:wrap;gap:10px}
        .navbar .logo{font-size:22px;font-weight:bold;color:var(--gold)}
        .navbar .user-info{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
        .navbar .balance{background:rgba(0,0,0,0.5);border:1px solid var(--gold);border-radius:20px;padding:8px 15px;color:var(--gold);font-weight:bold;cursor:pointer;font-size:14px}
        .navbar .btn-nav{background:var(--gold);color:#000;border:none;border-radius:20px;padding:8px 18px;font-weight:bold;cursor:pointer;font-size:13px}
        .container{max-width:500px;margin:0 auto;padding:20px}
        .card{background:rgba(26,26,46,0.9);border-radius:15px;padding:20px;margin-bottom:15px;border:1px solid rgba(255,255,255,0.1)}
        .card h2{color:var(--gold);margin-bottom:10px;font-size:18px}
        .card .price{font-size:32px;font-weight:bold;color:var(--gold)}
        .card .duration{color:#aaa;margin:5px 0}
        .card ul{list-style:none;margin:10px 0}
        .card ul li{padding:4px 0;color:#ccc;font-size:14px}
        .card ul li::before{content:"✓ ";color:var(--green)}
        .btn-card{display:block;width:100%;padding:14px;border:none;border-radius:10px;font-size:16px;font-weight:bold;cursor:pointer;text-align:center;margin-top:10px;transition:0.3s}
        .btn-card:hover{opacity:0.9;transform:scale(1.02)}
        .btn-card:disabled{opacity:0.5;cursor:not-allowed}
        .btn-green{background:linear-gradient(135deg,#00cc00,#008800);color:#fff}
        .btn-gold{background:linear-gradient(135deg,#FFD700,#FFA500);color:#000}
        .btn-blue{background:linear-gradient(135deg,#0088cc,#004488);color:#fff}
        .btn-purple{background:linear-gradient(135deg,#9933ff,#6600cc);color:#fff}
        .btn-recharge{background:linear-gradient(135deg,#00ff88,#00cc66);color:#000;font-size:18px;padding:18px;font-weight:bold}
        .badge{padding:3px 10px;border-radius:20px;font-size:11px;font-weight:bold}
        .badge-free{background:#00cc00;color:#fff}
        .badge-vip{background:var(--gold);color:#000}
        .badge-hot{background:#ff6600;color:#fff;animation:pulse 1s infinite}
        @keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}
        .tabs{display:flex;margin-bottom:15px;border-radius:10px;overflow:hidden}
        .tab{flex:1;text-align:center;padding:12px;background:rgba(26,26,46,0.9);border:1px solid rgba(255,255,255,0.1);cursor:pointer;font-weight:bold;color:#aaa}
        .tab.active{background:var(--gold);color:#000}
        .hidden{display:none!important}
        .modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:1000;justify-content:center;align-items:center}
        .modal.active{display:flex}
        .modal-content{background:rgba(26,26,46,0.98);border-radius:15px;padding:25px;width:90%;max-width:420px;text-align:center;max-height:85vh;overflow-y:auto;border:1px solid var(--gold)}
        .modal-content h3{color:var(--gold);margin-bottom:15px;font-size:20px}
        .modal-content input,.modal-content select{width:100%;padding:12px;margin:8px 0;border-radius:8px;border:1px solid #333;background:#0f0f1f;color:#fff;font-size:14px}
        .modal-content .close-btn{float:right;color:var(--gold);font-size:24px;cursor:pointer;background:none;border:none}
        .key-display{font-size:14px;color:var(--green);font-family:monospace;background:#000;padding:15px;border-radius:8px;margin:10px 0;word-break:break-all;border:1px dashed var(--green)}
        .copy-btn{background:var(--gold);color:#000;border:none;padding:12px;border-radius:8px;cursor:pointer;font-weight:bold;width:100%}
        table{width:100%;border-collapse:collapse;font-size:13px}
        th{background:var(--gold);color:#000;padding:10px}
        td{padding:10px;border-bottom:1px solid rgba(255,255,255,0.1);text-align:center}
        .key-link{color:var(--green);cursor:pointer;text-decoration:underline}
        .loading-spinner{display:inline-block;width:30px;height:30px;border:3px solid #333;border-top:3px solid var(--gold);border-radius:50%;animation:spin 1s linear infinite}
        @keyframes spin{0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}
        .alert-box{background:rgba(255,0,0,0.1);border:1px solid var(--red);border-radius:10px;padding:15px;margin:10px 0;color:var(--red)}
        .success-box{background:rgba(0,255,0,0.1);border:1px solid var(--green);border-radius:10px;padding:15px;margin:10px 0;color:var(--green)}
        .info-text{color:#888;font-size:12px;margin-top:10px}
        .toast{position:fixed;top:20px;right:20px;z-index:10000;padding:15px 20px;border-radius:10px;color:#fff;font-weight:bold;max-width:350px;animation:slideIn 0.5s}
        .toast-success{background:#00cc00}.toast-error{background:#ff4444}
        @keyframes slideIn{from{transform:translateX(100%)}to{transform:translateX(0)}}
    </style>
</head>
<body>
    <div class="navbar">
        <div class="logo">⚡ QANH SHOP</div>
        <div class="user-info">
            <div class="balance" id="balanceDisplay" onclick="scrollToRecharge()">💰 0₫</div>
            <button class="btn-nav" id="authBtn" onclick="showAuthModal()">🔑 ĐĂNG NHẬP</button>
        </div>
    </div>

    <div class="container">
        <div class="tabs">
            <div class="tab active" onclick="switchTab('shop')">🛒 SHOP KEY</div>
            <div class="tab" onclick="switchTab('history')">📋 LỊCH SỬ</div>
        </div>

        <div id="shopTab">
            <div class="card" style="border-color:#00ff88;border-width:2px" id="rechargeSection">
                <h2>💳 NẠP TIỀN</h2>
                <select id="rcType"><option value="">Chọn nhà mạng</option><option value="VIETTEL">📱 Viettel</option><option value="MOBIFONE">📱 Mobifone</option><option value="VINAPHONE">📱 Vinaphone</option></select>
                <select id="rcAmount"><option value="">Chọn mệnh giá</option><option value="10000">10,000₫</option><option value="20000">20,000₫</option><option value="50000">50,000₫</option><option value="100000">100,000₫</option><option value="200000">200,000₫</option><option value="500000">500,000₫</option></select>
                <input type="text" id="rcPin" placeholder="🔢 Mã thẻ...">
                <input type="text" id="rcSerial" placeholder="📝 Serial...">
                <button class="btn-card btn-recharge" onclick="recharge()">💳 NẠP NGAY</button>
                <div id="rcResult" style="margin-top:10px"></div>
            </div>

            <div class="card" style="border-color:#00cc00">
                <h2>🆓 KEY FREE <span class="badge badge-free">MIỄN PHÍ</span></h2>
                <div class="price">0₫</div><div class="duration">⏰ 1 ngày</div>
                <ul><li>Dùng thử miễn phí</li></ul>
                <button class="btn-card btn-green" id="btnFreeKey" onclick="getFreeKey()">🎁 NHẬN KEY FREE</button>
                <div id="verifyStatus" style="margin-top:10px"></div>
                <p class="info-text">⚠️ Cần xem quảng cáo link4m (15 giây)</p>
            </div>

            <div class="card" style="border-color:#9933ff">
                <h2>💎 KEY 1 TUẦN <span class="badge badge-hot">HOT</span></h2>
                <div class="price">50,000₫</div><div class="duration">⏰ 7 ngày</div>
                <ul><li>Tất cả tính năng VIP</li></ul>
                <button class="btn-card btn-purple" onclick="buyKey('week')">💳 MUA NGAY</button>
            </div>

            <div class="card" style="border-color:#0088cc">
                <h2>🔑 KEY 1 THÁNG <span class="badge badge-vip">VIP</span></h2>
                <div class="price">150,000₫</div><div class="duration">⏰ 30 ngày</div>
                <ul><li>Tất cả tính năng VIP</li></ul>
                <button class="btn-card btn-blue" onclick="buyKey('month')">💳 MUA NGAY</button>
            </div>

            <div class="card" style="border-color:#FFD700">
                <h2>👑 KEY VĨNH VIỄN <span class="badge badge-vip">PREMIUM</span></h2>
                <div class="price">250,000₫</div><div class="duration">⏰ Không giới hạn</div>
                <ul><li>Tất cả Premium</li></ul>
                <button class="btn-card btn-gold" onclick="buyKey('forever')">💳 MUA NGAY</button>
            </div>
        </div>

        <div id="historyTab" class="hidden">
            <div class="card"><h2>📋 LỊCH SỬ KEY</h2><table><thead><tr><th>Key</th><th>Loại</th><th>Hạn</th></tr></thead><tbody id="keyHistory"><tr><td colspan="3">Chưa có</td></tr></tbody></table></div>
            <div class="card"><h2>💳 LỊCH SỬ NẠP</h2><table><thead><tr><th>Loại</th><th>Tiền</th><th>TT</th></tr></thead><tbody id="rechargeHistory"><tr><td colspan="3">Chưa có</td></tr></tbody></table></div>
        </div>
    </div>

    <div class="modal" id="authModal"><div class="modal-content">
        <button class="close-btn" onclick="closeModal('authModal')">✕</button>
        <h3>🔑 ĐĂNG NHẬP / ĐĂNG KÝ</h3>
        <input type="text" id="authEmail" placeholder="📧 Email">
        <input type="password" id="authPassword" placeholder="🔒 Mật khẩu">
        <button class="btn-card btn-gold" onclick="doAuth()">🔓 ĐĂNG NHẬP</button>
        <p class="info-text">Chưa có TK? Điền email + pass để tự động đăng ký</p>
    </div></div>

    <div class="modal" id="keyModal"><div class="modal-content">
        <button class="close-btn" onclick="closeModal('keyModal')">✕</button>
        <h3 style="color:#0f0">✅ THÀNH CÔNG!</h3>
        <p id="keyMessage"></p>
        <div class="key-display" id="keyDisplay"></div>
        <button class="copy-btn" onclick="copyKey()">📋 COPY KEY</button>
        <p class="info-text">💡 Dùng /kichhoat KEY trong bot Telegram</p>
    </div></div>

<script>
var API_BASE = window.location.origin;
var PARTNER_ID = "''' + PARTNER_ID + '''";
var PARTNER_KEY = "''' + PARTNER_KEY + '''";
var currentUser = null;
var userKeys = [];
var userRecharges = [];
var allUsers = [];
var ADMIN_EMAIL = "admin@qanhshop.com";
var ADMIN_PASS = "QanhAdmin@2025#Secret!";

try {
    currentUser = JSON.parse(localStorage.getItem('quanh_user')) || null;
    userKeys = JSON.parse(localStorage.getItem('quanh_keys')) || [];
    userRecharges = JSON.parse(localStorage.getItem('quanh_recharges')) || [];
    allUsers = JSON.parse(localStorage.getItem('quanh_all_users')) || [];
} catch(e) { currentUser = null; userKeys = []; userRecharges = []; allUsers = []; }

function saveAll() {
    try {
        if (currentUser) localStorage.setItem('quanh_user', JSON.stringify(currentUser));
        localStorage.setItem('quanh_keys', JSON.stringify(userKeys));
        localStorage.setItem('quanh_recharges', JSON.stringify(userRecharges));
        localStorage.setItem('quanh_all_users', JSON.stringify(allUsers));
    } catch(e) {}
}

function updateUI() {
    if (!currentUser) {
        document.getElementById('authBtn').innerText = '🔑 ĐĂNG NHẬP';
        document.getElementById('balanceDisplay').innerText = '💰 0₫';
    } else {
        document.getElementById('authBtn').innerText = '👤 ' + (currentUser.name || 'User');
        document.getElementById('balanceDisplay').innerText = '💰 ' + (currentUser.balance || 0).toLocaleString() + '₫';
    }
    updateHistory();
}

function showToast(msg, type) {
    var t = document.createElement('div');
    t.className = 'toast toast-' + (type || 'success');
    t.innerText = msg;
    document.body.appendChild(t);
    setTimeout(function() { t.style.opacity = '0'; t.style.transition = 'opacity 0.5s'; setTimeout(function() { t.remove(); }, 500); }, 2500);
}

function showModal(id) { document.getElementById(id).classList.add('active'); }
function closeModal(id) { document.getElementById(id).classList.remove('active'); }

function switchTab(tab) {
    document.querySelectorAll('.tab')[0].classList.toggle('active', tab === 'shop');
    document.querySelectorAll('.tab')[1].classList.toggle('active', tab === 'history');
    document.getElementById('shopTab').classList.toggle('hidden', tab !== 'shop');
    document.getElementById('historyTab').classList.toggle('hidden', tab !== 'history');
    if (tab === 'history') updateHistory();
}

function scrollToRecharge() {
    if (!currentUser) { showAuthModal(); return; }
    document.getElementById('rechargeSection').scrollIntoView({behavior: 'smooth'});
}

function showAuthModal() {
    if (currentUser) {
        if (confirm('Đăng xuất?')) { currentUser = null; localStorage.removeItem('quanh_user'); updateUI(); showToast('👋 Đã đăng xuất!'); }
        return;
    }
    document.getElementById('authEmail').value = '';
    document.getElementById('authPassword').value = '';
    showModal('authModal');
}

function doAuth() {
    var email = document.getElementById('authEmail').value.trim();
    var pass = document.getElementById('authPassword').value.trim();
    if (!email || !pass) { showToast('⚠️ Điền đầy đủ!', 'error'); return; }
    
    if (email === ADMIN_EMAIL && pass === ADMIN_PASS) {
        currentUser = { name: 'Admin', email: ADMIN_EMAIL, password: pass, balance: 999999999, isAdmin: true };
        saveAll();
        closeModal('authModal');
        updateUI();
        showToast('✅ Admin!', 'success');
        return;
    }
    
    var found = false;
    for (var i = 0; i < allUsers.length; i++) {
        if (allUsers[i].email === email) {
            if (allUsers[i].password !== pass) { showToast('❌ Sai mật khẩu!', 'error'); return; }
            currentUser = allUsers[i];
            found = true;
            break;
        }
    }
    if (!found) {
        currentUser = { name: email.split('@')[0], email: email, password: pass, balance: 0, isAdmin: false };
        allUsers.push(currentUser);
    }
    saveAll();
    closeModal('authModal');
    updateUI();
    showToast('✅ Thành công!');
}

async function recharge() {
    if (!currentUser) { showToast('⚠️ Đăng nhập!', 'error'); showAuthModal(); return; }
    var telco = document.getElementById('rcType').value;
    var amount = parseInt(document.getElementById('rcAmount').value);
    var pin = document.getElementById('rcPin').value.trim();
    var serial = document.getElementById('rcSerial').value.trim();
    if (!telco || !amount || !pin || !serial) { showToast('⚠️ Điền đầy đủ!', 'error'); return; }
    
    document.getElementById('rcResult').innerHTML = '<div class="loading-spinner"></div><p>Đang xử lý...</p>';
    try {
        var res = await fetch('https://api.shoppay.vn/card/charge', {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({partner_id: PARTNER_ID, partner_key: PARTNER_KEY, telco: telco, amount: amount, pin: pin, serial: serial})
        });
        var data = await res.json();
        if (data.status === 1) {
            currentUser.balance = (currentUser.balance || 0) + amount;
            for (var i = 0; i < allUsers.length; i++) { if (allUsers[i].email === currentUser.email) { allUsers[i].balance = currentUser.balance; break; } }
            userRecharges.unshift({type: telco, amount: amount, time: new Date().toLocaleString(), status: '✅ OK'});
            saveAll();
            updateUI();
            document.getElementById('rcResult').innerHTML = '<div class="success-box">✅ Nạp thành công ' + amount.toLocaleString() + '₫!</div>';
            document.getElementById('rcPin').value = ''; document.getElementById('rcSerial').value = '';
        } else {
            document.getElementById('rcResult').innerHTML = '<div class="alert-box">❌ ' + (data.message || 'Thẻ lỗi') + '</div>';
        }
    } catch(e) { document.getElementById('rcResult').innerHTML = '<div class="alert-box">❌ Lỗi kết nối!</div>'; }
}

var keyPrices = {week: 50000, month: 150000, forever: 250000};
var keyNames = {week: '💎 KEY 1 TUẦN', month: '🔑 KEY 1 THÁNG', forever: '👑 KEY VĨNH VIỄN'};
var keyDurations = {week: '7 NGÀY VIP', month: '30 NGÀY VIP', forever: 'VĨNH VIỄN'};

async function buyKey(type) {
    if (!currentUser) { showToast('⚠️ Đăng nhập!', 'error'); showAuthModal(); return; }
    var price = keyPrices[type];
    if ((currentUser.balance || 0) < price) { showToast('❌ Không đủ! Cần ' + price.toLocaleString() + '₫', 'error'); return; }
    if (!confirm('Xác nhận mua ' + keyNames[type] + ' giá ' + price.toLocaleString() + '₫?')) return;
    
    currentUser.balance -= price;
    for (var i = 0; i < allUsers.length; i++) { if (allUsers[i].email === currentUser.email) { allUsers[i].balance = currentUser.balance; break; } }
    saveAll();
    updateUI();
    
    try {
        var res = await fetch(API_BASE + '/api/buy-key?type=' + type + '&email=' + encodeURIComponent(currentUser.email));
        var data = await res.json();
        if (data.status === 'success') {
            userKeys.unshift({key: data.key, type: keyNames[type], duration: keyDurations[type], time: new Date().toLocaleString()});
            saveAll();
            document.getElementById('keyDisplay').innerText = data.key;
            document.getElementById('keyMessage').innerText = 'Mua ' + keyNames[type] + ' thành công!';
            showModal('keyModal');
            updateHistory();
            showToast('✅ Mua thành công!', 'success');
        } else {
            currentUser.balance += price;
            saveAll();
            updateUI();
            showToast('❌ ' + (data.message || 'Lỗi'), 'error');
        }
    } catch(e) {
        currentUser.balance += price;
        saveAll();
        updateUI();
        showToast('❌ Lỗi kết nối!', 'error');
    }
}

async function getFreeKey() {
    if (!currentUser) { showToast('⚠️ Đăng nhập!', 'error'); showAuthModal(); return; }
    var btn = document.getElementById('btnFreeKey');
    btn.disabled = true; btn.innerText = '⏳ Đang tạo...';
    
    try {
        var res = await fetch(API_BASE + '/api/get-free-link?email=' + encodeURIComponent(currentUser.email));
        var data = await res.json();
        
        if (data.status === 'success' && data.link4m) {
            document.getElementById('verifyStatus').innerHTML = '<div class="success-box">🔗 Đã mở link! Vui lòng xem và chờ 15 giây...</div>';
            window.open(data.link4m, '_blank');
            
            // Check verify
            var checks = 0;
            var interval = setInterval(async function() {
                checks++;
                try {
                    var cr = await fetch(API_BASE + '/api/check-free-key?email=' + encodeURIComponent(currentUser.email));
                    var cd = await cr.json();
                    if (cd.status === 'success' && cd.key) {
                        clearInterval(interval);
                        document.getElementById('verifyStatus').innerHTML = '<div class="success-box">✅ Đã xác thực!</div>';
                        userKeys.unshift({key: cd.key, type: '🆓 FREE', duration: '1 NGÀY', time: new Date().toLocaleString()});
                        saveAll();
                        document.getElementById('keyDisplay').innerText = cd.key;
                        document.getElementById('keyMessage').innerText = 'Key Free đã xác thực!';
                        showModal('keyModal');
                        updateHistory();
                    }
                } catch(e) {}
                if (checks >= 30) { clearInterval(interval); document.getElementById('verifyStatus').innerHTML = '<div class="alert-box">⏰ Hết thời gian!</div>'; }
            }, 10000);
        } else {
            document.getElementById('verifyStatus').innerHTML = '<div class="alert-box">❌ ' + (data.message || 'Lỗi') + '</div>';
        }
    } catch(e) {
        document.getElementById('verifyStatus').innerHTML = '<div class="alert-box">❌ Lỗi kết nối!</div>';
    }
    
    btn.disabled = false; btn.innerText = '🎁 NHẬN KEY FREE';
}

function copyKey() {
    var key = document.getElementById('keyDisplay').innerText;
    navigator.clipboard.writeText(key).then(function() {
        showToast('✅ Đã copy! /kichhoat ' + key.substring(0, 20) + '...');
    }).catch(function() {
        prompt('Copy key:', key);
    });
}

function updateHistory() {
    var kh = document.getElementById('keyHistory');
    if (userKeys.length === 0) {
        kh.innerHTML = '<tr><td colspan="3">Chưa có key nào</td></tr>';
    } else {
        var h = '';
        for (var i = 0; i < userKeys.length; i++) {
            h += '<tr><td class="key-link" onclick="document.getElementById(\'keyDisplay\').innerText=\'' + userKeys[i].key + '\';showModal(\'keyModal\')">' + userKeys[i].key.substring(0, 25) + '...</td><td>' + userKeys[i].type + '</td><td>' + userKeys[i].duration + '</td></tr>';
        }
        kh.innerHTML = h;
    }
    var rh = document.getElementById('rechargeHistory');
    if (userRecharges.length === 0) {
        rh.innerHTML = '<tr><td colspan="3">Chưa có giao dịch</td></tr>';
    } else {
        var h = '';
        for (var i = 0; i < userRecharges.length; i++) {
            h += '<tr><td>' + userRecharges[i].type + '</td><td>' + (userRecharges[i].amount || 0).toLocaleString() + '₫</td><td style="color:#0f0">' + userRecharges[i].status + '</td></tr>';
        }
        rh.innerHTML = h;
    }
}

updateUI();
</script>
</body>
</html>
'''

# ===== API ROUTES =====
pending_free_keys = {}

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/buy-key')
def api_buy_key():
    key_type = request.args.get('type', 'week')
    email = request.args.get('email', '')
    
    key = generate_key()
    bot_cmds = {'week': '1w', 'month': 'vip 1thang', 'forever': 'vip vinhvien'}
    bot_cmd = bot_cmds.get(key_type, '1w')
    
    # Gửi lệnh tạo key cho bot
    try:
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', 
                     json={'chat_id': CHAT_ID, 'text': f'/taokey {bot_cmd}'}, timeout=5)
    except:
        pass
    
    # Lưu key
    if key_type == 'week':
        data.setdefault("licenses", {})[key] = {"created_by": OWNER_ID, "expire_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")}
    elif key_type == 'month':
        data.setdefault("licenses", {})[key] = {"created_by": OWNER_ID, "expire_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")}
    elif key_type == 'forever':
        data.setdefault("licenses", {})[key] = {"created_by": OWNER_ID, "expire_date": None}
    
    data.setdefault("keys_history", []).append({"key": key, "type": key_type, "time": datetime.now().isoformat()})
    save_data(data)
    
    return jsonify({"status": "success", "key": key})

@app.route('/api/get-free-link')
def api_get_free_link():
    email = request.args.get('email', 'user')
    
    # Kiểm tra user đã nhận key free hôm nay chưa
    today = datetime.now().strftime("%Y-%m-%d")
    for k, v in data.get("free_keys", {}).items():
        if v.get("email") == email and v.get("date") == today:
            return jsonify({"status": "error", "message": "Hôm nay bạn đã nhận key free rồi!"})
    
    # Tạo link link4m
    token = secrets.token_hex(8)
    callback_url = f"https://qanhno1shop.onrender.com/verify/{token}"
    
    try:
        api_url = f"https://link4m.co/api-shorten/v2?api={LINK4M_API_KEY}&url={callback_url}"
        res = requests.get(api_url, timeout=10)
        link_data = res.json()
        
        if link_data.get('status') == 'success':
            pending_free_keys[token] = {"email": email, "time": time()}
            return jsonify({"status": "success", "link4m": link_data.get('shortenedUrl'), "token": token})
        else:
            # Fallback: tạo key trực tiếp
            key = generate_key()
            data.setdefault("free_keys", {})[key] = {"created_by": OWNER_ID, "expire": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"), "email": email, "date": today}
            save_data(data)
            try:
                requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', json={'chat_id': CHAT_ID, 'text': '/taokey free 1ngay'}, timeout=5)
            except: pass
            return jsonify({"status": "success", "key": key})
    except:
        key = generate_key()
        data.setdefault("free_keys", {})[key] = {"created_by": OWNER_ID, "expire": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"), "email": email, "date": today}
        save_data(data)
        return jsonify({"status": "success", "key": key})

@app.route('/verify/<token>')
def verify_page(token):
    if token not in pending_free_keys:
        return "<h1>Link không hợp lệ!</h1>", 404
    
    info = pending_free_keys[token]
    key = generate_key()
    today = datetime.now().strftime("%Y-%m-%d")
    
    data.setdefault("free_keys", {})[key] = {
        "created_by": OWNER_ID, 
        "expire": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"), 
        "email": info["email"], 
        "date": today, 
        "verified": True
    }
    data.setdefault("keys_history", []).append({"key": key, "type": "free_verified", "time": datetime.now().isoformat()})
    save_data(data)
    
    try:
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', json={'chat_id': CHAT_ID, 'text': '/taokey free 1ngay'}, timeout=5)
    except: pass
    
    pending_free_keys[token]["key"] = key
    pending_free_keys[token]["verified"] = True
    
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Xác Thực Thành Công</title>
    <style>body{{background:#0f0c29;color:#fff;text-align:center;padding:50px;font-family:Arial}}h2{{color:#0f0}}.key{{color:#0f0;background:#000;padding:15px;border-radius:10px;border:1px dashed #0f0;font-family:monospace;font-size:18px;margin:15px 0}}button{{background:#0f0;color:#000;padding:12px 25px;border:none;border-radius:8px;cursor:pointer;font-weight:bold;font-size:16px}}</style></head>
    <body><h2>XÁC THỰC THÀNH CÔNG!</h2><p>Key Free của bạn (1 ngày):</p>
    <div class="key">{key}</div>
    <button onclick="navigator.clipboard.writeText('{key}').then(function(){{alert('Đã copy!')}})">COPY KEY</button>
    <p style="color:#aaa;margin-top:15px">Dùng /kichhoat {key[:20]}... trong bot Telegram</p>
    <script>setTimeout(function(){{if(window.opener)window.opener.location.reload()}},2000)</script></body></html>'''

@app.route('/api/check-free-key')
def api_check_free_key():
    email = request.args.get('email', '')
    
    for token, info in pending_free_keys.items():
        if info.get("email") == email and info.get("verified") and info.get("key"):
            key = info["key"]
            del pending_free_keys[token]
            return jsonify({"status": "success", "key": key})
    
    return jsonify({"status": "pending"})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
