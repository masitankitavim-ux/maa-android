# -*- coding: utf-8 -*-
html = r'''<!DOCTYPE html>
<html lang="zh-CN" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>MAA 控制台 · 明日方舟</title>
<style>
:root{
  --bg:#0b1020;--panel:rgba(24,31,48,.82);--panel2:rgba(35,44,66,.82);
  --line:#2b3550;--text:#eef2fb;--muted:#9aa6c2;--accent:#e8b04b;--accent2:#34c98e;
  --danger:#f0645c;--warn:#f5b83d;--radius:14px;
}
html[data-theme="light"]{
  --bg:#eef1f8;--panel:rgba(255,255,255,.92);--panel2:rgba(244,247,252,.92);
  --line:#d9e0ef;--text:#17203a;--muted:#65708c;--accent:#c8891e;--accent2:#1f9d6b;
  --danger:#d6453a;--warn:#c99018;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{
  color:var(--text);font:14px/1.55 -apple-system,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;
  height:100vh;display:flex;flex-direction:column;overflow:hidden;position:relative;
  background:
    radial-gradient(1200px 620px at 82% -10%, rgba(232,176,75,.16), transparent 60%),
    radial-gradient(900px 520px at -8% 112%, rgba(76,141,255,.14), transparent 55%),
    linear-gradient(160deg,#0b1020 0%, #10172b 55%, #0a0e1a 100%);
}
html[data-theme="light"] body{
  background:
    radial-gradient(1200px 620px at 82% -10%, rgba(200,137,30,.12), transparent 60%),
    radial-gradient(900px 520px at -8% 112%, rgba(37,99,235,.10), transparent 55%),
    linear-gradient(160deg,#f7f9fe 0%, #eef1f8 55%, #e9edf6 100%);
}
body::before{
  content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:
    repeating-linear-gradient(45deg, rgba(255,255,255,.025) 0 2px, transparent 2px 18px),
    repeating-linear-gradient(-45deg, rgba(255,255,255,.018) 0 2px, transparent 2px 18px);
}
button{font:inherit;background:var(--accent);color:#201a10;border:0;border-radius:9px;padding:8px 14px;font-size:13px;cursor:pointer;white-space:nowrap;font-weight:600}
button:hover{filter:brightness(1.06)}
button:active{transform:translateY(1px)}
button.sec{background:var(--panel2);color:var(--text);border:1px solid var(--line)}
button.danger{background:var(--danger);color:#fff}
button.green{background:var(--accent2);color:#fff}
button.ghost{background:transparent;color:var(--muted);border:1px solid var(--line)}
button:disabled{opacity:.45;cursor:not-allowed}
button.small{padding:5px 10px;font-size:12px}

.top{position:relative;z-index:1;display:flex;align-items:center;gap:10px;padding:11px 16px;background:var(--panel);border-bottom:1px solid var(--line);flex-wrap:wrap;backdrop-filter:blur(8px)}
.top h1{font-size:16px;font-weight:800;letter-spacing:.4px;background:linear-gradient(90deg,var(--accent),#f4d98c);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.top .sp{flex:1;min-width:8px}
.badge{display:inline-flex;align-items:center;gap:6px;padding:4px 11px;border-radius:999px;font-size:12px;border:1px solid var(--line);background:var(--panel2);color:var(--muted)}
.dot{width:8px;height:8px;border-radius:50%;background:var(--muted);flex:none}
.dot.on{background:var(--accent2)}
.dot.run{background:var(--accent);animation:blink 1s infinite}
@keyframes blink{50%{opacity:.25}}
.actions{display:flex;gap:8px;flex-wrap:wrap}

.main{position:relative;z-index:1;display:grid;grid-template-columns:430px minmax(0,1fr);gap:14px;padding:14px;flex:1;min-height:0}
.side{display:flex;flex-direction:column;gap:14px;overflow-y:auto;min-height:0;padding-right:3px;-webkit-overflow-scrolling:touch;overscroll-behavior:contain}
.workspace{display:flex;min-width:0;min-height:0}
.workspace .card{flex:1;min-width:0;min-height:0;display:flex;flex-direction:column}

.card{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:14px;backdrop-filter:blur(8px)}
.card-head{display:flex;align-items:center;gap:8px;cursor:pointer;user-select:none}
.card-head h2{font-size:14px;font-weight:700;flex:1}
.card-head .count{font-size:11px;color:var(--muted)}
.card-head .arrow{color:var(--muted);transition:transform .15s}
.card.collapsed .arrow{transform:rotate(-90deg)}
.card-body{margin-top:12px}
.card.collapsed .card-body{display:none}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:9px}
.field{display:flex;flex-direction:column;gap:4px;min-width:0}
.field label{font-size:12px;color:var(--text);font-weight:600}
.field .fdesc{font-size:11px;color:var(--muted);line-height:1.35}
input,select,textarea{background:var(--panel2);border:1px solid var(--line);color:var(--text);border-radius:8px;padding:8px 10px;font-size:13px;width:100%}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--accent)}
textarea{resize:vertical;min-height:52px;font-family:ui-monospace,Consolas,monospace;font-size:12px}
.row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.check{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--muted)}
.check input{width:auto}

#tasks{max-height:480px;overflow-y:auto;padding-right:4px;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;scrollbar-width:thin}
.task{display:flex;align-items:center;gap:9px;padding:9px 10px;border:1px solid var(--line);border-radius:10px;margin-bottom:7px;background:var(--panel2);cursor:pointer}
.task:hover{border-color:var(--accent)}
.task input[type=checkbox]{width:auto;flex:none}
.task .tbody{flex:1;min-width:0}
.task .tname{font-weight:700;font-size:13px}
.task .tdesc{font-size:11px;color:var(--muted);line-height:1.35;margin-top:1px}
.task .arrow{color:var(--muted);transition:transform .15s}
.task.open .arrow{transform:rotate(180deg)}
.params{display:none;margin:0 0 10px 26px;padding:12px;border-left:3px solid var(--accent);background:var(--panel2);border-radius:10px}
.params.open{display:grid;grid-template-columns:1fr;gap:11px}
.params .hint{grid-column:1/-1}

.tabs{display:flex;gap:6px;margin-bottom:12px;border-bottom:1px solid var(--line);padding-bottom:10px}
.tabs button{background:var(--panel2);color:var(--muted);border:1px solid var(--line);border-radius:8px;padding:6px 14px}
.tabs button.active{background:var(--accent);color:#201a10;border-color:var(--accent)}
.tabpane{flex:1;min-height:0;display:flex;flex-direction:column}
#log{flex:1;min-height:0;overflow:auto;font-family:ui-monospace,Consolas,monospace;font-size:13px;white-space:pre-wrap;word-break:break-word;background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:10px}
.logline{padding:3px 0;border-bottom:1px solid var(--line)}
.logline:last-child{border-bottom:0}
.logline b{color:var(--accent)}
.logline.err{color:var(--danger)}
.logline.ok{color:var(--accent2)}
.logline.warn{color:var(--warn)}
.shotbar{display:flex;gap:8px;align-items:center;margin-bottom:10px;flex-wrap:wrap}
.shotwrap{flex:1;min-height:0;max-height:calc(100vh - 190px);overflow:auto;background:var(--panel2);border:1px solid var(--line);border-radius:10px}
#shot{display:block;max-width:100%;height:auto;border-radius:8px;cursor:crosshair}
.hint{font-size:11px;color:var(--muted)}
.mono{font-family:ui-monospace,Consolas,monospace;font-size:12px}
#updateOut{margin-top:12px;white-space:pre-wrap;color:var(--muted);background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:10px;min-height:44px}

/* 桌宠 ew */
.pet{position:fixed;left:20px;top:20px;width:74px;height:74px;z-index:60;pointer-events:none;transition:left .9s ease-in-out,top .9s ease-in-out;filter:drop-shadow(0 6px 8px rgba(0,0,0,.35))}
.pet svg{width:100%;height:100%}
.pet.hop svg{animation:petbounce .55s ease-in-out}
@keyframes petbounce{0%{transform:translateY(0) scale(1,1)}35%{transform:translateY(-14px) scale(.96,1.04)}70%{transform:translateY(0) scale(1.05,.95)}100%{transform:translateY(0) scale(1,1)}}

@media (max-width:900px){
  .main{display:block;overflow-y:auto}
  .side{display:block;overflow:visible;padding-right:0}
  .side .card{margin-bottom:14px}
  .workspace{min-height:0}
  #tasks{max-height:none;overflow:visible}
  .shotwrap{max-height:calc(100vh - 240px)}
}
</style>
</head>
<body>
<div class="top">
  <h1>MAA · 明日方舟托管</h1>
  <span class="badge"><span class="dot" id="connDot"></span><span id="connText">未连接</span></span>
  <span class="badge"><span class="dot" id="runDot"></span><span id="runText">空闲</span></span>
  <span class="badge mono" id="verText">-</span>
  <span class="sp"></span>
  <div class="actions">
    <button class="green" id="btnLong">⚡ 一键长草</button>
    <button id="btnStart">▶ 开始</button>
    <button class="danger" id="btnStop">■ 停止</button>
    <button class="sec" id="btnHome">⌂ 返回主界面</button>
    <button class="ghost small" id="btnTheme">🌓 主题</button>
  </div>
</div>

<div class="main">
  <div class="side">
    <div class="card" id="connCard">
      <div class="card-head" onclick="toggleCard('connCard')"><h2>连接设置</h2><span class="arrow">▼</span></div>
      <div class="card-body">
        <div class="grid2">
          <div class="field"><label>客户端类型</label>
            <select id="clientType"><option>Official</option><option>Bilibili</option><option>YoStarEN</option><option>YoStarJP</option><option>YoStarKR</option><option>txwy</option></select></div>
          <div class="field"><label>游戏包名</label><input id="pkg" value="com.hypergryph.arknights"></div>
          <div class="field"><label>ADB 地址</label><input id="adbAddr" placeholder="127.0.0.1"></div>
          <div class="field"><label>ADB 端口</label><input id="adbPort" type="number" placeholder="5555"></div>
          <div class="field"><label>触控模式</label>
            <select id="touchMode"><option value="Android">Android 原生</option><option value="adb">ADB</option><option value="MaaFwAdb">MaaFwAdb</option><option value="minitouch">Minitouch</option><option value="maatouch">Maatouch</option><option value="MumuExtras">MumuExtras</option></select></div>
          <div class="field"><label>显示 ID</label><input id="displayId" type="number" value="0"></div>
          <div class="field"><label>宽</label><input id="width" type="number" value="1280"></div>
          <div class="field"><label>高</label><input id="height" type="number" value="720"></div>
        </div>
        <div class="row" style="margin-top:10px">
          <button id="btnConnect" style="flex:1">连接</button>
          <label class="check"><input id="forceStop" type="checkbox" checked>强制停止游戏</label>
        </div>
        <p class="hint" style="margin-top:8px">Android 原生模式无需 ADB；选择 ADB / MaaFwAdb 时才填写地址与端口。</p>
      </div>
    </div>

    <div class="card" id="farmCard">
      <div class="card-head" onclick="toggleCard('farmCard')"><h2>一键长草任务</h2><span class="count" id="taskCount">0 项</span><span class="arrow">▼</span></div>
      <div class="card-body">
        <div class="row" style="margin-bottom:9px">
          <button class="sec small" id="btnAll">全选</button>
          <button class="sec small" id="btnNone">清空</button>
          <span style="flex:1"></span>
          <span class="hint">点任务行展开详细参数</span>
        </div>
        <div id="tasks"></div>
        <button class="green" id="btnApplyRun" style="width:100%;margin-top:12px">应用任务并启动</button>
      </div>
    </div>

    <div class="card" id="schCard">
      <div class="card-head" onclick="toggleCard('schCard')"><h2>每日定时长草</h2><span class="count" id="schStatus">未启用</span><span class="arrow">▼</span></div>
      <div class="card-body">
        <label class="check" style="margin-bottom:9px"><input id="schEnabled" type="checkbox">启用每日定时</label>
        <label class="check" style="margin-bottom:9px"><input id="schLaunch" type="checkbox" checked>到点先打开明日方舟</label>
        <div class="row">
          <div class="field" style="flex:1"><label>启动时间</label><input id="schTime" type="time" value="04:00"></div>
          <button class="sec" id="schSave" style="align-self:flex-end">保存</button>
        </div>
        <p class="hint" style="margin-top:9px">到点后自动打开明日方舟，并运行上方已勾选的「一键长草任务」。</p>
        <div class="row" style="margin-top:10px">
          <button class="sec small" id="schRun">立即执行一次</button>
          <span class="hint" id="schLast">上次执行：-</span>
        </div>
      </div>
    </div>
  </div>

  <div class="workspace">
    <div class="card">
      <div class="tabs">
        <button class="active" data-tab="log">状态 / 日志</button>
        <button data-tab="shot">截图</button>
        <button data-tab="update">自动更新</button>
      </div>
      <div class="tabpane" id="tab-log"><div id="log"></div></div>
      <div class="tabpane" id="tab-shot" style="display:none">
        <div class="shotbar">
          <button id="btnShot">手动截图</button>
          <span class="hint">点击画面可对游戏点击（坐标已按分辨率映射）</span>
        </div>
        <div class="shotwrap"><img id="shot" alt="screenshot"></div>
      </div>
      <div class="tabpane" id="tab-update" style="display:none">
        <p class="hint" style="margin-bottom:10px">从 GitHub 拉取最新 MAA Android 组件，校验后原子替换并重启控制台。</p>
        <button id="btnUpdate">检查并更新</button>
        <pre id="updateOut" class="mono"></pre>
      </div>
    </div>
  </div>
</div>

<div class="pet" id="pet">
  <svg viewBox="0 0 96 96" xmlns="http://www.w3.org/2000/svg">
    <ellipse cx="48" cy="78" rx="24" ry="12" fill="#f3e7d3"/>
    <ellipse cx="48" cy="56" rx="26" ry="24" fill="#f7efe2"/>
    <path d="M28 30 C30 18 38 16 42 24 L40 32 Z" fill="#e2b64f"/>
    <path d="M68 30 C66 18 58 16 54 24 L56 32 Z" fill="#e2b64f"/>
    <path d="M30 34 C20 40 22 52 32 54 Z" fill="#f7efe2"/>
    <path d="M66 34 C76 40 74 52 64 54 Z" fill="#f7efe2"/>
    <circle cx="38" cy="52" r="4.6" fill="#4a2f18"/>
    <circle cx="58" cy="52" r="4.6" fill="#4a2f18"/>
    <circle cx="39.6" cy="50.4" r="1.6" fill="#fff"/>
    <circle cx="59.6" cy="50.4" r="1.6" fill="#fff"/>
    <ellipse cx="34" cy="62" rx="4.4" ry="2.8" fill="#f4a6a0"/>
    <ellipse cx="62" cy="62" rx="4.4" ry="2.8" fill="#f4a6a0"/>
    <path d="M44 62 Q48 66 52 62" stroke="#b97a5a" stroke-width="2" fill="none" stroke-linecap="round"/>
    <path d="M40 78 Q48 84 56 78 L54 88 L42 88 Z" fill="#f7efe2"/>
  </svg>
</div>

<script>
function $(id){return document.getElementById(id);}
function esc(s){return String(s).replace(/[<>&]/g,c=>({"<":"&lt;",">":"&gt;","&":"&amp;"}[c]));}
function attr(s){return esc(s).replace(/"/g,"&quot;");}

const TASK_ORDER=["StartUp","Fight","Recruit","Infrast","Mall","Award","Roguelike","Copilot","Depot","OperBox","CloseDown"];

const TASK_META={
  StartUp:{name:"开始唤醒",desc:"启动游戏并进入主界面，处理公告、签到等弹窗。",fields:[
    {k:"client_type",label:"客户端",type:"text",desc:"游戏客户端类型：Official 官服 / Bilibili B服 等"},
    {k:"start_game_enabled",label:"自动启动游戏",type:"bool",desc:"游戏未运行时自动拉起"},
    {k:"account_name",label:"账号备注",type:"text",desc:"可选，用于区分多账号"}]},
  Fight:{name:"刷理智",desc:"自动刷取指定关卡消耗理智。",fields:[
    {k:"stage",label:"关卡",type:"text",desc:"关卡代号，如 1-7、CE-5"},
    {k:"medicine",label:"理智药",type:"number",desc:"使用理智回复剂数量，0 为不使用"},
    {k:"stone",label:"源石",type:"number",desc:"使用源石次数，0 为不使用"},
    {k:"times",label:"刷取次数",type:"number",desc:"刷取次数，填大数表示刷完为止"},
    {k:"series",label:"连战",type:"number",desc:"连战系列，0 为默认"},
    {k:"drops",label:"掉落统计",type:"json",desc:"掉落物品统计，如 {\"30011\":1}"},
    {k:"report_to_penguin",label:"企鹅物流上报",type:"bool",desc:"是否上报企鹅物流统计"},
    {k:"penguin_id",label:"企鹅物流ID",type:"text",desc:"可选，企鹅物流统计 ID"},
    {k:"server",label:"服务器",type:"text",desc:"CN / US / JP / KR"},
    {k:"client_type",label:"客户端",type:"text",desc:"游戏客户端类型"},
    {k:"DrGrandet",label:"葛朗台模式",type:"bool",desc:"理智不足时是否自动用源石补"},
    {k:"expiring_medicine",label:"即将过期药",type:"number",desc:"优先使用即将过期的理智药数量"}]},
  Recruit:{name:"自动公招",desc:"自动进行公开招募并处理标签。",fields:[
    {k:"refresh",label:"自动刷新",type:"bool",desc:"自动刷新公招列表"},
    {k:"select",label:"选择标签",type:"array",arr:"num",desc:"选择标签索引，逗号分隔"},
    {k:"confirm",label:"确认标签",type:"array",arr:"num",desc:"确认出稀有标签索引，逗号分隔"},
    {k:"times",label:"招募次数",type:"number",desc:"招募次数"},
    {k:"expedite",label:"加速",type:"bool",desc:"使用加速道具"},
    {k:"skip_robot",label:"跳过机器人",type:"bool",desc:"跳过机器人标签"},
    {k:"set_time",label:"设置时长",type:"bool",desc:"自动设置招募时长"},
    {k:"recruitment_time",label:"招募时长",type:"json",desc:"标签等级对应时长(分钟)，如 {\"3\":540,\"4\":540}"},
    {k:"report_to_penguin",label:"企鹅物流上报",type:"bool",desc:"是否上报企鹅物流"},
    {k:"report_to_yituliu",label:"一图流上报",type:"bool",desc:"是否上报一图流"},
    {k:"server",label:"服务器",type:"text",desc:"CN / US / JP / KR"}]},
  Infrast:{name:"基建换班",desc:"自动进行基建设施换班。",fields:[
    {k:"facility",label:"设施",type:"array",arr:"str",desc:"要换班的设施：Mfg 制造站、Trade 贸易站、Power 发电站、Control 中枢、Reception 会客室、Office 办公室、Dorm 宿舍"},
    {k:"drones",label:"无人机用途",type:"text",desc:"无人机用途，_NotUse 为不使用"},
    {k:"threshold",label:"阈值",type:"number",desc:"心情低于该阈值才换班，0~1"},
    {k:"replenish",label:"补满心情",type:"bool",desc:"是否把干员心情补满"},
    {k:"dorm_notstationed_enabled",label:"宿舍非驻守干员",type:"bool",desc:"启用宿舍非驻守干员策略"},
    {k:"dorm_trust_enabled",label:"宿舍刷信赖",type:"bool",desc:"启用宿舍刷信赖策略"}]},
  Mall:{name:"领取信用及购物",desc:"领取信用并自动购物。",fields:[
    {k:"shopping",label:"购物",type:"bool",desc:"是否自动购买"},
    {k:"buy_first",label:"优先购买",type:"array",arr:"str",desc:"优先购买物品，逗号分隔"},
    {k:"blacklist",label:"黑名单",type:"array",arr:"str",desc:"不购买的物品，逗号分隔"},
    {k:"force_shopping_if_credit_full",label:"信用满强制购物",type:"bool",desc:"信用满时强制购物"},
    {k:"only_buy_discount",label:"只买折扣",type:"bool",desc:"只购买打折物品"}]},
  Award:{name:"领取日常奖励",desc:"一键领取各类每日奖励。",fields:[
    {k:"award",label:"每日奖励",type:"bool",desc:"领取每日任务奖励"},
    {k:"mail",label:"邮件",type:"bool",desc:"领取邮件"},
    {k:"recruit",label:"公招奖励",type:"bool",desc:"领取公开招募奖励"},
    {k:"orundum",label:"源石",type:"bool",desc:"领取源石"},
    {k:"mining",label:"采矿",type:"bool",desc:"领取采矿奖励"},
    {k:"specialaccess",label:"特殊权限",type:"bool",desc:"领取特殊权限奖励"}]},
  Roguelike:{name:"自动肉鸽",desc:"自动探索集成战略/肉鸽模式。",fields:[
    {k:"theme",label:"主题",type:"text",desc:"肉鸽主题：Phantom / Sami / Mizuki / Sarkaz 等"},
    {k:"mode",label:"模式",type:"number",desc:"肉鸽模式编号，见 MAA 文档"},
    {k:"starts_count",label:"开始次数",type:"number",desc:"开始探索次数"},
    {k:"investment_enabled",label:"投资",type:"bool",desc:"是否进行投资"},
    {k:"investments_count",label:"投资次数",type:"number",desc:"投资次数"},
    {k:"stop_when_investment_full",label:"投资满停止",type:"bool",desc:"投资满时停止"}]},
  Copilot:{name:"自动抄作业",desc:"按作业 JSON 自动执行关卡作业。",fields:[
    {k:"filename",label:"作业文件名",type:"text",desc:"作业 JSON 文件名，需已放到资源目录"},
    {k:"formation",label:"阵容",type:"bool",desc:"是否自动编队"}]},
  Depot:{name:"仓库识别",desc:"识别仓库物品库存。",fields:[]},
  OperBox:{name:"干员box识别",desc:"识别干员图鉴与练度。",fields:[]},
  CloseDown:{name:"关闭游戏",desc:"结束托管并退出游戏。",fields:[
    {k:"client_type",label:"客户端",type:"text",desc:"游戏客户端类型"}]}
};

const TASK_DEFAULTS={
  StartUp:{client_type:"Official",start_game_enabled:true,account_name:""},
  Fight:{stage:"",medicine:0,stone:0,times:2147483647,series:0,drops:{"30011":1},report_to_penguin:false,penguin_id:"",server:"CN",client_type:"Official",DrGrandet:false,expiring_medicine:0},
  Recruit:{refresh:true,select:[4],confirm:[3,4],times:4,expedite:false,skip_robot:true,set_time:true,recruitment_time:{"3":540,"4":540},report_to_penguin:true,report_to_yituliu:true,server:"CN"},
  Infrast:{facility:["Mfg","Trade","Power","Control","Reception","Office","Dorm"],drones:"_NotUse",threshold:0.3,replenish:false,dorm_notstationed_enabled:false,dorm_trust_enabled:false},
  Mall:{shopping:true,buy_first:["招聘许可","龙门币"],blacklist:[],force_shopping_if_credit_full:false,only_buy_discount:true},
  Award:{award:true,mail:true,recruit:true,orundum:true,mining:true,specialaccess:true},
  Roguelike:{theme:"Phantom",mode:0,starts_count:9999999,investment_enabled:true,investments_count:999,stop_when_investment_full:false},
  Copilot:{filename:"",formation:false},
  Depot:{},
  OperBox:{},
  CloseDown:{client_type:"Official"}
};

const TASKS=TASK_ORDER.map(t=>({type:t,params:TASK_DEFAULTS[t]||{}}));

function toggleCard(id){$(id).classList.toggle("collapsed");}

function fieldHTML(f,v){
  const label=esc(f.label||f.k);
  const desc=f.desc?('<span class="fdesc">'+esc(f.desc)+'</span>'):'';
  const full=(f.type==="array"||f.type==="json")?" full":"";
  let ctrl="";
  if(f.type==="bool"){
    ctrl='<select data-k="'+attr(f.k)+'" data-bool="1"><option value="true"'+(v?' selected':'')+'>是</option><option value="false"'+(v?'':' selected')+'>否</option></select>';
  }else if(f.type==="number"){
    ctrl='<input data-k="'+attr(f.k)+'" type="number" value="'+attr(String(v))+'">';
  }else if(f.type==="array"){
    const at=f.arr||(v&&v.length&&typeof v[0]==="number"?"num":"str");
    ctrl='<input data-k="'+attr(f.k)+'" data-array="1" data-arrtype="'+at+'" value="'+attr(Array.isArray(v)?v.join(", "):String(v))+'" placeholder="逗号分隔">';
  }else if(f.type==="json"){
    const txt=(typeof v==="string")?v:JSON.stringify(v);
    ctrl='<textarea data-k="'+attr(f.k)+'" data-json="1" rows="3">'+esc(txt)+'</textarea>';
  }else{
    ctrl='<input data-k="'+attr(f.k)+'" value="'+attr(String(v))+'">';
  }
  return '<div class="field'+full+'"><label>'+label+'</label>'+ctrl+desc+'</div>';
}

function renderTasks(){
  const box=$("tasks");box.innerHTML="";
  TASKS.forEach((t,i)=>{
    const meta=TASK_META[t.type]||{name:t.type,desc:"",fields:[]};
    const d=document.createElement("div");d.className="task";
    d.innerHTML='<input type="checkbox" data-i="'+i+'" '+((i<6)?"checked":"")+'><div class="tbody"><div class="tname">'+esc(meta.name)+'</div><div class="tdesc">'+esc(meta.desc)+'</div></div><span class="arrow">▾</span>';
    d.onclick=function(e){if(e.target.tagName!=="INPUT"){d.classList.toggle("open");const p=d.nextElementSibling;p.classList.toggle("open");}};
    box.appendChild(d);
    const p=document.createElement("div");p.className="params";p.dataset.ti=i;
    const fields=meta.fields&&meta.fields.length?meta.fields:Object.keys(t.params||{}).map(k=>({k,label:k,type:"text",desc:""}));
    p.innerHTML=fields.map(f=>fieldHTML(f,(t.params||{})[f.k])).join("")||'<span class="hint">无参数</span>';
    box.appendChild(p);
  });
  $("taskCount").textContent=TASKS.length+" 项";
}

function taskParams(i){
  const t=TASKS[i];const out={};
  const panel=document.querySelector('.params[data-ti="'+i+'"]');
  if(!panel)return out;
  panel.querySelectorAll("[data-k]").forEach(inp=>{
    const k=inp.dataset.k;const orig=(t.params||{})[k];let v=inp.value;
    if(inp.dataset.bool){v=(v==="true");}
    else if(inp.dataset.array){v=v.split(",").map(x=>x.trim()).filter(x=>x!=="");if(inp.dataset.arrtype==="num")v=v.map(Number);}
    else if(inp.dataset.json){try{v=JSON.parse(v)}catch(e){v=orig}}
    else if(typeof orig==="number"){v=Number(v);}
    out[k]=v;
  });
  return out;
}
function selectedTasks(){
  const out=[];
  document.querySelectorAll(".task input[type=checkbox]").forEach(cb=>{
    if(cb.checked){const i=+cb.dataset.i;out.push({type:TASKS[i].type,params:JSON.stringify(taskParams(i))});}
  });
  return out;
}
async function api(path,opt){const r=await fetch(path,opt);return r.json().catch(()=>({}));}
function log(msg,cls){const d=document.createElement("div");d.className="logline "+(cls||"");d.innerHTML=msg;const l=$("log");l.appendChild(d);while(l.children.length>200)l.removeChild(l.firstChild);l.scrollTop=l.scrollHeight;}

function summarize(ev){
  const m=ev.msg;let obj={};try{obj=JSON.parse(ev.json||"{}")}catch(e){}
  const chain=obj.taskchain||obj.task||"";
  const name=TASK_META[chain]?TASK_META[chain].name:(chain||"任务");
  if(m===2)return{text:"✅ 全部任务已完成",cls:"ok"};
  if(m===10000)return{text:"⚠ 失败："+name,cls:"err"};
  if(m===10001)return{text:"▶ 开始："+name,cls:""};
  if(m===10002)return{text:"✅ 完成："+name,cls:"ok"};
  if(m===10003){const what=obj.what||obj.subtask||"";return{text:"· "+name+(what?(" — "+what):""),cls:""};}
  if(m===20002)return{text:"   完成子步骤："+(obj.what||obj.subtask||chain||"")}; 
  return null;
}

async function refreshState(){
  try{const s=await api("/api/state");
    $("verText").textContent="MAA "+(s.version||"-");
    $("connDot").className="dot "+(s.connected?"on":"");
    $("connText").textContent=s.connected?"已连接":"未连接";
    $("runDot").className="dot "+(s.running?"run":"");
    $("runText").textContent=s.running?"运行中":"空闲";
    if(s.config){
      const c=s.config;
      $("clientType").value=c.client_type||"Official";
      $("pkg").value=c.package||"com.hypergryph.arknights";
      $("adbAddr").value=c.adb_address||"";
      $("adbPort").value=(c.adb_port||"");
      $("touchMode").value=c.touch_mode||"Android";
      $("displayId").value=(c.display_id==null?0:c.display_id);
      $("width").value=c.width||1280;
      $("height").value=c.height||720;
      $("forceStop").checked=!!c.force_stop;
    }
  }catch(e){}
}
async function refreshSchedule(){
  try{const s=await api("/api/schedule");
    $("schEnabled").checked=!!s.enabled;
    $("schLaunch").checked=(s.launch==null?true:!!s.launch);
    $("schTime").value=s.time||"04:00";
    $("schStatus").textContent=s.enabled?("已启用 "+s.time):"未启用";
    $("schLast").textContent="上次执行："+(s.last_run||"-");
  }catch(e){}
}
function connect(){
  const payload={
    client_type:$("clientType").value,
    package:$("pkg").value,
    width:+$("width").value,height:+$("height").value,
    display_id:+$("displayId").value,
    touch_mode:$("touchMode").value,
    force_stop:$("forceStop").checked,
    adb_address:$("adbAddr").value.trim(),
    adb_port:+($("adbPort").value||0)
  };
  log("正在连接…","");
  api("/api/connect",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)}).then(()=>{log("连接请求已发送","ok");setTimeout(refreshState,1500);});
}
async function runFarm(){
  const tasks=selectedTasks();
  let n=0;
  for(const t of tasks){
    const name=TASK_META[t.type]?TASK_META[t.type].name:t.type;
    await api("/api/append_task",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(t)}).then(r=>{log("已添加："+name+" (#"+r.id+")","ok");n++;});
  }
  log("一键长草：共 "+n+" 个任务，即将启动","ok");
  setTimeout(async()=>{const r=await api("/api/start",{method:"POST"});log(r.ok?"已启动，请留意右侧日志":"启动失败",r.ok?"ok":"err");refreshState();},300);
}
function saveSchedule(){
  const body={enabled:$("schEnabled").checked,time:$("schTime").value,launch:$("schLaunch").checked,tasks:selectedTasks()};
  api("/api/schedule",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)}).then(s=>{
    log("定时设置已保存","ok");refreshSchedule();
  });
}

$("btnConnect").onclick=connect;
$("btnStart").onclick=()=>api("/api/start",{method:"POST"}).then(r=>{log(r.ok?"已启动":"启动失败",r.ok?"ok":"err");refreshState();});
$("btnStop").onclick=()=>api("/api/stop",{method:"POST"}).then(r=>{log("已停止","warn");refreshState();});
$("btnHome").onclick=()=>api("/api/back_home",{method:"POST"}).then(()=>log("返回主界面","ok"));
$("btnLong").onclick=runFarm;
$("btnApplyRun").onclick=runFarm;
$("btnAll").onclick=()=>document.querySelectorAll(".task input[type=checkbox]").forEach(cb=>cb.checked=true);
$("btnNone").onclick=()=>document.querySelectorAll(".task input[type=checkbox]").forEach(cb=>cb.checked=false);
$("schSave").onclick=saveSchedule;
$("schRun").onclick=()=>api("/api/schedule/run",{method:"POST"}).then(()=>log("已触发一次定时执行","ok"));
$("btnShot").onclick=async()=>{await api("/api/screencap",{method:"POST"});refreshShot();};
function refreshShot(){$("shot").src="/api/screenshot.png?t="+Date.now();}
$("shot").onclick=function(e){const r=e.target.getBoundingClientRect();const x=Math.round((e.clientX-r.left)*($("width").value/r.width));const y=Math.round((e.clientY-r.top)*($("height").value/r.height));api("/api/click?x="+x+"&y="+y,{method:"POST"}).then(()=>log("点击 ("+x+","+y+")","ok"));};
$("btnUpdate").onclick=function(){const o=$("updateOut");o.textContent="检查中…";api("/api/update",{method:"POST"}).then(()=>{const t=setInterval(async()=>{const s=await api("/api/update/status");o.textContent=s.status||"";if(!s.status||s.status!=="running")clearInterval(t);},2000);});};
$("btnTheme").onclick=function(){const h=document.documentElement;const next=h.getAttribute("data-theme")==="dark"?"light":"dark";h.setAttribute("data-theme",next);localStorage.setItem("maa-theme",next);};
document.querySelectorAll(".tabs button").forEach(b=>b.onclick=function(){document.querySelectorAll(".tabs button").forEach(x=>x.classList.remove("active"));b.classList.add("active");document.querySelectorAll(".tabpane").forEach(x=>x.style.display="none");$("tab-"+b.dataset.tab).style.display="";if(b.dataset.tab==="shot")refreshShot();});

const es=new EventSource("/api/events");
es.onmessage=function(e){try{const ev=JSON.parse(e.data);const s=summarize(ev);if(s)log(s.text,s.cls||"");}catch(_){}};

function petHop(){
  const pet=$("pet");const w=innerWidth,h=innerHeight;
  const pw=pet.offsetWidth||74,ph=pet.offsetHeight||74;
  const x=Math.round(Math.random()*Math.max(1,w-pw-16))+8;
  const y=Math.round(Math.random()*Math.max(1,h-ph-20))+8;
  pet.style.left=x+"px";pet.style.top=y+"px";
  pet.classList.remove("hop");void pet.offsetWidth;pet.classList.add("hop");
}
setInterval(petHop,3400);

(function init(){const t=localStorage.getItem("maa-theme");if(t)document.documentElement.setAttribute("data-theme",t);renderTasks();refreshState();refreshSchedule();setInterval(refreshState,3000);setInterval(refreshSchedule,30000);petHop();})();
</script>
</body>
</html>
'''
import io
p = r'work\maa-project\maaweb\webui\index.html'
io.open(p, 'w', encoding='utf-8', newline='').write(html)
print('wrote', p, len(html), 'bytes')
