import pandas as pd
import calendar
import json
from datetime import datetime

# ==========================================
# CONSTANTES DE MARCA
# ==========================================
LOGO_SRC = "https://github.com/Valbaton/public_resources_gunova/blob/main/Assets/elrenaco_white.png?raw=true" 

MESES_ES = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 
            7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}

PALETA = {
    'sidebar_bg':       'rgba(8, 14, 26, 0.4)',                 
    'accent_color':     '#00d2ff',                 
    'card_border':      'rgba(255, 255, 255, 0.08)', 
    'video_color':      '#3b82f6',                 
    'grafica_color':    '#0ea5e9',                 
    'story_color':      '#06b6d4',                 
    'nota_color':       '#6366f1',                 
    'default_color':    '#2563eb'                  
}

def clean_text(txt):
    if pd.isna(txt) or txt == '-': return ''
    return str(txt).replace('\n', '<br>')

def get_color(t):
    t = str(t).strip()
    if t in ['Video', 'Reel']: return PALETA['video_color']
    if t == 'Gráfica': return PALETA['grafica_color']
    if 'Fotografía' in t: return PALETA['story_color']
    if 'Editorial' in t: return PALETA['nota_color']
    return PALETA['default_color']

# ==========================================
# GENERADORES MODULARES
# ==========================================
def generar_crm(df, svgs):
    if df.empty: return "<div style='color:var(--txt-s); font-style:italic; padding:20px;'>No hay registros en esta categoría.</div>"
    cards = ""
    for _, r in df.iterrows():
        nick = clean_text(r.get('Acc_nickname')); nom = clean_text(r.get('Acc_nombre'))
        foto = str(r.get('Acc_Foto_Perfil', '')).strip()
        origen = clean_text(r.get('Acc_Origen', 'Comunidad')); cat = clean_text(r.get('Acc_categoría', 'General'))
        
        def parse_folls(val):
            if val in ['-', 'nan', '', '0']: return False, "", 0
            try:
                num = int(float(val))
                return True, f"{num:,}", num
            except:
                v_low = val.lower().replace(',', '.')
                s_val = 0
                try:
                    if 'k' in v_low: s_val = int(float(v_low.replace('k','')) * 1000)
                    elif 'm' in v_low: s_val = int(float(v_low.replace('m','')) * 1000000)
                except: pass
                return True, val, s_val

        ig_raw = str(r.get('Instagram_Follows', '-')).strip()
        tk_raw = str(r.get('Tiktok_Follows', '-')).strip()
        
        has_ig, ig_disp, ig_sort = parse_folls(ig_raw)
        has_tk, tk_disp, tk_sort = parse_folls(tk_raw)
        
        ig_er_raw = str(r.get('Instagram_EngagementRate', '-')).strip()
        tk_er_raw = str(r.get('Tiktok_EngagementRate', '-')).strip()
        gen_er = str(r.get('Engagement', '-')).strip()
        if ig_er_raw == '-' and gen_er != '-': ig_er_raw = gen_er
        if tk_er_raw == '-' and gen_er != '-': tk_er_raw = gen_er

        def fmt_er(val):
            if val == '-' or val == 'nan': return ''
            try:
                v = float(val)
                return f"{v*100:.1f}%" if v < 1 else f"{v:.1f}%"
            except:
                return f"{val}%" if not str(val).endswith('%') else str(val)

        ig_er = fmt_er(ig_er_raw); tk_er = fmt_er(tk_er_raw)
        c_orig = '#10b981' if origen == 'Booking' else '#f43f5e' if origen == 'Competencia' else '#8b5cf6' if origen == 'Aliado Comercial' else '#0ea5e9'
        badge_origen = f'<div style="background:{c_orig}15; color:{c_orig}; border:1px solid {c_orig}40; font-size:9px; padding:4px 12px; border-radius:50px; font-weight:900; display:inline-block; margin-bottom:18px; text-transform:uppercase; letter-spacing:1px; box-shadow: inset 0 0 10px {c_orig}10;">{origen}</div>'
        
        metrics = ""
        if has_ig: 
            er_html = f'<span class="er-tag">ER: {ig_er}</span>' if ig_er else ''
            metrics += f'<div class="foll-badge"><span>IG</span> {ig_disp} {er_html}</div>'
        if has_tk: 
            er_html = f'<span class="er-tag">ER: {tk_er}</span>' if tk_er else ''
            metrics += f'<div class="foll-badge"><span>TK</span> {tk_disp} {er_html}</div>'
        
        bg_ring = f"linear-gradient(#0f172a, #0f172a) padding-box, linear-gradient(45deg, {c_orig}, #0ea5e9) border-box"
        links = []
        for col in ['Instagram_Link', 'Tiktok_Link', 'Otros_Link1', 'Otros_Link2']:
            val = str(r.get(col, '')).strip()
            if val != '-' and 'http' in val:
                k = 'web'
                if 'instagram.com' in val: k = 'ig'
                elif 'tiktok.com' in val: k = 'tk'
                elif 'youtube.com' in val or 'youtu.be' in val: k = 'yt'
                links.append(f'<a href="{val}" target="_blank" class="s-link"><svg viewBox="0 0 24 24"><path d="{svgs[k]}"/></svg></a>')
            
        cards += f"""<div class="crm-card" data-cat="{cat}" data-ig="{ig_sort}" data-tk="{tk_sort}"><div class="crm-ava-wrap" style="background: {bg_ring};"><img src="{foto}" class="crm-ava-img" onerror="this.src='https://via.placeholder.com/100/0f172a/00d2ff?text=++'"></div>{badge_origen}<div style="font-weight:900; font-size:18px; margin-bottom:5px; color:#fff; letter-spacing:-0.5px;">{nom}</div><div style="color:var(--txt-s); font-size:12px; font-weight:700; margin-bottom:15px; opacity:0.8;">@{nick}</div><div style="display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin-bottom:20px;">{metrics}</div><div style="display:flex; justify-content:center; gap:18px; border-top:1px solid rgba(255,255,255,0.08); padding-top:20px;">{"".join(links)}</div></div>"""
    return cards

def generar_calendario(df, APP_DATA):
    if df.empty: return ""
    html = ""
    for p in sorted(df['Post_Fecha'].dt.to_period('M').dropna().unique()):
        m_name = MESES_ES[p.month]
        m_id = f"{m_name} {p.year}"
        html += f'<div class="month-wrapper" data-mes="{m_id}" style="margin-bottom:60px;"><h3 style="color:white; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:15px; font-weight:900; text-transform:uppercase; font-size:24px; letter-spacing:-1px; display:inline-block; margin-bottom:25px;">{m_id}</h3><div class="cal-wrapper"><div class="cal-grid">'
        
        for d_str in ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]:
            html += f'<div style="text-align:center; font-weight:900; color:var(--accent); font-size:11px; padding:10px 0; border-bottom:2px solid rgba(0,210,255,0.3); text-transform:uppercase; letter-spacing:2px; text-shadow: 0 0 10px rgba(0,210,255,0.2);">{d_str}</div>'

        for week in calendar.monthcalendar(p.year, p.month):
            for day in week:
                if day == 0: html += '<div class="day-c" style="border:none; background:transparent;"></div>'
                else:
                    html += f'<div class="day-c"><div style="text-align:right; font-weight:900; color: rgba(255,255,255,0.2); font-size:24px; margin-bottom:10px; font-variant-numeric: tabular-nums;">{day}</div>'
                    events = df[(df['Post_Fecha'].dt.day == day) & (df['Post_Fecha'].dt.month == p.month)]
                    for i, e in events.iterrows():
                        tit = clean_text(e.get('Contenido_Titulo')); tipo = clean_text(e.get('Contenido_Tipo')); sub = clean_text(e.get('Contenido_Tipo_Detalle')); est = clean_text(e.get('Post_Estado'))
                        id_i = f"P_{p.month}_{day}_{i}"
                        links = []
                        l_rec = str(e.get('Post_Link_Recurso','')).strip(); l_pub = str(e.get('Post_Link_RRRSS','')).strip()
                        if 'http' in l_rec: links.append({'url': l_rec, 'lbl': 'Recurso', 'pri': False})
                        if 'http' in l_pub: links.append({'url': l_pub, 'lbl': 'Link', 'pri': True})
                        
                        APP_DATA[id_i] = {'tit': tit, 'desc': clean_text(e.get('Contenido_Descripción')), 'copy': clean_text(e.get('Post_Copy')), 'tag': f"{tipo} | {sub}", 'links': links}
                        
                        thumb_html = ""
                        if 'http' in l_pub and 'drive.google.com' in l_pub and '/file/d/' in l_pub:
                            try:
                                file_id = l_pub.split('/file/d/')[1].split('/')[0]
                                thumb_url = f"https://drive.google.com/thumbnail?id={file_id}&sz=w400"
                                thumb_html = f'<div class="card-preview-wrap"><img src="{thumb_url}" class="card-preview-img" onerror="this.parentElement.style.display=\'none\'"></div>'
                            except:
                                pass
                        
                        html += f'<div class="card s-item" style="border-left-color:{get_color(tipo)};" data-ftipo="{tipo}" data-fsub="{sub}" data-fpost="{est}" data-tit="{tit}" onclick="openM(\'{id_i}\')">'
                        html += f'<div style="font-weight:900; color:{get_color(tipo)}; font-size:10px; text-transform:uppercase; letter-spacing:1px;">{tipo}</div><div style="font-weight:800; padding-right:10px; font-size:13px; line-height:1.5; color:#fff;">{tit}</div>{thumb_html}<div class="c-badge" style="background:rgba(255,255,255,0.08); color:var(--txt-s); padding:5px 10px; border-radius:6px; font-size:9px; font-weight:800; width:fit-content; margin-top:auto; letter-spacing:1px; border: 1px solid rgba(255,255,255,0.05);">{est}</div></div>'
                    html += '</div>'
        html += '</div></div></div>'
    return html

# ==========================================
# MOTOR PRINCIPAL
# ==========================================
def construir_dashboard(df_rrss, df_comu, df_acc):
    APP_DATA = {}

    # EXTRACTOR DEL EVENTO PRINCIPAL
    ev_nombre = "Evento Principal"
    ev_banner = "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=2070&auto=format&fit=crop"
    ev_fecha_display = "Fecha por definir"
    ev_fecha_js = ""

    if not df_acc.empty:
        r_evento = df_acc.iloc[0]
        ev_nombre = clean_text(r_evento.get('Evento_Nombre', ev_nombre))
        ban_val = str(r_evento.get('Evento_Banner_Link', '')).strip()
        if ban_val != '-' and 'http' in ban_val: ev_banner = ban_val
        
        fec_val = r_evento.get('Evento_Fecha')
        if pd.notna(fec_val) and fec_val != '-':
            try:
                dt = pd.to_datetime(fec_val, dayfirst=True)
                ev_fecha_display = f"{dt.day} de {MESES_ES[dt.month]} {dt.year} - 20:00 HRS"
                ev_fecha_js = dt.strftime('%Y-%m-%dT20:00:00') 
            except:
                ev_fecha_display = str(fec_val)

    # FILTROS GLOBALES
    meses_disponibles = []
    if not df_rrss.empty:
        for p in sorted(df_rrss['Post_Fecha'].dt.to_period('M').dropna().unique()):
            meses_disponibles.append(f"{MESES_ES[p.month]} {p.year}")

    all_tipos = sorted([str(x) for x in df_rrss['Contenido_Tipo'].astype(str).unique() if x != '-']) if not df_rrss.empty else []
    all_formatos = sorted([str(x) for x in df_rrss['Contenido_Tipo_Detalle'].astype(str).unique() if x != '-']) if not df_rrss.empty else []
    all_estados = sorted([str(x) for x in df_rrss['Post_Estado'].astype(str).unique() if x != '-']) if not df_rrss.empty else []

    # SEGREGACIÓN DE CRM
    df_artistas = pd.DataFrame(); df_medios = pd.DataFrame(); df_influencers = pd.DataFrame()
    if not df_comu.empty and 'Acc_categoría' in df_comu.columns:
        categoria = df_comu['Acc_categoría'].astype(str).str.strip().str.lower()
        es_artista = categoria == 'artista'
        es_medio = categoria == 'medio de comunicación'
        
        df_artistas = df_comu[es_artista]
        df_medios = df_comu[es_medio]
        df_influencers = df_comu[~es_artista & ~es_medio]

    svgs = {
        'ig': 'M7.8 2h8.4C19.4 2 22 4.6 22 7.8v8.4a5.8 5.8 0 0 1-5.8 5.8H7.8C4.6 22 2 19.4 2 16.2V7.8A5.8 5.8 0 0 1 7.8 2m.2 2A3.6 3.6 0 0 0 4.4 7.6v8.8C4.4 18.39 6 20 8 20h8c2 0 3.6-1.61 3.6-3.6V7.6C19.6 5.6 18 4 16 4H8m8 11.17c-1.12 1.12-2.97 1.12-4.09 0-1.12-1.12-1.12-2.97 0-4.09 1.12-1.12 2.97-1.12 4.09 0 1.12 1.12 1.12 2.97 0 4.09M16.5 6a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3',
        'tk': 'M12.5 3a.5.5 0 0 0-.5.5v12.16c0 2.15-1.74 3.89-3.89 3.89A3.89 3.89 0 0 1 4.22 15.67a3.89 3.89 0 0 1 3.89-3.89c.33 0 .64.04.94.12a.5.5 0 0 0 .61-.59l-.47-2.32a.5.5 0 0 0-.58-.39 8.24 8.24 0 0 0-1.78-.1 8.27 8.27 0 0 0-8.27 8.27 8.27 8.27 0 0 0 8.27 8.27c4.57 0 8.27-3.7 8.27-8.27V9.74a10.85 10.85 0 0 0 4.67 1.17.5.5 0 0 0 .5-.5v-2.36a.5.5 0 0 0-.5-.5 6.44 6.44 0 0 1-5.63-3.37.5.5 0 0 0-.48-.28h-2.35z',
        'yt': 'M21.58 7.19c-.23-.86-.91-1.54-1.77-1.77C18.25 5 12 5 12 5s-6.25 0-7.81.42c-.86.23-1.54.91-1.77 1.77C2 8.75 2 12 2 12s0 3.25.42 4.81c.23.86.91 1.54 1.77 1.77C5.75 19 12 19 12 19s6.25 0 7.81-.42c.86-.23 1.54-.91 1.77-1.77C22 15.25 22 12 22 12s0-3.25-.42-4.81zM10 15V9l5.2 3-5.2 3z',
        'web': 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z'
    }

    html_meses = "".join([f'<div class="f-opt" onclick="toggleF(\'mes\', \'{x}\', this)">{x}</div>' for x in meses_disponibles])
    html_tipos = "".join([f'<div class="f-opt" onclick="toggleF(\'tipo\', \'{x}\', this)">{x}</div>' for x in all_tipos])
    html_formatos = "".join([f'<div class="f-opt" onclick="toggleF(\'sub\', \'{x}\', this)">{x}</div>' for x in all_formatos])
    html_estados = "".join([f'<div class="f-opt" onclick="toggleF(\'post\', \'{x}\', this)">{x}</div>' for x in all_estados])

    influencers_html = generar_crm(df_influencers, svgs)
    artistas_html = generar_crm(df_artistas, svgs)
    medios_html = generar_crm(df_medios, svgs)
    marketing_html = generar_calendario(df_rrss, APP_DATA)

    app_data_json = json.dumps(APP_DATA).replace("</", "<\\/")

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SPACE HUB | {ev_nombre}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700;800;900&display=swap');
            :root {{ 
                --accent: {PALETA['accent_color']}; --txt: #f8fafc; --txt-s: #94a3b8;
                --sidebar_bg: {PALETA['sidebar_bg']}; --card-border: {PALETA['card_border']};
            }}
            * {{ box-sizing: border-box; scrollbar-width: thin; scrollbar-color: var(--accent) transparent; }}
            
            /* DYNAMIC MESH BACKGROUND */
            body {{ 
                font-family: 'Montserrat', sans-serif; 
                background-color: #020617;
                background-image: 
                    radial-gradient(circle at 15% 50%, rgba(0, 210, 255, 0.08), transparent 25%),
                    radial-gradient(circle at 85% 30%, rgba(99, 102, 241, 0.08), transparent 25%);
                color: var(--txt); 
                margin:0; padding:0; height:100vh; display:flex; overflow:hidden; 
            }}
            
            /* PREMIUM SIDEBAR */
            .sidebar {{ width: 90px; height: auto; max-height: 85vh; background: var(--sidebar_bg); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px); border: 1px solid var(--card-border); border-radius: 24px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 30px 0; gap: 35px; margin-left: 20px; position: fixed; left: 0; top: 50%; transform: translateY(-50%); z-index: 100; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5), inset 0 0 0 1px rgba(255,255,255,0.05); transition: 0.3s; }}
            .brand-logo {{ width: 50px; border-radius: 12px; margin-bottom: 5px; filter: drop-shadow(0 0 10px rgba(255,255,255,0.2)); }}
            .nav-icon {{ font-size: 24px; cursor: pointer; opacity: 0.4; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); position: relative; display:flex; flex-direction:column; align-items:center; gap:5px; }}
            .nav-icon span {{ font-size: 9px; font-weight:800; opacity:0; transition:0.3s; position:absolute; bottom:-18px; white-space:nowrap; text-transform:uppercase; color:var(--accent); letter-spacing: 1px; }}
            .nav-icon:hover, .nav-icon.active {{ opacity: 1; transform: scale(1.15); filter: drop-shadow(0 0 12px var(--accent)); }}
            .nav-icon.active::after {{ content:''; position:absolute; right:-25px; top:50%; transform:translateY(-50%); width:4px; height:24px; background:var(--accent); border-radius:4px; box-shadow: 0 0 15px var(--accent); }}
            .nav-icon:hover span {{ opacity:1; transform:translateY(5px); }}

            .main-content {{ flex-grow: 1; margin-left: 130px; display: flex; flex-direction: column; height: 100%; overflow: hidden; transition: 0.3s; position: relative; }}
            .top-header {{ padding: 30px 40px; display: flex; justify-content: space-between; align-items: center; min-height: 100px; }}
            .page-title {{ font-size: 32px; font-weight: 900; text-transform: uppercase; letter-spacing: -1.5px; color:white; text-shadow: 0 0 20px rgba(0,210,255,0.3); }}
            
            .scroll-area {{ flex-grow: 1; overflow-y: auto; padding: 0 40px 50px 40px; }}
            
            /* SMOOTH VIEW TRANSITIONS */
            @keyframes slideUpFade {{ from {{ opacity: 0; transform: translateY(30px) scale(0.98); }} to {{ opacity: 1; transform: translateY(0) scale(1); }} }}
            .view {{ display: none; }}
            .view.active {{ display: block; animation: slideUpFade 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
            .sub-content {{ display: none; }}
            .sub-content.active {{ display: block; animation: slideUpFade 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}

            .mobile-menu-btn {{ display: none; background: rgba(0, 210, 255, 0.1); border: 1px solid var(--accent); color: var(--accent); font-family: 'Montserrat', sans-serif; font-weight: 800; text-transform: uppercase; padding: 10px 15px; border-radius: 8px; font-size: 11px; cursor: pointer; transition: 0.2s; box-shadow: 0 0 15px rgba(0,210,255,0.15); }}

            /* HERO BANNER - CINEMATIC ENHANCEMENT */
            .hero-wrap {{ position: relative; width: 100%; min-height: 48vh; border-radius: 32px; overflow: hidden; margin-bottom: 40px; display: flex; align-items: center; justify-content: center; text-align:center; padding: 40px 20px; background: url('{ev_banner}') center/cover no-repeat; box-shadow: 0 20px 50px rgba(0,0,0,0.6), inset 0 0 0 1px rgba(255,255,255,0.1); }}
            .hero-wrap::before {{ content:''; position:absolute; top:0; left:0; width:100%; height:100%; background: linear-gradient(180deg, rgba(2,6,23,0.3) 0%, rgba(2,6,23,0.9) 100%); z-index: 1; }}
            .hero-content {{ position: relative; z-index: 3; display: flex; flex-direction: column; align-items: center; width: 100%; max-width: 900px; }}
            .hero-title {{ font-size: 75px; font-weight: 900; line-height: 1.05; margin: 0 0 15px 0; text-transform:uppercase; letter-spacing: -3px; text-shadow: 0 10px 40px rgba(0,0,0,0.9), 0 0 20px rgba(255,255,255,0.1); color: #fff; }}
            .hero-date {{ display: inline-block; background: rgba(0,210,255,0.1); border: 1px solid rgba(0,210,255,0.4); padding: 10px 25px; border-radius: 50px; font-size: 15px; color: var(--accent); font-weight: 800; margin-bottom: 35px; letter-spacing: 3px; text-transform: uppercase; backdrop-filter: blur(10px); box-shadow: 0 8px 20px rgba(0,0,0,0.5), inset 0 0 15px rgba(0,210,255,0.1); }}
            
            /* NEON COUNTDOWN */
            .countdown-box {{ display:flex; gap:25px; justify-content:center; flex-wrap:wrap; }}
            .cd-item {{ background: rgba(2, 6, 23, 0.45); border: 1px solid rgba(255,255,255,0.1); border-top: 1px solid rgba(0, 210, 255, 0.4); padding: 20px 30px; border-radius: 20px; backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); min-width: 110px; box-shadow: 0 15px 35px rgba(0,0,0,0.5); transition: transform 0.3s ease; }}
            .cd-item:hover {{ transform: translateY(-5px); border-color: rgba(0, 210, 255, 0.5); box-shadow: 0 20px 40px rgba(0, 210, 255, 0.15); }}
            .cd-num {{ font-size: 50px; font-weight: 900; color: #fff; line-height: 1; text-shadow: 0 0 25px rgba(0,210,255,0.8); font-variant-numeric: tabular-nums; }}
            .cd-lbl {{ font-size: 11px; font-weight: 800; color: var(--txt-s); text-transform: uppercase; letter-spacing: 3px; margin-top: 8px; }}

            /* MODERN TABS */
            .sub-tabs-wrapper {{ display: flex; gap: 35px; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 35px; overflow-x: auto; white-space: nowrap; padding-bottom: 5px; justify-content:center; }}
            .sub-tab {{ font-size: 13px; font-weight: 800; color: var(--txt-s); text-transform: uppercase; padding-bottom: 15px; cursor: pointer; transition: all 0.3s ease; position: relative; letter-spacing: 2px; }}
            .sub-tab:hover {{ color: white; }}
            .sub-tab.active {{ color: var(--accent); text-shadow: 0 0 15px rgba(0,210,255,0.4); }}
            .sub-tab.active::after {{ content: ''; position: absolute; bottom: -1px; left: 0; width: 100%; height: 3px; background: var(--accent); border-radius: 3px 3px 0 0; box-shadow: 0 -2px 15px var(--accent); }}
            
            .crm-toolbar {{ display: flex; gap: 15px; margin-bottom: 30px; flex-wrap: wrap; align-items: center; justify-content:flex-end; }}
            .crm-sel {{ background: rgba(15,23,42,0.6); backdrop-filter: blur(10px); color: white; border: 1px solid var(--card-border); padding: 12px 20px; border-radius: 12px; font-family: 'Montserrat', sans-serif; font-size: 11px; font-weight: 800; outline: none; cursor: pointer; transition: 0.3s ease; text-transform: uppercase; letter-spacing: 1px; }}
            .crm-sel:hover, .crm-sel:focus {{ border-color: var(--accent); box-shadow: 0 0 15px rgba(0,210,255,0.1); }}
            .crm-sel option {{ background: #0f172a; color: white; }}

            .g-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 25px; }}
            
            /* GLASSMORPHISM CRM CARDS */
            .crm-card {{ background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.05); border-top: 1px solid rgba(255, 255, 255, 0.1); border-radius: 24px; padding: 30px 25px; text-align: center; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); position: relative; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
            .crm-card:hover {{ transform: translateY(-8px) scale(1.02); border-top: 1px solid rgba(0, 210, 255, 0.5); border-color: rgba(0, 210, 255, 0.2); box-shadow: 0 20px 40px rgba(0,0,0,0.8), inset 0 0 20px rgba(0, 210, 255, 0.05); }}
            .crm-ava-wrap {{ width: 100px; height: 100px; margin: 0 auto 20px auto; border-radius: 50%; padding: 4px; background-clip: content-box, border-box; display: flex; justify-content: center; align-items: center; box-shadow: 0 10px 25px rgba(0,0,0,0.6); transition: 0.3s; }}
            .crm-card:hover .crm-ava-wrap {{ transform: scale(1.05); filter: drop-shadow(0 0 15px rgba(0,210,255,0.3)); }}
            .crm-ava-img {{ width: 100%; height: 100%; object-fit: cover; border-radius: 50%; border: 3px solid #0f172a; }}
            
            .foll-badge {{ background: rgba(2,6,23,0.5); padding: 8px 15px; border-radius: 10px; font-size: 14px; font-weight: 900; color: var(--txt); display: inline-flex; align-items: center; gap: 5px; margin-top: 5px; border: 1px solid rgba(255,255,255,0.08); box-shadow: 0 4px 15px rgba(0,0,0,0.3); }}
            .foll-badge span {{ color: var(--txt-s); font-size: 10px; font-weight: 800; margin-right: 2px; }}
            .er-tag {{ color: var(--accent); font-size: 10px; margin-left: 6px; font-weight: 900; border-left: 1px solid rgba(255,255,255,0.1); padding-left: 8px; }}
            
            .s-link {{ width:22px; height:22px; opacity:0.5; transition:all 0.3s cubic-bezier(0.16, 1, 0.3, 1); display:block; }}
            .s-link svg {{ fill:white; width:100%; }}
            .s-link:hover {{ opacity:1; transform:scale(1.25) translateY(-3px); }}
            .s-link:hover svg {{ fill:var(--accent); filter: drop-shadow(0 0 8px var(--accent)); }}

            /* CALENDAR GLASSMORPHISM */
            .cal-wrapper {{ overflow-x: auto; padding-bottom: 20px; }} 
            .cal-grid {{ display: grid; grid-template-columns: repeat(7, minmax(160px, 1fr)); gap: 18px; }} 
            .day-c {{ border-top: 1px solid rgba(255,255,255,0.05); min-height: 150px; padding: 15px 10px 10px 10px; display:flex; flex-direction:column; gap:10px; background: rgba(255,255,255,0.01); border-radius: 0 0 12px 12px; }}
            
            .card {{ background: rgba(15,23,42,0.5); backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.05); padding: 18px; border-radius: 14px; font-size: 12px; border-left: 4px solid var(--accent); cursor: pointer; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); display:flex; flex-direction:column; gap:8px; box-shadow: 0 8px 20px rgba(0,0,0,0.4); position:relative; }}
            .card:hover {{ transform:translateY(-5px) scale(1.02); border-color: rgba(255,255,255,0.2); border-left-color: var(--accent); box-shadow: 0 12px 30px rgba(0,0,0,0.6), inset 0 0 15px rgba(0,210,255,0.05); }}
            
            .card-preview-wrap {{ max-height: 0; opacity: 0; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden; border-radius: 8px; width: 100%; }}
            .card:hover .card-preview-wrap {{ max-height: 120px; opacity: 1; margin-top: 6px; margin-bottom: 2px; }}
            .card-preview-img {{ width: 100%; height: 100px; object-fit: cover; background: #0b1120; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; display: block; }}

            /* COMMAND BAR */
            .command-bar {{ display: flex; align-items: center; gap: 15px; background: rgba(15,23,42,0.6); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); padding: 10px 25px; border-radius: 50px; border: 1px solid rgba(255,255,255,0.08); display:none; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
            .search-box {{ border-right:1px solid rgba(255,255,255,0.1); padding-right:15px; display:flex; align-items:center; flex-grow: 1; }}
            .search-i {{ background:transparent; border:none; color:white; font-family:'Montserrat'; font-weight:700; width:150px; outline:none; font-size:12px; margin-left: 8px; }}
            .search-i::placeholder {{ color: rgba(255,255,255,0.3); }}
            .filters-wrap {{ display: flex; gap: 15px; }}
            .dd-btn {{ background: transparent; border: none; cursor: pointer; color: var(--txt-s); font-weight: 800; font-size: 11px; text-transform: uppercase; transition:0.2s; white-space: nowrap; letter-spacing: 1px; }}
            .dd-btn:hover {{ color: var(--accent); text-shadow: 0 0 10px rgba(0,210,255,0.5); }}
            .dd-menu {{ display: none; position: absolute; top: 140%; right: 0; background: rgba(15,23,42,0.95); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); width: 200px; z-index:200; border-radius:16px; overflow:hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.8); max-height: 300px; overflow-y: auto; }}
            .dd-menu.show {{ display: block; animation: slideUpFade 0.2s ease forwards; }}
            .f-opt {{ padding: 12px 20px; font-size: 11px; font-weight: 700; cursor: pointer; border-bottom: 1px solid rgba(255,255,255,0.03); transition: 0.2s; }}
            .f-opt:hover {{ background: rgba(0,210,255,0.1); color: var(--accent); padding-left: 25px; }}
            .f-opt.active {{ background: var(--accent); color: #030712; }}

            /* MODAL PREMIUM */
            .over {{ position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(2,6,23,0.8); backdrop-filter: blur(15px); display: none; justify-content: center; align-items: center; z-index: 1000; padding: 20px; }}
            .box {{ background: rgba(15,23,42,0.85); border: 1px solid rgba(255,255,255,0.1); border-top: 1px solid var(--accent); padding: 50px; border-radius: 32px; width: 100%; max-width: 600px; max-height:85vh; overflow-y:auto; position: relative; box-shadow: 0 30px 60px rgba(0,0,0,0.9), 0 0 40px rgba(0,210,255,0.1); animation: slideUpFade 0.4s cubic-bezier(0.16, 1, 0.3, 1); }}
            .m-btns {{ display:flex; gap:15px; flex-wrap: wrap; margin-top: 30px; }}
            .btn-m {{ flex: 1; min-width: 150px; padding: 16px; border-radius: 50px; text-align: center; text-decoration: none; font-weight: 800; font-size: 12px; text-transform: uppercase; color: white; background: rgba(255,255,255,0.05); transition:all 0.3s ease; border: 1px solid rgba(255,255,255,0.1); letter-spacing: 1px; }}
            .btn-m:hover {{ background: rgba(255,255,255,0.1); transform: translateY(-2px); }}
            .btn-m.primary {{ background: var(--accent); color: #030712; border: none; box-shadow: 0 10px 20px rgba(0,210,255,0.3); }}
            .btn-m.primary:hover {{ background: #fff; box-shadow: 0 15px 30px rgba(255,255,255,0.4); }}

            @media (max-width: 992px) {{
                .hero-title {{ font-size: 55px; }}
                .countdown-box {{ gap: 15px; }}
                .cd-item {{ min-width: 90px; padding: 15px 20px; }}
                .cd-num {{ font-size: 35px; }}
            }}
            @media (max-width: 768px) {{
                .sidebar {{ width: 100%; height: 75px; max-height: 75px; top: auto; bottom: 0; left: 0; transform: none; flex-direction: row; justify-content: space-evenly; border-radius: 24px 24px 0 0; margin-left: 0; padding: 10px 0; border-bottom: none; border-left: none; border-right: none; }}
                .brand-logo, .nav-icon span {{ display: none; }} 
                .nav-icon.active::after {{ right: 50%; top: -15px; transform: translateX(50%); width: 24px; height: 4px; }}
                .main-content {{ margin-left: 0; padding-bottom: 90px; }}
                .top-header {{ padding: 20px; min-height: 80px; }}
                .scroll-area {{ padding: 0 20px 20px 20px; }}
                .command-bar {{ display: none !important; position: absolute; top: 80px; left: 20px; right: 20px; width: auto; background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(25px); border: 1px solid rgba(0,210,255,0.3); border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.9); z-index: 300; flex-direction: column; align-items: stretch; padding: 25px; gap: 20px; }}
                .command-bar.mobile-active {{ display: flex !important; }}
                .search-box {{ border-right: none; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px; padding-right: 0; }}
                .filters-wrap {{ flex-direction: column; width: 100%; }}
                .dd-btn {{ width: 100%; text-align: left; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 12px; font-size: 13px; }}
                .dd-menu {{ position: static; width: 100%; background: rgba(0,0,0,0.2); box-shadow: none; margin-top: 10px; border: none; }}
                .hero-wrap {{ border-radius: 24px; padding: 30px 15px; }}
                .hero-title {{ font-size: 40px; letter-spacing: -1px; }}
                .box {{ padding: 30px; border-radius: 24px; }}
            }}
        </style>
    </head>
    <body>
        <div class="sidebar">
            <img src="{LOGO_SRC}" class="brand-logo" onerror="this.style.display='none'">
            <div class="nav-icon active" onclick="go('home', this, 'Dashboard SPACE')" title="Resumen del Evento">
                🏠 <span>Resumen</span>
            </div>
            <div class="nav-icon" onclick="go('marketing', this, 'Calendario de Contenido')" title="Calendario">
                📅 <span>Calendario</span>
            </div>
        </div>

        <div class="main-content">
            <div class="top-header">
                <div id="pageTitle" class="page-title">Dashboard SPACE</div>
                <button class="mobile-menu-btn" id="mobileMenuBtn" onclick="toggleMobileFilters()">☰ Filtros</button>
                <div class="command-bar" id="filterBar">
                    <div class="search-box">🔍 <input type="text" id="gSearch" class="search-i" placeholder="Buscar contenido..." onkeyup="doSearch()"></div>
                    <div class="filters-wrap">
                        <div style="position:relative;"><button onclick="tog(this)" class="dd-btn">Mes ▾</button><div class="dd-menu">{html_meses}</div></div>
                        <div style="position:relative;"><button onclick="tog(this)" class="dd-btn">Tipo ▾</button><div class="dd-menu">{html_tipos}</div></div>
                        <div style="position:relative;"><button onclick="tog(this)" class="dd-btn">Formato ▾</button><div class="dd-menu">{html_formatos}</div></div>
                        <div style="position:relative;"><button onclick="tog(this)" class="dd-btn">Estado ▾</button><div class="dd-menu">{html_estados}</div></div>
                    </div>
                </div>
            </div>

            <div class="scroll-area">
                <div id="view-home" class="view active">
                    <div class="hero-wrap">
                        <div class="hero-content">
                            <h1 class="hero-title">{ev_nombre}</h1>
                            <div class="hero-date">📅 {ev_fecha_display}</div>
                            
                            <div class="countdown-box">
                                <div class="cd-item"><div class="cd-num" id="cd-days">00</div><div class="cd-lbl">Días</div></div>
                                <div class="cd-item"><div class="cd-num" id="cd-hours">00</div><div class="cd-lbl">Hrs</div></div>
                                <div class="cd-item"><div class="cd-num" id="cd-mins">00</div><div class="cd-lbl">Min</div></div>
                                <div class="cd-item"><div class="cd-num" id="cd-secs">00</div><div class="cd-lbl">Seg</div></div>
                            </div>
                        </div>
                    </div>

                    <div class="sub-tabs-wrapper">
                        <div class="sub-tab active" onclick="switchSubTab('influencers', this)">Influencers</div>
                        <div class="sub-tab" onclick="switchSubTab('artistas', this)">Artistas</div>
                        <div class="sub-tab" onclick="switchSubTab('medios', this)">Medios</div>
                    </div>

                    <div id="sub-influencers" class="sub-content active">
                        <div class="crm-toolbar">
                            <select id="inf-sort" class="crm-sel" onchange="applyCrmFilters('influencers')">
                                <option value="default">Orden por Defecto</option>
                                <option value="ig_desc">IG Seguidores (Mayor a Menor)</option>
                                <option value="ig_asc">IG Seguidores (Menor a Mayor)</option>
                                <option value="tk_desc">TK Seguidores (Mayor a Menor)</option>
                                <option value="tk_asc">TK Seguidores (Menor a Mayor)</option>
                            </select>
                        </div>
                        <div class="g-grid" id="grid-influencers">{influencers_html}</div>
                    </div>

                    <div id="sub-artistas" class="sub-content">
                        <div class="crm-toolbar">
                            <select id="art-sort" class="crm-sel" onchange="applyCrmFilters('artistas')">
                                <option value="default">Orden por Defecto</option>
                                <option value="ig_desc">IG Seguidores (Mayor a Menor)</option>
                                <option value="ig_asc">IG Seguidores (Menor a Mayor)</option>
                                <option value="tk_desc">TK Seguidores (Mayor a Menor)</option>
                                <option value="tk_asc">TK Seguidores (Menor a Mayor)</option>
                            </select>
                        </div>
                        <div class="g-grid" id="grid-artistas">{artistas_html}</div>
                    </div>

                    <div id="sub-medios" class="sub-content">
                        <div class="crm-toolbar">
                            <select id="med-sort" class="crm-sel" onchange="applyCrmFilters('medios')">
                                <option value="default">Orden por Defecto</option>
                                <option value="ig_desc">IG Seguidores (Mayor a Menor)</option>
                                <option value="ig_asc">IG Seguidores (Menor a Mayor)</option>
                                <option value="tk_desc">TK Seguidores (Mayor a Menor)</option>
                                <option value="tk_asc">TK Seguidores (Menor a Mayor)</option>
                            </select>
                        </div>
                        <div class="g-grid" id="grid-medios">{medios_html}</div>
                    </div>
                </div>

                <div id="view-marketing" class="view">
                    {marketing_html}
                </div>
            </div>
        </div>

        <div id="modal" class="over" onclick="closeM(event)">
            <div class="box">
                <h2 id="mT" style="margin-top:0; color:white; font-size:26px; margin-bottom:15px; font-weight:900; letter-spacing:-1px;"></h2>
                <div id="mSubTag" style="display:inline-block; background:rgba(0,210,255,0.1); padding:8px 15px; border-radius:8px; font-size:11px; font-weight:800; margin-bottom:25px; color:var(--accent); border: 1px solid rgba(0,210,255,0.3); text-transform:uppercase; letter-spacing:1px;"></div>
                <div id="mDesc" style="font-size: 15px; color: var(--txt-s); line-height: 1.7; margin-bottom:25px; background:rgba(0,0,0,0.2); padding:20px; border-radius:16px; border: 1px solid rgba(255,255,255,0.05);"></div>
                <div class="m-btns" id="mActions"></div>
            </div>
        </div>

        <script>
            const APP_DATA = {app_data_json};
            let currentView = 'home';

            // JS COUNTDOWN ENGINE
            const targetDateStr = "{ev_fecha_js}";
            if (targetDateStr) {{
                const countDownDate = new Date(targetDateStr).getTime();
                const x = setInterval(function() {{
                    const now = new Date().getTime();
                    const distance = countDownDate - now;
                    
                    if (distance < 0) {{
                        clearInterval(x);
                        document.getElementById("cd-days").innerHTML = "00";
                        document.getElementById("cd-hours").innerHTML = "00";
                        document.getElementById("cd-mins").innerHTML = "00";
                        document.getElementById("cd-secs").innerHTML = "00";
                        return;
                    }}
                    
                    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                    const seconds = Math.floor((distance % (1000 * 60)) / 1000);
                    
                    document.getElementById("cd-days").innerHTML = days.toString().padStart(2, '0');
                    document.getElementById("cd-hours").innerHTML = hours.toString().padStart(2, '0');
                    document.getElementById("cd-mins").innerHTML = minutes.toString().padStart(2, '0');
                    document.getElementById("cd-secs").innerHTML = seconds.toString().padStart(2, '0');
                }}, 1000);
            }}

            function go(id, el, title) {{
                currentView = id;
                document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
                document.querySelectorAll('.nav-icon').forEach(n => n.classList.remove('active'));
                
                // Forzar reflow para reiniciar animación
                const view = document.getElementById('view-'+id);
                void view.offsetWidth; 
                view.classList.add('active');
                
                el.classList.add('active');
                document.getElementById('pageTitle').innerText = title;
                window.scrollTo(0, 0);
                handleResize(); 
            }}

            function switchSubTab(id, el) {{
                document.querySelectorAll('.sub-content').forEach(c => c.classList.remove('active'));
                document.querySelectorAll('.sub-tab').forEach(t => t.classList.remove('active'));
                
                const content = document.getElementById('sub-'+id);
                void content.offsetWidth;
                content.classList.add('active');
                
                el.classList.add('active');
            }}

            function handleResize() {{
                const fb = document.getElementById('filterBar');
                const mb = document.getElementById('mobileMenuBtn');
                if (currentView === 'marketing') {{
                    if (window.innerWidth <= 768) {{
                        mb.style.display = 'block';
                        fb.style.display = fb.classList.contains('mobile-active') ? 'flex' : 'none';
                    }} else {{
                        mb.style.display = 'none';
                        fb.style.display = 'flex'; 
                        fb.classList.remove('mobile-active');
                    }}
                }} else {{
                    mb.style.display = 'none';
                    fb.style.display = 'none';
                    fb.classList.remove('mobile-active');
                }}
            }}

            function toggleMobileFilters() {{
                const fb = document.getElementById('filterBar');
                fb.classList.toggle('mobile-active');
                handleResize();
            }}
            window.addEventListener('resize', handleResize);
            handleResize();

            function applyCrmFilters(section) {{
                let grid = document.getElementById('grid-' + section);
                if(!grid) return;
                
                let sortId = '';
                if (section === 'influencers') sortId = 'inf-sort';
                if (section === 'artistas') sortId = 'art-sort';
                if (section === 'medios') sortId = 'med-sort';
                let sortVal = document.getElementById(sortId).value;
                
                let cards = Array.from(grid.querySelectorAll('.crm-card'));
                if(sortVal !== 'default') {{
                    cards.sort((a, b) => {{
                        let key = sortVal.includes('ig') ? 'data-ig' : 'data-tk';
                        let mult = sortVal.includes('desc') ? -1 : 1;
                        let valA = parseInt(a.getAttribute(key)) || 0;
                        let valB = parseInt(b.getAttribute(key)) || 0;
                        return (valA - valB) * mult;
                    }});
                }}
                cards.forEach(c => grid.appendChild(c)); 
            }}

            function openM(id) {{
                const d = APP_DATA[id]; if(!d) return;
                document.getElementById('mT').innerText = d.tit;
                document.getElementById('mSubTag').innerText = d.tag;
                document.getElementById('mDesc').innerHTML = d.desc + (d.copy ? '<br><br><b style="color:var(--accent); font-weight:900; text-transform:uppercase; letter-spacing:1px; font-size:12px;">Post Copy:</b><br><span style="color:white;">'+d.copy+'</span>' : '');
                const acts = document.getElementById('mActions'); acts.innerHTML = '';
                if(d.links) d.links.forEach(l => {{
                    const a = document.createElement('a'); a.href = l.url; a.target = '_blank'; a.className = 'btn-m ' + (l.pri ? 'primary' : ''); a.innerText = l.lbl; acts.appendChild(a);
                }});
                document.getElementById('modal').style.display = 'flex';
            }}
            function closeM(e) {{ if(e.target.id === 'modal') e.target.style.display = 'none'; }}
            function tog(btn) {{ let m=btn.nextElementSibling; document.querySelectorAll('.dd-menu').forEach(d=>{{if(d!==m) d.classList.remove('show');}}); m.classList.toggle('show'); }}
            
            let F = {{ mes:[], tipo:[], sub: [], post: [] }};
            function toggleF(cat, val, el) {{ el.classList.toggle('active'); if(el.classList.contains('active')) F[cat].push(val); else F[cat] = F[cat].filter(x=>x!==val); doSearch(); }}
            function doSearch() {{
                let q = document.getElementById('gSearch').value.toLowerCase();
                
                document.querySelectorAll('.month-wrapper').forEach(mw => {{
                    let m = mw.getAttribute('data-mes');
                    mw.style.display = (!F.mes.length || F.mes.includes(m)) ? 'block' : 'none';
                }});

                document.querySelectorAll('.s-item').forEach(item => {{
                    let t = item.getAttribute('data-ftipo'), s = item.getAttribute('data-fsub'), p = item.getAttribute('data-fpost'), txt = item.getAttribute('data-tit').toLowerCase();
                    let okT = !F.tipo.length || F.tipo.includes(t);
                    let okS = !F.sub.length || F.sub.includes(s);
                    let okP = !F.post.length || F.post.includes(p);
                    let okTxt = q === '' || txt.includes(q);
                    item.style.display = (okT && okS && okP && okTxt) ? 'flex' : 'none';
                }});
            }}
        </script>
    </body>
    </html>
    """
    return html
