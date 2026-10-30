#!/usr/bin/env python3
"""Touch + hint + key/mark checks. Servers 8801/8802 must be running."""
import json
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    br = pw.chromium.launch()
    # mouse desktop: which hint shows, cursor on marks
    pg = br.new_page(viewport={'width': 760, 'height': 900}); pg.goto('http://localhost:8801/preview/nn-launch-kit/explorer/?embed=1&tab=governance'); pg.wait_for_timeout(600)
    vis = lambda: pg.evaluate('()=>[...document.querySelectorAll("#hint span")].filter(s=>getComputedStyle(s).display!=="none").map(s=>s.textContent)')
    print('desktop hint:', vis())
    pt = pg.evaluate('()=>NNX.pt("New York Times")'); pg.mouse.move(pt['x'] - 20, pt['y']); pg.mouse.move(pt['x'], pt['y'], steps=4); pg.wait_for_timeout(100)
    print('canvas cursor on mark:', pg.evaluate('()=>getComputedStyle(document.getElementById("cv")).cursor'), 'tip:', pg.evaluate('()=>document.getElementById("tip").innerText.replace(/\\n/g," | ")'))
    pg.mouse.move(5, 5); pg.wait_for_timeout(100); print('cursor off mark:', pg.evaluate('()=>getComputedStyle(document.getElementById("cv")).cursor'))
    pg.evaluate('()=>NNX.go("history")'); pg.wait_for_timeout(500)
    print('history mark cursor:', pg.evaluate('()=>getComputedStyle(document.querySelector("#hsvg .mk")).cursor'))
    # touch
    ctx = br.new_context(viewport={'width': 375, 'height': 812}, has_touch=True, is_mobile=True, device_scale_factor=2); tp = ctx.new_page()
    tp.goto('http://localhost:8801/preview/nn-launch-kit/explorer/?embed=1&tab=governance'); tp.wait_for_timeout(700)
    print('touch hint:', tp.evaluate('()=>[...document.querySelectorAll("#hint span")].filter(s=>getComputedStyle(s).display!=="none").map(s=>s.textContent)'))
    for tab in ('governance', 'ways'):
        tp.evaluate(f'()=>NNX.go("{tab}")'); tp.wait_for_timeout(1800)
        pt = tp.evaluate('()=>NNX.pt("New York Times")'); tp.touchscreen.tap(pt['x'], pt['y']); tp.wait_for_timeout(200)
        print(tab, 'tap tooltip:', tp.evaluate('()=>{const t=document.getElementById("tip");return t.hidden?null:t.innerText.replace(/\\n/g," | ")}'))
        tp.touchscreen.tap(8, 8); tp.wait_for_timeout(150); print(tab, 'tap elsewhere hides:', tp.evaluate('()=>document.getElementById("tip").hidden'))
    tp.evaluate('()=>NNX.go("history")'); tp.wait_for_timeout(600)
    mk = tp.locator('#hsvg .mk').nth(30); mk.scroll_into_view_if_needed(); tp.wait_for_timeout(300); b = mk.bounding_box(); tp.touchscreen.tap(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2); tp.wait_for_timeout(250)
    print('history tap tooltip:', tp.evaluate('()=>{const t=document.getElementById("htip");return t.hidden?null:t.innerText.replace(/\\n/g," | ")}'))
    tp.touchscreen.tap(8, 400); tp.wait_for_timeout(200); print('history tap elsewhere hides:', tp.evaluate('()=>document.getElementById("htip").hidden'))
    # key/mark: on each tab compare key svg opacity+fill with what charts draw
    pg2 = br.new_page(viewport={'width': 760, 'height': 900}); pg2.goto('http://localhost:8801/preview/nn-launch-kit/explorer/?embed=1&tab=governance'); pg2.wait_for_timeout(600)
    for tab in ('governance', 'ways', 'history'):
        pg2.evaluate(f'()=>NNX.go("{tab}")'); pg2.wait_for_timeout(1800)
        print('key', tab, pg2.evaluate('()=>[...document.querySelectorAll("#legend .row:last-child .sw")].map(s=>{const v=s.querySelector("svg"),sh=v.firstElementChild;return s.textContent.trim()+": "+sh.tagName+" fill="+(sh.getAttribute("fill")||"solid")+" opacity="+(v.style.opacity||sh.getAttribute("opacity")||"1")})'))
    br.close()
