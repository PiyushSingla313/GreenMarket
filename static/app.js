// ============================================================
// GreenMarket — Shared App JS
// Language (EN/HI), nav toggle, language selector modal
// ============================================================

// ---- API HELPER ----
const API_BASE = '/api';

function authToken() {
  return localStorage.getItem('gm_token');
}

function currentUser() {
  const raw = localStorage.getItem('gm_user');
  return raw ? JSON.parse(raw) : null;
}

function setSession(token, user) {
  localStorage.setItem('gm_token', token);
  localStorage.setItem('gm_user', JSON.stringify(user));
}

function clearSession() {
  localStorage.removeItem('gm_token');
  localStorage.removeItem('gm_user');
}

async function api(path, options = {}) {
  const headers = Object.assign({ 'Content-Type': 'application/json' }, options.headers || {});
  const token = authToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, Object.assign({}, options, { headers }));
  if (!res.ok) {
    let detail = res.statusText;
    try { detail = (await res.json()).detail || detail; } catch (e) {}
    throw new Error(detail);
  }
  if (res.status === 204) return null;
  return res.json();
}

// ---- TRANSLATIONS ----
const TRANSLATIONS = {
  en: {
    nav_marketplace: "Marketplace",
    nav_prices: "Live Prices",
    nav_storage: "Cold Storage",
    nav_rentals: "Rentals & Supplies",
    nav_schemes: "Gov Schemes",
    nav_login: "Login",
    nav_join: "Join Free",

    hero_badge: "🇮🇳 Made for Indian Farmers",
    hero_title_1: "Sell Your Crops",
    hero_title_em: "Directly.",
    hero_title_2: "No Middleman.",
    hero_sub: "Connect with buyers across India, track live mandi prices, book cold storage, rent machinery, and access government schemes — all in one place.",
    hero_btn1: "Start Selling Free",
    hero_btn2: "View Live Prices →",
    hero_stat1: "Farmers",
    hero_stat2: "Trade Volume",
    hero_stat3: "States",

    feat_mp: "Direct Marketplace",
    feat_mp_sub: "List crops, set your price, connect with buyers directly across India.",
    feat_mp_link: "Open Marketplace →",
    feat_price: "Live Mandi Prices",
    feat_price_sub: "Real-time crop prices from 500+ mandis. Know your crop's worth today.",
    feat_price_link: "Check Prices →",
    feat_store: "Cold Storage",
    feat_store_sub: "Book nearby cold storage units. Preserve your harvest, sell at the right time.",
    feat_store_link: "Find Storage →",
    feat_rent: "Rent Machinery",
    feat_rent_sub: "Rent tractors, harvesters, and more. Also buy pesticides and seeds.",
    feat_rent_link: "Browse Rentals →",
    feat_scheme: "Government Schemes",
    feat_scheme_sub: "All central & state farmer schemes in one place. Apply directly online.",
    feat_scheme_link: "View Schemes →",

    listings_title: "Fresh Listings Today",
    listings_eyebrow: "MARKETPLACE",
    listings_viewall: "View All →",

    how_eyebrow: "HOW IT WORKS",
    how_title: "From Farm to Buyer in 3 Steps",
    step1_title: "Register & List",
    step1_desc: "Create your free account. List your crops with quantity, quality, and your asking price.",
    step2_title: "Buyers Contact You",
    step2_desc: "Verified buyers from across India see your listing and contact you directly. No commission.",
    step3_title: "Get Paid Directly",
    step3_desc: "Negotiate, agree, and receive payment directly to your bank account. Full profit is yours.",

    testi_eyebrow: "FARMER STORIES",
    testi_title: "Farmers Who Earn More",

    cta_title: "Ready to earn what your crops deserve?",
    cta_sub: "Join 12,400+ farmers already selling directly. Free forever for farmers.",
    cta_btn1: "Register as Farmer",
    cta_btn2: "Register as Buyer",

    footer_tagline: "Empowering farmers with technology. No middlemen, no commissions, just fair prices.",
    footer_platform: "Platform",
    footer_support: "Support",
    footer_connect: "Connect",
    footer_copy: "© 2025 GreenMarket. Made with ❤️ for Indian Farmers.",
    footer_langs: "Available in: Hindi • Punjabi • Marathi • Telugu • Tamil",

    lang_modal_title: "Choose Your Language",
    lang_modal_sub: "Select your preferred language to continue",
  },
  hi: {
    nav_marketplace: "बाज़ार",
    nav_prices: "मंडी भाव",
    nav_storage: "शीत भंडार",
    nav_rentals: "किराया व आपूर्ति",
    nav_schemes: "सरकारी योजनाएं",
    nav_login: "लॉगिन",
    nav_join: "निःशुल्क जुड़ें",

    hero_badge: "🇮🇳 भारतीय किसानों के लिए",
    hero_title_1: "अपनी फसल बेचें",
    hero_title_em: "सीधे।",
    hero_title_2: "बिना बिचौलिए के।",
    hero_sub: "पूरे भारत के खरीदारों से जुड़ें, मंडी भाव ट्रैक करें, शीत भंडार बुक करें, मशीनरी किराए पर लें और सरकारी योजनाओं तक पहुंचें — सब एक जगह।",
    hero_btn1: "मुफ़्त बेचना शुरू करें",
    hero_btn2: "मंडी भाव देखें →",
    hero_stat1: "किसान",
    hero_stat2: "व्यापार मात्रा",
    hero_stat3: "राज्य",

    feat_mp: "सीधा बाज़ार",
    feat_mp_sub: "फसल सूचीबद्ध करें, अपनी कीमत तय करें, सीधे खरीदारों से जुड़ें।",
    feat_mp_link: "बाज़ार खोलें →",
    feat_price: "लाइव मंडी भाव",
    feat_price_sub: "500+ मंडियों से रियल-टाइम फसल कीमतें। आज अपनी फसल का मूल्य जानें।",
    feat_price_link: "भाव देखें →",
    feat_store: "शीत भंडार",
    feat_store_sub: "पास का शीत भंडार बुक करें। फसल सुरक्षित रखें, सही समय पर बेचें।",
    feat_store_link: "भंडार खोजें →",
    feat_rent: "मशीनरी किराया",
    feat_rent_sub: "ट्रैक्टर, हार्वेस्टर किराए पर लें। कीटनाशक और बीज भी खरीदें।",
    feat_rent_link: "किराया देखें →",
    feat_scheme: "सरकारी योजनाएं",
    feat_scheme_sub: "सभी केंद्र व राज्य किसान योजनाएं एक जगह। सीधे ऑनलाइन आवेदन करें।",
    feat_scheme_link: "योजनाएं देखें →",

    listings_title: "आज की नई सूचियां",
    listings_eyebrow: "बाज़ार",
    listings_viewall: "सभी देखें →",

    how_eyebrow: "यह कैसे काम करता है",
    how_title: "खेत से खरीदार तक 3 कदमों में",
    step1_title: "पंजीकरण करें और सूचीबद्ध करें",
    step1_desc: "अपना मुफ्त खाता बनाएं। मात्रा, गुणवत्ता और मांगी कीमत के साथ फसल सूचीबद्ध करें।",
    step2_title: "खरीदार आपसे संपर्क करें",
    step2_desc: "पूरे भारत के सत्यापित खरीदार आपकी सूची देखते हैं और सीधे संपर्क करते हैं। कोई कमीशन नहीं।",
    step3_title: "सीधे भुगतान पाएं",
    step3_desc: "बातचीत करें, सहमत हों और सीधे अपने बैंक खाते में भुगतान प्राप्त करें। पूरा मुनाफा आपका।",

    testi_eyebrow: "किसानों की कहानियां",
    testi_title: "अधिक कमाने वाले किसान",

    cta_title: "क्या आप अपनी फसल का सही मूल्य पाने के लिए तैयार हैं?",
    cta_sub: "12,400+ किसान पहले से सीधे बेच रहे हैं। किसानों के लिए हमेशा मुफ्त।",
    cta_btn1: "किसान के रूप में पंजीकरण करें",
    cta_btn2: "खरीदार के रूप में पंजीकरण करें",

    footer_tagline: "प्रौद्योगिकी से किसानों को सशक्त बनाना। कोई बिचौलिए नहीं, कोई कमीशन नहीं, बस उचित मूल्य।",
    footer_platform: "प्लेटफ़ॉर्म",
    footer_support: "सहायता",
    footer_connect: "जुड़ें",
    footer_copy: "© 2025 GreenMarket. भारतीय किसानों के लिए ❤️ से बनाया।",
    footer_langs: "उपलब्ध: Hindi • Punjabi • Marathi • Telugu • Tamil",

    lang_modal_title: "अपनी भाषा चुनें",
    lang_modal_sub: "जारी रखने के लिए अपनी पसंदीदा भाषा चुनें",
  }
};

// ---- STATE ----
let currentLang = localStorage.getItem('gm_lang') || null;

// ---- INIT ----
document.addEventListener('DOMContentLoaded', () => {
  if (!currentLang) {
    showLangModal();
  } else {
    applyLanguage(currentLang);
  }
  renderLangToggle();
});

// ---- LANGUAGE MODAL ----
function showLangModal() {
  const existing = document.getElementById('langModal');
  if (existing) existing.remove();

  const overlay = document.createElement('div');
  overlay.id = 'langModal';
  overlay.style.cssText = `
    position:fixed;inset:0;background:rgba(0,0,0,0.65);z-index:9999;
    display:flex;align-items:center;justify-content:center;padding:24px;
    backdrop-filter:blur(4px);animation:fadeIn 0.2s ease;
  `;
  overlay.innerHTML = `
    <div style="background:#fff;border-radius:20px;padding:48px 40px;max-width:480px;width:100%;text-align:center;box-shadow:0 24px 64px rgba(0,0,0,0.25);">
      <div style="font-size:52px;margin-bottom:16px;">🌾</div>
      <h2 style="font-family:'Syne',sans-serif;font-size:26px;font-weight:800;color:#1b5e20;margin-bottom:8px;">GreenMarket</h2>
      <p style="font-size:15px;color:#777;margin-bottom:8px;">Choose your language / अपनी भाषा चुनें</p>
      <p style="font-size:13px;color:#aaa;margin-bottom:36px;">You can change this anytime from the top bar</p>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
        <button onclick="selectLang('en')" style="
          padding:20px;border-radius:14px;border:2px solid #e0e0e0;
          background:#fafaf8;cursor:pointer;transition:all 0.2s;font-family:'DM Sans',sans-serif;
          display:flex;flex-direction:column;align-items:center;gap:8px;">
          <span style="font-size:36px;">🇬🇧</span>
          <span style="font-size:18px;font-weight:700;color:#1a1a1a;">English</span>
          <span style="font-size:12px;color:#888;">Continue in English</span>
        </button>
        <button onclick="selectLang('hi')" style="
          padding:20px;border-radius:14px;border:2px solid #e0e0e0;
          background:#fafaf8;cursor:pointer;transition:all 0.2s;font-family:'DM Sans',sans-serif;
          display:flex;flex-direction:column;align-items:center;gap:8px;">
          <span style="font-size:36px;">🇮🇳</span>
          <span style="font-size:18px;font-weight:700;color:#1a1a1a;">हिंदी</span>
          <span style="font-size:12px;color:#888;">हिंदी में जारी रखें</span>
        </button>
      </div>
      <p style="font-size:12px;color:#bbb;margin-top:24px;">More languages coming soon: Punjabi • Marathi • Telugu • Tamil</p>
    </div>
  `;
  // hover effect via mouseover
  overlay.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('mouseenter', () => { btn.style.borderColor='#2e7d32'; btn.style.background='#e8f5e9'; btn.style.transform='translateY(-2px)'; });
    btn.addEventListener('mouseleave', () => { btn.style.borderColor='#e0e0e0'; btn.style.background='#fafaf8'; btn.style.transform='none'; });
  });
  document.body.appendChild(overlay);
}

function selectLang(lang) {
  currentLang = lang;
  localStorage.setItem('gm_lang', lang);
  const modal = document.getElementById('langModal');
  if (modal) modal.remove();
  applyLanguage(lang);
  renderLangToggle();
}

// ---- APPLY TRANSLATIONS ----
function applyLanguage(lang) {
  const t = TRANSLATIONS[lang];
  if (!t) return;
  document.querySelectorAll('[data-t]').forEach(el => {
    const key = el.getAttribute('data-t');
    if (t[key] !== undefined) el.textContent = t[key];
  });
  document.querySelectorAll('[data-t-html]').forEach(el => {
    const key = el.getAttribute('data-t-html');
    if (t[key] !== undefined) el.innerHTML = t[key];
  });
  document.querySelectorAll('[data-t-placeholder]').forEach(el => {
    const key = el.getAttribute('data-t-placeholder');
    if (t[key] !== undefined) el.placeholder = t[key];
  });
  // Update <html lang>
  document.documentElement.lang = lang;
}

// ---- LANG TOGGLE BUTTON (injected into nav) ----
function renderLangToggle() {
  const existing = document.getElementById('langToggleBtn');
  if (existing) existing.remove();

  const btn = document.createElement('button');
  btn.id = 'langToggleBtn';
  btn.title = 'Change language / भाषा बदलें';
  btn.style.cssText = `
    display:inline-flex;align-items:center;gap:6px;
    padding:7px 14px;border-radius:8px;border:1.5px solid #c8e6c9;
    background:#e8f5e9;color:#2e7d32;font-weight:700;font-size:13px;
    cursor:pointer;font-family:'DM Sans',sans-serif;transition:all 0.15s;
    flex-shrink:0;
  `;
  const flag = currentLang === 'hi' ? '🇮🇳 हिंदी' : '🇬🇧 EN';
  btn.innerHTML = flag + ' <span style="font-size:10px;opacity:0.7;">▼</span>';
  btn.addEventListener('click', showLangMenu);
  btn.addEventListener('mouseenter', () => { btn.style.background='#c8e6c9'; });
  btn.addEventListener('mouseleave', () => { btn.style.background='#e8f5e9'; });

  // Insert before the first .nav-cta or at end of nav-inner
  const navCta = document.querySelector('.nav-cta');
  const navInner = document.querySelector('.nav-inner');
  if (navCta && navInner) navInner.insertBefore(btn, navCta);
  else if (navInner) navInner.appendChild(btn);
}

function showLangMenu() {
  const existing = document.getElementById('langDropdown');
  if (existing) { existing.remove(); return; }

  const btn = document.getElementById('langToggleBtn');
  const rect = btn.getBoundingClientRect();

  const menu = document.createElement('div');
  menu.id = 'langDropdown';
  menu.style.cssText = `
    position:fixed;top:${rect.bottom + 8}px;left:${rect.left}px;
    background:#fff;border:1.5px solid #e0e0e0;border-radius:12px;
    box-shadow:0 8px 32px rgba(0,0,0,0.15);z-index:9998;
    min-width:180px;overflow:hidden;
  `;
  const langs = [
    { code:'en', label:'🇬🇧 English', sub:'Continue in English' },
    { code:'hi', label:'🇮🇳 हिंदी', sub:'हिंदी में जारी रखें' },
  ];
  langs.forEach(l => {
    const item = document.createElement('button');
    item.style.cssText = `
      width:100%;padding:12px 16px;border:none;background:${currentLang===l.code?'#e8f5e9':'#fff'};
      cursor:pointer;text-align:left;font-family:'DM Sans',sans-serif;display:flex;flex-direction:column;gap:2px;
      border-bottom:1px solid #f0f0f0;
    `;
    item.innerHTML = `<span style="font-weight:700;font-size:14px;color:${currentLang===l.code?'#2e7d32':'#1a1a1a'}">${l.label}</span><span style="font-size:12px;color:#888">${l.sub}</span>`;
    item.addEventListener('click', () => { menu.remove(); selectLang(l.code); });
    item.addEventListener('mouseenter', () => { item.style.background='#f5f5f5'; });
    item.addEventListener('mouseleave', () => { item.style.background=currentLang===l.code?'#e8f5e9':'#fff'; });
    menu.appendChild(item);
  });

  document.body.appendChild(menu);
  setTimeout(() => document.addEventListener('click', () => { menu.remove(); }, { once: true }), 50);
}

// ---- NAV TOGGLE ----
function toggleMenu() {
  const m = document.getElementById('mobileMenu');
  if (m) m.classList.toggle('open');
}
