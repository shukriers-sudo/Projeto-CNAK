# Argos Visual Coach — CNAK Vision V2
Sistema de monitoramento visual de ambientes para os 4 prédios.

---

## 📁 Estrutura do projeto

```
argos-visual-coach/
├── app.py                  ← servidor Flask (backend)
├── requirements.txt        ← dependências Python
├── templates/
│   └── index.html          ← página principal (Jinja2)
└── static/
    ├── css/
    │   └── style.css       ← estilos
    ├── js/
    │   └── app.js          ← lógica do frontend
    ├── manifest.json       ← PWA (instalar no celular)
    └── sw.js               ← service worker offline
```

---

## ▶️ Como rodar no VS Code

### 1. Abrir a pasta no VS Code
```
Arquivo → Abrir Pasta → selecione "argos-visual-coach"
```

### 2. Abrir o terminal integrado
```
Ctrl + ` (acento grave)
```

### 3. Criar ambiente virtual (recomendado)
```bash
python -m venv venv
```

#### Ativar no Windows:
```bash
venv\Scripts\activate
```

#### Ativar no Mac/Linux:
```bash
source venv/bin/activate
```

### 4. Instalar dependências
```bash
pip install -r requirements.txt
```

### 5. Rodar o servidor
```bash
python app.py
```

Você verá algo como:
```
* Running on http://0.0.0.0:5000
* Running on http://192.168.X.X:5000   ← use esse IP no celular!
```

---

## 📱 Acessar no celular (mesmo Wi-Fi)

1. Conecte o celular na **mesma rede Wi-Fi** do computador
2. No celular, abra o navegador (Chrome ou Safari)
3. Digite o endereço que apareceu no terminal, ex:
   ```
   http://192.168.1.105:5000
   ```
4. Para **instalar como app** no celular:
   - Chrome Android: menu ⋮ → "Adicionar à tela inicial"
   - Safari iOS: compartilhar → "Adicionar à Tela de Início"

---

## 🌐 Acessar no navegador do PC
```
http://localhost:5000
```

---

## 🔄 Endpoints disponíveis

| Rota            | Descrição                          |
|-----------------|------------------------------------|
| `GET /`         | Dashboard principal                |
| `GET /api/status` | JSON com ocupação em tempo real  |
| `GET /api/eventos` | JSON com log de eventos         |

---

## 🛑 Parar o servidor
```
Ctrl + C  no terminal
```

---

## ⚙️ Extensões VS Code recomendadas
- **Python** (Microsoft)
- **Flask Snippets**
- **Live Server** (opcional para HTML estático)

---

Argos Segurança · CNAK Vision V2 · Brasília/DF
