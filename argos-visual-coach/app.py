from flask import Flask, render_template, jsonify
import random
import datetime

app = Flask(__name__)

# ─── Dados simulados dos ambientes ───────────────────────────────────────────
PREDIOS = ['A', 'B', 'C', 'D']

AMBIENTES_BASE = [
    { 'id': 'cant-col',  'icon': '🍽️', 'nome': 'Cantina Coletiva',       'detalhe': 'Área comum',               'cap': 55,  'cameras': 3 },
    { 'id': 'cant-func', 'icon': '☕',  'nome': 'Cantina Funcionários',   'detalhe': 'Acesso restrito',           'cap': 30,  'cameras': 2 },
    { 'id': 'audit',     'icon': '🎤',  'nome': 'Auditório',              'detalhe': 'Eventos e reuniões',        'cap': 120, 'cameras': 4 },
    { 'id': 'corredor',  'icon': '🚶',  'nome': 'Corredores',             'detalhe': 'Fluxo de passagem',         'cap': 200, 'cameras': 8 },
    { 'id': 'estac',     'icon': '🅿️',  'nome': 'Estacionamento',         'detalhe': 'Vagas cobertas',            'cap': 80,  'cameras': 6 },
    { 'id': 'dejetos',   'icon': '♻️',  'nome': 'Área de Dejetos',        'detalhe': 'Recicláveis / N-Recicláveis','cap': 10, 'cameras': 2 },
    { 'id': 'maquinas',  'icon': '⚙️',  'nome': 'Centro de Máquinas',     'detalhe': 'Infraestrutura',            'cap': 20,  'cameras': 3 },
    { 'id': 'equiptos',  'icon': '🖥️',  'nome': 'Centro de Equipamentos', 'detalhe': 'TI e eletrônicos',          'cap': 15,  'cameras': 2 },
    { 'id': 'seguranca', 'icon': '🔒',  'nome': 'Centro de Segurança',    'detalhe': 'Monitoramento 24h',         'cap': 12,  'cameras': 4 },
    { 'id': 'colabor',   'icon': '👥',  'nome': 'Área de Colaboradores',  'detalhe': 'Vestiários e descanso',     'cap': 50,  'cameras': 2 },
]

CAMERAS_BASE = [
    ('ENTRADA',       '🏢'),
    ('CANTINA',       '🍽️'),
    ('ESTACIONAMENTO','🅿️'),
    ('CORREDOR',      '🚶'),
]

EVENTOS_BASE = [
    {'tipo': 'crit', 'titulo': 'Acesso negado — credencial inválida',    'local': 'ESTACIONAMENTO'},
    {'tipo': 'warn', 'titulo': 'Ocupação acima de 90%',                   'local': 'CANTINA FUNCIONÁRIOS'},
    {'tipo': 'warn', 'titulo': 'Manutenção agendada — máquinas',          'local': 'CTR. MÁQUINAS'},
    {'tipo': 'ok',   'titulo': 'Biometria validada — colaborador',         'local': 'ENTRADA PRINCIPAL'},
    {'tipo': 'ok',   'titulo': 'QR Code gerado — visitante',               'local': 'TOTEM RECEPÇÃO'},
    {'tipo': 'warn', 'titulo': 'Câmera offline temporariamente',           'local': 'CORREDOR L3'},
    {'tipo': 'ok',   'titulo': 'Acesso autorizado — auditório',            'local': 'AUDITÓRIO PRINCIPAL'},
    {'tipo': 'warn', 'titulo': 'Descarte irregular identificado',          'local': 'ÁREA DE DEJETOS'},
]


def get_status(pessoas, cap):
    ratio = pessoas / cap
    if ratio >= 0.90:
        return 'crit'
    elif ratio >= 0.70:
        return 'warn'
    else:
        return 'ok'


def build_ambientes():
    result = []
    for a in AMBIENTES_BASE:
        pessoas = random.randint(1, a['cap'])
        status = get_status(pessoas, a['cap'])
        result.append({**a, 'pessoas': pessoas, 'status': status})
    return result


def build_cameras():
    cams = []
    for i, predio in enumerate(PREDIOS):
        for j, (nome, icon) in enumerate(CAMERAS_BASE):
            num = i * len(CAMERAS_BASE) + j + 1
            cams.append({
                'num': f'{num:02d}',
                'icon': icon,
                'nome': f'CAM-{num:02d} · {nome} {predio}',
                'predio': f'PRÉDIO {predio}',
                'status': random.choice(['ok', 'ok', 'ok', 'warn']),
                'res': random.choice(['1080p', '4K']),
                'fps': '25fps',
                'uptime': f'{random.uniform(97,100):.1f}%',
                'eventos': random.randint(0, 15),
            })
    return cams


def build_eventos():
    result = []
    now = datetime.datetime.now()
    for i, ev in enumerate(EVENTOS_BASE):
        t = now - datetime.timedelta(minutes=i * 37 + random.randint(0, 10))
        result.append({
            **ev,
            'hora': t.strftime('%H:%M'),
            'local': f'PRÉDIO {random.choice(PREDIOS)} · {ev["local"]}',
        })
    return result


# ─── Rotas ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    ambientes = build_ambientes()
    cameras   = build_cameras()
    eventos   = build_eventos()
    total_pess = sum(a['pessoas'] for a in ambientes)
    criticos   = sum(1 for a in ambientes if a['status'] == 'crit')
    return render_template('index.html',
        ambientes=ambientes,
        cameras=cameras,
        eventos=eventos,
        total_pessoas=total_pess,
        total_cameras=len(cameras),
        total_eventos=len(eventos),
        criticos=criticos,
        predios=PREDIOS,
    )


@app.route('/api/status')
def api_status():
    """Endpoint JSON para atualização em tempo real (polling)."""
    ambientes = build_ambientes()
    return jsonify({
        'timestamp': datetime.datetime.now().strftime('%H:%M:%S'),
        'total_pessoas': sum(a['pessoas'] for a in ambientes),
        'ambientes': ambientes,
        'cameras_ok': random.randint(46, 48),
        'alertas': sum(1 for a in ambientes if a['status'] in ('warn', 'crit')),
    })


@app.route('/api/eventos')
def api_eventos():
    return jsonify(build_eventos())


if __name__ == '__main__':
    # host='0.0.0.0' → acessível pelo celular na mesma rede Wi-Fi
    app.run(host='0.0.0.0', port=5000, debug=True)
