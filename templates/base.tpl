<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>__ID__</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      /* 骨架默认用「示波器」风格；换风格时只改这一段色值 + 字体 */
      @font-face { font-family: "YH"; src: local("Microsoft YaHei"); }
      @font-face { font-family: "Mono"; src: local("Consolas"); }
      * { box-sizing: border-box; }
      html, body { margin: 0; background: #000; }
      #root { position: relative; width: 1920px; height: 1080px; overflow: hidden;
        background: #030C0A; font-family: YH, sans-serif; color: #E6FFFA; }
      .f { position: absolute; inset: 0; opacity: 0; overflow: hidden; }
      .gra { position: absolute; inset: 0;
        background-image: linear-gradient(rgba(95,232,200,0.085) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(95,232,200,0.085) 1px, transparent 1px);
        background-size: 400px 400px; }
      .gra2 { position: absolute; inset: 0;
        background-image: linear-gradient(rgba(95,232,200,0.03) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(95,232,200,0.03) 1px, transparent 1px);
        background-size: 20px 20px; }
      .scan { position: absolute; inset: 0; opacity: 0.55; mix-blend-mode: multiply;
        background: repeating-linear-gradient(to bottom, rgba(0,0,0,0.22) 0 1px, transparent 1px 3px); }
      .noise { position: absolute; inset: 0; opacity: 0.35;
        background-image: radial-gradient(rgba(230,255,250,0.05) 1px, transparent 1px); background-size: 3px 3px; }
      .vig { position: absolute; inset: 0;
        background: radial-gradient(ellipse at 50% 50%, transparent 26%, rgba(0,8,6,0.9) 100%); }
      .cx { position: absolute; left: 0; right: 0; top: 50%; height: 1px; background: rgba(95,232,200,0.10); }
      .cy { position: absolute; top: 0; bottom: 0; left: 50%; width: 1px; background: rgba(95,232,200,0.10); }
      .kick { position: absolute; left: 88px; top: 48px; font-family: Mono; font-size: 13px;
        letter-spacing: 6px; color: #5FE8C8; }
      .idx { position: absolute; right: 88px; top: 48px; font-family: Mono; font-size: 12px;
        letter-spacing: 5px; color: rgba(95,232,200,0.45); }
      .ro { position: absolute; left: 88px; bottom: 52px; font-family: Mono; font-size: 12px;
        letter-spacing: 3px; color: rgba(95,232,200,0.5); }
      .h { font-weight: 900; letter-spacing: -3px; line-height: 1.06; }
      .mono { font-family: Mono; letter-spacing: 3px; }
      .amber { color: #FFB347; }
      .dim { color: #6E9A90; }
      .glow { filter: drop-shadow(0 0 10px rgba(95,232,200,0.65)) drop-shadow(0 0 30px rgba(95,232,200,0.28)); }
      .glowA { filter: drop-shadow(0 0 10px rgba(255,179,71,0.6)); }
      /* 逐句揭示：默认隐藏，由 build.py 在对应句开始时点亮 */
      .ln { opacity: 0; transform: translateY(16px); }
      .draw { stroke-dasharray: 3000; stroke-dashoffset: 3000; }
      #sub { position: absolute; left: 150px; right: 150px; bottom: 44px; text-align: center;
        font-size: 33px; letter-spacing: 2px; color: #DFFFF7; opacity: 0; z-index: 99;
        text-shadow: 0 0 24px rgba(3,12,10,0.95), 0 2px 10px rgba(3,12,10,0.9); }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="__ID__" data-width="1920" data-height="1080" data-duration="__DURATION__">

      <!-- 01 钩子 -->
      <section class="f" id="s1">
        <div class="gra"></div><div class="gra2"></div><div class="cx"></div><div class="cy"></div>
        <div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">01 / 钩子</div><div class="idx">CH1 · 01</div>
        <div class="ro">SAMPLE 240 Hz</div>
        <svg width="1800" height="400" viewBox="0 0 1800 400" style="position:absolute;left:60px;top:290px">
          <path class="draw ln1" d="M 0 200 L 300 200 L 340 132 L 380 268 L 420 200 L 760 200 L 800 168 L 840 232 L 880 200 L 1200 200 L 1240 84 L 1280 324 L 1320 200 L 1800 200"
                fill="none" stroke="#5FE8C8" stroke-width="2.5" class="glow" />
        </svg>
        <div style="position:absolute;left:88px;top:700px">
          <div class="h ln ln1" style="font-size:100px">第一句的画面文字</div>
          <div class="h ln ln2" style="font-size:100px;color:#FFB347;margin-top:4px">第二句的画面文字</div>
        </div>
      </section>

      <!-- 02 片名 -->
      <section class="f" id="s2">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div style="position:absolute;left:0;right:0;top:300px;text-align:center">
          <div class="h ln ln3" style="font-size:132px">片名第一行</div>
          <div class="h ln ln3 glow" style="font-size:132px;color:#5FE8C8;margin-top:4px">片名第二行</div>
        </div>
      </section>

      <!-- 03 对比 -->
      <section class="f" id="s3">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">02 / 对比</div>
        <div style="position:absolute;left:96px;top:230px;width:560px">
          <div class="h ln ln4" style="font-size:72px">第四句</div>
          <div class="h ln ln5" style="font-size:72px;color:#FFB347;margin-top:2px">第五句</div>
        </div>
        <svg width="1120" height="520" viewBox="0 0 1120 520" style="position:absolute;left:720px;top:300px">
          <rect class="ln ln4" x="60" y="106" width="180" height="40" fill="rgba(95,232,200,0.28)" stroke="#5FE8C8" stroke-width="2" />
          <rect class="ln ln5" x="60" y="286" width="620" height="40" fill="rgba(255,179,71,0.18)" stroke="#FFB347" stroke-width="2" />
        </svg>
      </section>

      <!-- 04 快路 -->
      <section class="f" id="s4">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">03 / 快路</div>
        <div style="position:absolute;left:88px;top:260px;width:560px">
          <div class="h ln ln6" style="font-size:84px">第六句</div>
          <div class="mono amber ln ln7" style="font-size:110px;margin-top:30px">12<span style="font-size:38px">ms</span></div>
          <div class="mono dim ln ln8" style="margin-top:12px;font-size:14px">第八句的注释</div>
        </div>
        <svg width="1000" height="480" viewBox="0 0 1000 480" style="position:absolute;left:820px;top:360px">
          <path class="draw ln6" d="M 100 250 L 840 230" fill="none" stroke="#5FE8C8" stroke-width="2.5" class="glow" />
          <circle class="ln ln6" cx="100" cy="250" r="26" fill="#030C0A" stroke="#5FE8C8" stroke-width="2" />
          <circle class="ln ln7" cx="840" cy="230" r="28" fill="none" stroke="#FFB347" stroke-width="2" class="glowA" />
        </svg>
      </section>

      <!-- 05 慢路 -->
      <section class="f" id="s5">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">04 / 慢路</div>
        <div style="position:absolute;left:88px;top:250px;width:560px">
          <div class="h ln ln9" style="font-size:84px">第九句</div>
          <div class="mono ln ln10" style="font-size:110px;margin-top:34px">≈500<span style="font-size:38px">ms</span></div>
          <div class="mono dim ln ln11" style="margin-top:12px;font-size:14px">第十一句的注释</div>
        </div>
        <svg width="1000" height="480" viewBox="0 0 1000 480" style="position:absolute;left:820px;top:340px">
          <path class="draw ln9" d="M 100 250 Q 340 40 660 110 Q 800 150 840 220" fill="none" stroke="#5FE8C8" stroke-width="2.5" class="glow" />
        </svg>
      </section>

      <!-- 06 三条通道 -->
      <section class="f" id="s6">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">05 / 身体</div>
        <div style="position:absolute;left:96px;top:250px;width:520px">
          <div class="h ln ln12" style="font-size:74px">第十二句</div>
          <div class="h ln ln13" style="font-size:74px;margin-top:2px">第十三句</div>
          <div class="h ln ln14" style="font-size:56px;color:#5FE8C8;margin-top:18px">第十四句</div>
        </div>
        <svg width="1080" height="560" viewBox="0 0 1080 560" style="position:absolute;left:760px;top:300px">
          <path class="draw ln12" d="M 200 110 L 360 110 L 380 50 L 400 170 L 420 110 L 620 110 L 640 60 L 660 160 L 680 110 L 1070 110"
                fill="none" stroke="#5FE8C8" stroke-width="2.5" class="glow" />
          <path class="draw ln13" d="M 200 290 Q 330 220 460 290 Q 590 360 720 290 Q 850 220 980 290"
                fill="none" stroke="rgba(95,232,200,0.75)" stroke-width="2.5" />
          <path class="draw ln14" d="M 200 470 L 420 470 L 440 420 L 460 510 L 480 470 L 760 470 L 780 430 L 800 505 L 820 470 L 1070 470"
                fill="none" stroke="rgba(255,179,71,0.9)" stroke-width="2.5" class="glowA" />
        </svg>
      </section>

      <!-- 07 解释 -->
      <section class="f" id="s7">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">06 / 解释</div>
        <div style="position:absolute;left:96px;top:250px;width:500px">
          <div class="h ln ln15" style="font-size:70px">第十五句</div>
        </div>
        <svg width="1080" height="560" viewBox="0 0 1080 560" style="position:absolute;left:720px;top:280px">
          <rect class="ln ln16" x="40" y="40" width="640" height="120" fill="rgba(255,179,71,0.06)" stroke="#FFB347" stroke-width="3" />
          <text class="ln ln16" x="70" y="116" fill="#FFB347" font-size="46" font-weight="700">第十六句</text>
        </svg>
      </section>

      <!-- 08 循环 -->
      <section class="f" id="s8">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">07 / 循环</div>
        <div style="position:absolute;left:96px;top:250px;width:520px">
          <div class="h ln ln17" style="font-size:78px">第十七句</div>
          <div class="h ln ln18" style="font-size:78px;margin-top:2px">第十八句</div>
          <div class="h ln ln19" style="font-size:56px;color:#FFB347;margin-top:16px">第十九句</div>
        </div>
        <svg width="900" height="620" viewBox="0 0 900 620" style="position:absolute;left:880px;top:230px">
          <circle class="ln ln17" cx="430" cy="310" r="210" fill="none" stroke="#5FE8C8" stroke-width="4"
                  stroke-dasharray="440 880" transform="rotate(-90 430 310)" class="glow" />
        </svg>
      </section>

      <!-- 09 放大器 -->
      <section class="f" id="s9">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">08 / 放大器</div>
        <div style="position:absolute;left:96px;top:230px;width:520px">
          <div class="h ln ln20" style="font-size:62px">第二十句</div>
          <div class="mono amber ln ln21" style="font-size:96px;margin-top:24px">+60<span style="font-size:38px">%</span></div>
          <div class="mono dim ln ln21" style="margin-top:12px;font-size:15px">第二十一句的注记</div>
          <div class="mono dim ln ln22" style="margin-top:8px;font-size:15px">第二十二句的注记</div>
        </div>
      </section>

      <!-- 10 收尾 -->
      <section class="f" id="s10">
        <div class="gra"></div><div class="gra2"></div><div class="noise"></div><div class="scan"></div><div class="vig"></div>
        <div class="kick">09 / 收尾</div>
        <div style="position:absolute;left:96px;top:250px;width:580px">
          <div class="h ln ln23" style="font-size:62px">第二十三句</div>
          <div class="h ln ln24" style="font-size:62px;color:#5FE8C8;margin-top:2px">第二十四句</div>
        </div>
      </section>

      <div id="sub"></div>
    </div>

    <script>
      /*__TIMELINE__*/
    </script>
  </body>
</html>
