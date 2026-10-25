/* =========================================================
   app.js — منطق الموقع: اللغة، الثيم، المحاكي، الأنشطة، الاختبار، المساعد
   ========================================================= */

/* ============ 0) أدوات عامة ============ */
/* تخزين آمن: بعض المتصفحات تمنع localStorage على file:// أو في الوضع الخاص */
const store = {
    get(k, d = null) { try { const v = localStorage.getItem(k); return v === null ? d : v; } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* تجاهل */ } }
};
let LANG = store.get("qc-lang", "ar") || "ar";
const $  = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const t  = o => (o ? (o[LANG] || o.ar) : "");
const DEG = "°";

/* تحويل نص عربي/إنجليزي إلى صيغة موحّدة للمطابقة */
function norm(s = "") {
    return s.toLowerCase()
        .replace(/[\u064B-\u0652\u0670]/g, "")
        .replace(/[أإآٱ]/g, "ا").replace(/ى/g, "ي").replace(/ة/g, "ه")
        .replace(/\s+/g, " ").trim();
}

/* ============ 1) اللغة (عربي / إنجليزي) ============ */
function applyLang() {
    document.documentElement.lang = LANG;
    document.documentElement.dir  = LANG === "ar" ? "rtl" : "ltr";

    /* النصوص الثابتة التي تحمل data-ar / data-en */
    $$("[data-ar]").forEach(el => {
        const v = el.dataset[LANG];
        if (v !== undefined) el.textContent = v;
    });

    /* النص البديل للصور التوضيحية يتبع اللغة الحالية */
    $$("img[data-alt-ar]").forEach(img => {
        const v = LANG === "ar" ? img.dataset.altAr : img.dataset.altEn;
        if (v) img.alt = v;
    });

    $("#langLabel").textContent = LANG === "ar" ? "EN" : "ع";
    $("#chatText").placeholder = LANG === "ar"
        ? "اكتب سؤالك عن الحوسبة الكمية…" : "Ask about quantum computing…";

    /* خيارات النشاط الأول */
    const a1 = ["دائماً 0", "دائماً 1", "0 أو 1 باحتمال 50% لكل منهما", "لا يمكن القياس"];
    const a1e = ["Always 0", "Always 1", "0 or 1 with 50% each", "Not measurable"];
    $$("#a1Options .opt").forEach((b, i) => b.textContent = LANG === "ar" ? a1[i] : a1e[i]);

    renderConcepts(); renderGates(); renderLab();
    renderProjects(); renderTeacher(); renderActivitiesStatic();
    if ($("#quizBody")) renderQuiz();
    $("#chatSuggestions") && renderSuggestions();
    renderWelcome();
}
$("#langBtn").addEventListener("click", () => {
    LANG = LANG === "ar" ? "en" : "ar";
    store.set("qc-lang", LANG);
    applyLang();
});

/* ============ 2) الوضع الليلي / الفاتح ============ */
const themeBtn = $("#themeBtn");
function applyTheme() {
    const light = store.get("qc-theme", "light") === "light";
    document.body.classList.toggle("light", light);
    $("#themeIcon").setAttribute("href", light ? "#ic-sun" : "#ic-moon");
}
themeBtn.addEventListener("click", () => {
    store.set("qc-theme", document.body.classList.contains("light") ? "dark" : "light");
    applyTheme();
});
applyTheme();

/* ============ 3) خلفية النجوم ============ */
(function stars() {
    const cv = $("#starsCanvas");
    let ctx = null;
    try { ctx = cv.getContext("2d"); } catch (e) { ctx = null; }
    if (!ctx) return;
    let w, h, pts = [];
    function resize() {
        w = cv.width = innerWidth; h = cv.height = innerHeight;
        const n = Math.min(90, Math.floor(w * h / 16000));
        pts = Array.from({ length: n }, () => ({
            x: Math.random() * w, y: Math.random() * h,
            vx: (Math.random() - .5) * .28, vy: (Math.random() - .5) * .28,
            r: Math.random() * 1.7 + .5, c: Math.random() > .55 ? "34,211,238" : "139,92,246"
        }));
    }
    function draw() {
        ctx.clearRect(0, 0, w, h);
        for (const p of pts) {
            p.x += p.vx; p.y += p.vy;
            if (p.x < 0 || p.x > w) p.vx *= -1;
            if (p.y < 0 || p.y > h) p.vy *= -1;
            ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 7);
            ctx.fillStyle = `rgba(${p.c},.75)`; ctx.fill();
        }
        for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) {
            const a = pts[i], b = pts[j], d = Math.hypot(a.x - b.x, a.y - b.y);
            if (d < 130) {
                ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
                ctx.strokeStyle = `rgba(148,163,184,${.16 * (1 - d / 130)})`;
                ctx.lineWidth = .7; ctx.stroke();
            }
        }
        requestAnimationFrame(draw);
    }
    addEventListener("resize", resize); resize(); draw();
})();

/* ============ 4) القائمة الجانبية + التمرير النشط ============ */
const sidebar = $("#sidebar");
$("#menuBtn").addEventListener("click", () => document.body.classList.toggle("nav-open"));
$("#navOverlay").addEventListener("click", () => document.body.classList.remove("nav-open"));
$$(".nav-link").forEach(a => a.addEventListener("click", () => document.body.classList.remove("nav-open")));

const HAS_IO = "IntersectionObserver" in window;
if (HAS_IO) {
    const secObserver = new IntersectionObserver(es => {
        es.forEach(e => {
            if (!e.isIntersecting) return;
            const id = e.target.id;
            $$(".nav-link").forEach(l => l.classList.toggle("active", l.dataset.target === id));
            const act = $(`.nav-link[data-target="${id}"] span`);
            if (act) {
                const cur = $("#currentSection");
                cur.dataset.ar = act.dataset.ar; cur.dataset.en = act.dataset.en;
                cur.textContent = act.dataset[LANG];
            }
        });
    }, { rootMargin: "-45% 0px -50% 0px" });
    $$(".main .section").forEach(s => secObserver.observe(s));
}

/* ظهور العناصر عند التمرير */
if (HAS_IO) {
    const revObserver = new IntersectionObserver(es => {
        es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); revObserver.unobserve(e.target); } });
    }, { threshold: .12 });
    $$("[data-reveal]").forEach(el => revObserver.observe(el));
} else {
    $$("[data-reveal]").forEach(el => el.classList.add("in"));
}

/* زر العودة للأعلى */
const backTop = $("#backTop");
addEventListener("scroll", () => backTop.classList.toggle("show", scrollY > 420), { passive: true });
backTop.addEventListener("click", () => scrollTo({ top: 0, behavior: "smooth" }));

/* ============ 5) محاكي الكمّيات المصغّر (statevector) ============ */
const S2 = Math.SQRT1_2;
const MATS = {
    I: [[[1, 0], [0, 0]], [[0, 0], [1, 0]]],
    X: [[[0, 0], [1, 0]], [[1, 0], [0, 0]]],
    Y: [[[0, 0], [0, -1]], [[0, 1], [0, 0]]],
    Z: [[[1, 0], [0, 0]], [[0, 0], [-1, 0]]],
    H: [[[S2, 0], [S2, 0]], [[S2, 0], [-S2, 0]]],
    S: [[[1, 0], [0, 0]], [[0, 0], [0, 1]]],
    T: [[[1, 0], [0, 0]], [[0, 0], [Math.SQRT1_2, Math.SQRT1_2]]]
};
const cmul = (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];

function initState(n) { const s = Array(1 << n).fill(0).map(() => [0, 0]); s[0] = [1, 0]; return s; }
const bitOf = (q, n) => 1 << (n - 1 - q);

/* تطبيق بوابة أحادية على كيوبت واحد */
function apply1(state, n, g, q) {
    const M = MATS[g]; if (!M) return state;
    const out = Array(1 << n).fill(0).map(() => [0, 0]);
    const b = bitOf(q, n);
    for (let i = 0; i < state.length; i++) {
        if (i & b) continue;
        const j = i | b;
        for (let r = 0; r < 2; r++) {
            for (let c = 0; c < 2; c++) {
                const src = (c === 0) ? i : j, dst = (r === 0) ? i : j;
                const a = cmul(M[r][c], state[src]);
                out[dst][0] += a[0]; out[dst][1] += a[1];
            }
        }
    }
    return out;
}
/* بوابة CNOT */
function applyCNOT(state, n, c, t) {
    const out = state.map(v => [v[0], v[1]]), bc = bitOf(c, n), bt = bitOf(t, n);
    for (let i = 0; i < state.length; i++) if (i & bc) {
        const j = i ^ bt;
        if (j > i) { const tmp = out[i]; out[i] = out[j]; out[j] = tmp; }
    }
    return out;
}
/* بوابة SWAP */
function applySWAP(state, n, a, b) {
    const out = state.map(v => [v[0], v[1]]), ba = bitOf(a, n), bb = bitOf(b, n);
    for (let i = 0; i < state.length; i++) {
        const ai = !!(i & ba), bi = !!(i & bb);
        if (ai !== bi) {
            let j = i;
            j = ai ? (j & ~ba) | bb : (j | ba) & ~bb;
            if (j > i) { const tmp = out[i]; out[i] = out[j]; out[j] = tmp; }
        }
    }
    return out;
}
/* قياس: يعيد {value, state} بعد الانهيار */
function measure(state, n) {
    const p = state.map(a => a[0] * a[0] + a[1] * a[1]);
    let r = Math.random(), acc = 0, idx = state.length - 1;
    for (let i = 0; i < p.length; i++) { acc += p[i]; if (r <= acc) { idx = i; break; } }
    const out = Array(state.length).fill(0).map(() => [0, 0]);
    out[idx] = [1, 0];
    return { value: idx.toString(2).padStart(n, "0"), state: out, probs: p };
}
/* عرض الحالة بالصيغة Dirac */
function fmtState(state, n) {
    const parts = [];
    state.forEach((a, i) => {
        const m = Math.hypot(a[0], a[1]);
        if (m < 1e-6) return;
        const re = Math.round(a[0] * 100) / 100, im = Math.round(a[1] * 100) / 100;
        let c;
        if (Math.abs(im) < 1e-9) c = (re < 0 ? "−" : "") + (Math.abs(Math.abs(re) - 1) < 1e-9 ? "" : Math.abs(re));
        else if (Math.abs(re) < 1e-9) c = (im < 0 ? "−" : "") + (Math.abs(Math.abs(im) - 1) < 1e-9 ? "" : Math.abs(im)) + "i";
        else c = `(${re}${im < 0 ? "−" : "+"}${Math.abs(im)}i)`;
        parts.push(`${c}|${i.toString(2).padStart(n, "0")}⟩`);
    });
    return parts.join(" + ") || "0";
}
/* مساواة حالتين حتى مرحلة عالمية مشتركة (Up to global phase) */
function sameState(a, b) {
    let ref = null;
    for (let i = 0; i < a.length; i++) {
        const ma = Math.hypot(a[i][0], a[i][1]), mb = Math.hypot(b[i][0], b[i][1]);
        if (ma < 1e-6 && mb < 1e-6) continue;
        if (Math.abs(ma - mb) > 1e-4) return false;
        if (!ref) {
            const d = ma * ma;                                   // الطور = b/a
            const r = cmul(b[i], [a[i][0], -a[i][1]]);
            ref = [r[0] / d, r[1] / d];
        }
    }
    if (!ref) return true;
    for (let i = 0; i < a.length; i++) {
        const v = cmul(ref, a[i]);
        if (Math.hypot(v[0] - b[i][0], v[1] - b[i][1]) > 1e-4) return false;
    }
    return true;
}
/* توليد رابط دائرة Quirk */
const quirkUrl = (cols, bust = false) =>
    "https://algassert.com/quirk" + (bust ? "?v=" + Date.now() : "") +
    "#circuit=" + encodeURIComponent(JSON.stringify({ cols }));

/* ============ 6) بطاقات المفاهيم + النافذة ============ */
const ILLUS = {
    qubit: `<svg viewBox="0 0 420 150"><circle cx="210" cy="75" r="62" stroke="#7c3aed" stroke-opacity=".6"/><ellipse cx="210" cy="75" rx="62" ry="22" stroke="#22d3ee" stroke-opacity=".55"/><line x1="210" y1="13" x2="210" y2="137" stroke="#64748b" stroke-opacity=".45"/><line x1="210" y1="75" x2="258" y2="41" stroke="#d97706" stroke-width="3"/><circle cx="258" cy="41" r="7" fill="#d97706"/><text x="210" y="147" fill="#0891b2" font-size="14" text-anchor="middle" stroke="none">|0⟩ … |1⟩</text></svg>`,
    compare: `<svg viewBox="0 0 420 150"><rect x="30" y="35" width="140" height="80" rx="10" stroke="#7c3aed"/><text x="100" y="70" fill="#64748b" font-size="13" text-anchor="middle" stroke="none">Bit</text><text x="100" y="95" fill="#7c3aed" font-size="17" text-anchor="middle" stroke="none">0 أو 1</text><rect x="250" y="35" width="140" height="80" rx="10" stroke="#22d3ee"/><text x="320" y="70" fill="#64748b" font-size="13" text-anchor="middle" stroke="none">Qubit</text><text x="320" y="95" fill="#d97706" font-size="17" text-anchor="middle" stroke="none">α|0⟩+β|1⟩</text><path d="M175 75h65" stroke="#d97706" stroke-dasharray="5 5"/><path d="M232 68l10 7-10 7" fill="#d97706"/></svg>`,
    superposition: `<svg viewBox="0 0 420 150"><text x="40" y="82" fill="#0891b2" font-size="18" stroke="none">|0⟩</text><path d="M75 75h60" stroke="#22d3ee"/><rect x="140" y="52" width="46" height="46" rx="9" fill="#7c3aed" stroke="none"/><text x="163" y="82" fill="#fff" font-size="18" text-anchor="middle" stroke="none">H</text><path d="M190 75h45" stroke="#22d3ee"/><path d="M235 75l60-32M235 75l60 32" stroke="#d97706"/><text x="315" y="52" fill="#d97706" font-size="16" stroke="none">|+⟩ 50%</text><text x="315" y="106" fill="#d97706" font-size="16" stroke="none">|−⟩ 50%</text></svg>`,
    entangle: `<svg viewBox="0 0 420 150"><circle cx="110" cy="75" r="34" stroke="#22d3ee"/><circle cx="310" cy="75" r="34" stroke="#a78bfa"/><path d="M144 75c40-38 92-38 132 0" stroke="#d97706" stroke-dasharray="6 6"/><path d="M144 75c40 38 92 38 132 0" stroke="#d97706" stroke-dasharray="6 6"/><text x="110" y="82" fill="#0891b2" font-size="15" text-anchor="middle" stroke="none">q0</text><text x="310" y="82" fill="#7c3aed" font-size="15" text-anchor="middle" stroke="none">q1</text><text x="210" y="30" fill="#d97706" font-size="13" text-anchor="middle" stroke="none">Entangled</text></svg>`,
    measure: `<svg viewBox="0 0 420 150"><path d="M25 90q20-45 40 0t40 0t40 0" stroke="#22d3ee"/><path d="M155 75h60" stroke="#d97706"/><rect x="225" y="45" width="46" height="46" rx="9" fill="#312e81" stroke="#7c3aed"/><text x="248" y="75" fill="#67e8f9" font-size="16" text-anchor="middle" stroke="none">M</text><path d="M278 68h45M278 68l10-7M323 68l-10 7" stroke="#d97706"/><rect x="335" y="52" width="26" height="46" rx="4" fill="#7c3aed" stroke="none"/><rect x="370" y="52" width="26" height="46" rx="4" fill="#0891b2" stroke="none"/><text x="348" y="45" fill="#64748b" font-size="12" text-anchor="middle" stroke="none">0</text><text x="383" y="45" fill="#64748b" font-size="12" text-anchor="middle" stroke="none">1</text></svg>`,
    gates: `<svg viewBox="0 0 420 150"><line x1="20" y1="75" x2="400" y2="75" stroke="#22d3ee" stroke-opacity=".7"/><rect x="70" y="52" width="46" height="46" rx="9" fill="#7c3aed" stroke="none"/><text x="93" y="83" fill="#fff" font-size="17" text-anchor="middle" stroke="none">H</text><rect x="185" y="52" width="46" height="46" rx="9" fill="#7c3aed" stroke="none"/><text x="208" y="83" fill="#fff" font-size="17" text-anchor="middle" stroke="none">X</text><rect x="300" y="52" width="46" height="46" rx="9" fill="#312e81" stroke="#7c3aed"/><text x="323" y="83" fill="#67e8f9" font-size="15" text-anchor="middle" stroke="none">M</text></svg>`
};

function renderConcepts() {
    const g = $("#conceptsGrid"); if (!g) return;
    g.innerHTML = CONCEPTS.map(c => `
        <article class="card" data-id="${c.id}" tabindex="0">
            <div class="card-ic"><svg><use href="#${c.icon}"/></svg></div>
            <h3>${t(c.title)}</h3>
            <span class="en">${c.en}</span>
            <p>${t(c.short)}</p>
            <span class="card-more">${LANG === "ar" ? "افتح الشرح التفاعلي" : "Open interactive explanation"}</span>
        </article>`).join("");
    $$("#conceptsGrid .card").forEach(card => {
        card.addEventListener("mousemove", e => {
            const r = card.getBoundingClientRect();
            card.style.setProperty("--mx", (e.clientX - r.left) + "px");
            card.style.setProperty("--my", (e.clientY - r.top) + "px");
        });
        card.addEventListener("click", () => openConcept(card.dataset.id));
        card.addEventListener("keydown", e => { if (e.key === "Enter") openConcept(card.dataset.id); });
    });
}

const modal = $("#conceptModal");
function openConcept(id) {
    const c = CONCEPTS.find(x => x.id === id); if (!c) return;
    $("#modalContent").innerHTML = `
        <div class="m-head">
            <div class="card-ic"><svg><use href="#${c.icon}"/></svg></div>
            <div><h3>${t(c.title)}</h3><span class="en">${c.en}</span></div>
        </div>
        <div class="m-body">
            ${c.long.map(p => `<p>${t(p)}</p>`).join("")}
            <div class="m-illu">${c.image ? `<img class="m-photo" src="${c.image}" alt="${t(c.imageAlt)}" loading="lazy" decoding="async">` : ""}${ILLUS[c.illu]}</div>
            <ul class="m-points">${c.points.map(p => `<li>${t(p)}</li>`).join("")}</ul>
            <div class="m-example">
                <h4><svg class="btn-ic"><use href="#ic-play"/></svg>${LANG === "ar" ? "مثال تفاعلي — جرّب بنفسك" : "Interactive example — try it yourself"}</h4>
                <div id="mExample"></div>
            </div>
            <div class="m-actions">
                <button class="btn btn-primary" data-run><svg class="btn-ic"><use href="#ic-flask"/></svg>${LANG === "ar" ? "جرّب في Quirk" : "Try in Quirk"}</button>
                <button class="btn btn-ghost" data-close>${LANG === "ar" ? "إغلاق" : "Close"}</button>
            </div>
        </div>`;
    mountExample(c.example, $("#mExample"));
    $("#modalContent [data-run]").addEventListener("click", () => { loadCircuit(c.cols); closeModal(); go("#lab"); });
    $("#modalContent [data-close]").addEventListener("click", closeModal);
    modal.classList.add("open"); modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
}
function closeModal() {
    modal.classList.remove("open"); modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
}
$$("[data-close]", modal).forEach(b => b.addEventListener("click", closeModal));
addEventListener("keydown", e => { if (e.key === "Escape") closeModal(); });

/* ---------- الأمثلة التفاعلية داخل النافذة ---------- */
function barsHTML(id) {
    return `<div class="prob-bars">
        <div class="pbar"><label>P(|0⟩)</label><div class="track"><i id="${id}0" style="width:100%"></i></div><b id="${id}v0">100%</b></div>
        <div class="pbar"><label>P(|1⟩)</label><div class="track"><i id="${id}1" style="width:0%"></i></div><b id="${id}v1">0%</b></div>
    </div>`;
}
function setBars(id, s) {
    const p0 = (s[0][0] ** 2 + s[0][1] ** 2) * 100, p1 = (s[1][0] ** 2 + s[1][1] ** 2) * 100;
    $(`#${id}0`).style.width = p0 + "%"; $(`#${id}1`).style.width = p1 + "%";
    $(`#${id}v0`).textContent = p0.toFixed(0) + "%"; $(`#${id}v1`).textContent = p1.toFixed(0) + "%";
}
function mountExample(mode, box) {
    if (!box) return;
    const AR = LANG === "ar";
    if (mode === "qubit") {
        box.innerHTML = `
            <p>${AR ? "حرّك المؤشر لتغيير زاوية الحالة على كرة بلوك وشاهد الاحتمالات:" : "Move the slider to change the state angle on the Bloch sphere:"}</p>
            <input type="range" id="exTheta" min="0" max="180" value="45" style="width:100%;accent-color:#0891b2">
            <div class="state-view" id="exState" style="margin:12px 0"></div>${barsHTML("exB")}`;
        const upd = () => {
            const th = +$("#exTheta").value * Math.PI / 180;
            const s = [[Math.cos(th / 2), 0], [Math.sin(th / 2), 0]];
            $("#exState").textContent = `${Math.cos(th / 2).toFixed(2)}|0⟩ + ${Math.sin(th / 2).toFixed(2)}|1⟩`;
            setBars("exB", s);
        };
        $("#exTheta").addEventListener("input", upd); upd();
    }
    else if (mode === "compare") {
        box.innerHTML = `
            <div class="opt-row" style="margin-bottom:12px">
                <button class="opt" id="exBit">${AR ? "بدّل البت (حالي: 0)" : "Toggle bit (now: 0)"}</button>
                <button class="opt" id="exQ">${AR ? "قِس الكيوبت 10 مرات" : "Measure qubit 10 times"}</button>
            </div>
            <div class="state-view" id="exState">${AR ? "البت: 0 | الكيوبت: |0⟩" : "Bit: 0 | Qubit: |0⟩"}</div>
            <div class="result-log" id="exLog" style="margin-top:10px"></div>`;
        let bit = 0, s = [[1, 0], [0, 0]];
        $("#exBit").onclick = () => { bit ^= 1; $("#exBit").textContent = AR ? `بدّل البت (حالي: ${bit})` : `Toggle bit (now: ${bit})`; $("#exState").textContent = AR ? `البت: ${bit} (حتمي) | الكيوبت: |0⟩` : `Bit: ${bit} (deterministic) | Qubit: |0⟩`; };
        $("#exQ").onclick = () => {
            s = apply1(s, 1, "H", 0); $("#exLog").innerHTML = "";
            let z = 0;
            for (let i = 0; i < 10; i++) { const m = measure(s, 1); if (m.value === "0") z++; $("#exLog").insertAdjacentHTML("beforeend", `<span class="res-chip">${m.value}</span>`); }
            $("#exState").textContent = AR ? `البت: ${bit} | الكيوبت أعطى ${z}×0 و ${10 - z}×1` : `Bit: ${bit} | Qubit gave ${z}×0 and ${10 - z}×1`;
            s = [[1, 0], [0, 0]];
        };
    }
    else if (mode === "superposition") {
        box.innerHTML = `
            <div class="state-view" id="exState" style="margin-bottom:12px">|0⟩</div>${barsHTML("exB")}
            <div class="act-controls" style="margin-top:14px">
                <button class="btn btn-primary" id="exH">H</button>
                <button class="btn btn-ghost" id="exM">${AR ? "قياس" : "Measure"}</button>
                <button class="btn btn-ghost" id="exR">${AR ? "إعادة" : "Reset"}</button>
            </div><div class="result-log" id="exLog" style="margin-top:10px"></div>`;
        let s = [[1, 0], [0, 0]];
        const upd = () => { $("#exState").textContent = fmtState(s, 1); setBars("exB", s); };
        $("#exH").onclick = () => { s = apply1(s, 1, "H", 0); upd(); };
        $("#exM").onclick = () => { const m = measure(s, 1); s = m.state; upd(); $("#exLog").insertAdjacentHTML("beforeend", `<span class="res-chip">${m.value}</span>`); };
        $("#exR").onclick = () => { s = [[1, 0], [0, 0]]; $("#exLog").innerHTML = ""; upd(); };
        upd();
    }
    else if (mode === "entangle") {
        box.innerHTML = `
            <div class="state-view" id="exState" style="margin-bottom:12px">|00⟩</div>
            <div class="act-controls">
                <button class="btn btn-primary" id="exB1">${AR ? "أنشئ بيل" : "Build Bell"}</button>
                <button class="btn btn-ghost" id="exM">${AR ? "قِس السلكين" : "Measure both"}</button>
                <button class="btn btn-ghost" id="exR">${AR ? "إعادة" : "Reset"}</button>
            </div>
            <div class="result-log" id="exLog" style="margin-top:12px"></div>
            <p id="exNote" style="margin-top:10px;color:var(--text-3);font-size:13.5px"></p>`;
        let s = initState(2), ok = 0, all = 0;
        const upd = () => $("#exState").textContent = fmtState(s, 2);
        $("#exB1").onclick = () => { s = apply1(s, 2, "H", 0); s = applyCNOT(s, 2, 0, 1); upd(); $("#exLog").innerHTML = ""; };
        $("#exM").onclick = () => {
            const m = measure(s, 2); all++; if (m.value[0] === m.value[1]) ok++;
            $("#exLog").insertAdjacentHTML("beforeend", `<span class="res-chip">${m.value}</span>`);
            $("#exNote").textContent = AR
                ? `تطابق ${ok}/${all} — لاحظ أن القيمتين متطابقتان دائماً.`
                : `Agreement ${ok}/${all} — the two values always match.`;
        };
        $("#exR").onclick = () => { s = initState(2); ok = all = 0; $("#exLog").innerHTML = ""; $("#exNote").textContent = ""; upd(); };
        upd();
    }
    else if (mode === "measure") {
        box.innerHTML = `
            <div class="act-controls" style="margin-bottom:14px">
                <button class="btn btn-primary" id="exH">H</button>
                <button class="btn btn-ghost" id="ex1">${AR ? "قياس واحد" : "One shot"}</button>
                <button class="btn btn-ghost" id="ex100">${AR ? "100 قياس" : "100 shots"}</button>
                <button class="btn btn-ghost" id="exR">${AR ? "إعادة" : "Reset"}</button>
            </div>
            <div class="state-view" id="exState">|0⟩</div>${barsHTML("exB")}
            <p id="exNote" style="margin-top:10px;font-size:14px;color:var(--text-2)"></p>`;
        let s = [[1, 0], [0, 0]], c0 = 0, c1 = 0, last = "";
        const upd = () => {
            $("#exState").textContent = fmtState(s, 1) + (last ? `   ⟵ ${last}` : "");
            setBars("exB", s);
            $("#exNote").textContent = AR
                ? `النتائج: 0 ← ${c0} | 1 ← ${c1}${c0 + c1 ? `  (نسبة الـ 0 = ${(c0 / (c0 + c1) * 100).toFixed(0)}%)` : ""}`
                : `Results: 0 → ${c0} | 1 → ${c1}${c0 + c1 ? `  (ratio of 0 = ${(c0 / (c0 + c1) * 100).toFixed(0)}%)` : ""}`;
        };
        $("#exH").onclick = () => { s = apply1(s, 1, "H", 0); last = ""; upd(); };
        $("#ex1").onclick = () => { last = measure(s, 1).value; last === "0" ? c0++ : c1++; upd(); };
        $("#ex100").onclick = () => { for (let i = 0; i < 100; i++) measure(s, 1).value === "0" ? c0++ : c1++; upd(); };
        $("#exR").onclick = () => { c0 = c1 = 0; last = ""; s = [[1, 0], [0, 0]]; upd(); };
        upd();
    }
    else if (mode === "gates") {
        box.innerHTML = `
            <div class="opt-row" id="exGates" style="margin-bottom:14px">
                ${["X", "Y", "Z", "H", "S", "T"].map(g => `<button class="opt" data-g="${g}">${g}</button>`).join("")}
            </div>
            <div class="state-view" id="exState" style="margin-bottom:12px">|0⟩</div>${barsHTML("exB")}
            <div class="act-controls" style="margin-top:12px"><button class="btn btn-ghost" id="exR">${AR ? "إعادة إلى |0⟩" : "Reset to |0⟩"}</button></div>`;
        let s = [[1, 0], [0, 0]];
        const upd = () => { $("#exState").textContent = fmtState(s, 1); setBars("exB", s); };
        $$("#exGates .opt").forEach(b => b.onclick = () => { s = apply1(s, 1, b.dataset.g, 0); upd(); });
        $("#exR").onclick = () => { s = [[1, 0], [0, 0]]; upd(); };
        upd();
    }
}

/* ============ 7) البوابات ============ */
function renderGates() {
    const g = $("#gatesGrid"); if (!g) return;
    g.innerHTML = GATES.map(x => `
        <article class="card" data-gate="${x.id}">
            <div class="card-ic">${x.sym}</div>
            <h3>${t(x.name)}</h3>
            <span class="en">${x.id} GATE</span>
            <div class="gate-matrix">${x.matrix.flat().map(v => `<span>${v}</span>`).join("")}</div>
            <p>${t(x.func)}</p>
            <p style="margin-top:9px;color:var(--text-3)"><b>${LANG === "ar" ? "مثال عملي:" : "Example:"}</b> ${t(x.example)}</p>
            <button class="gate-try" data-id="${x.id}"><svg class="btn-ic"><use href="#ic-flask"/></svg>${LANG === "ar" ? "جرّب في Quirk" : "Try in Quirk"}</button>
        </article>`).join("");
    $$("#gatesGrid .gate-try").forEach(b => b.addEventListener("click", e => {
        e.stopPropagation();
        const gt = GATES.find(v => v.id === b.dataset.id);
        loadCircuit(gt.cols); go("#lab");
    }));
}

/* ============ 8) مختبر Quirk ============ */
const frame = $("#quirkFrame");
let currentExp = EXPERIMENTS[0].id;   /* التجربة المعروضة حالياً (لتُعاد عند تبديل اللغة) */
let currentCols = EXPERIMENTS[0].cols;
function loadCircuit(cols) {
    if (!cols) return;
    currentCols = cols;
    /* ?v= يفرض إعادة تحميل كاملة: تغيير الـhash وحده لا يعيد قراءة الدائرة داخل Quirk */
    frame.src = quirkUrl(cols, true);
}
function go(sel) {
    const el = $(sel);
    if (el && typeof el.scrollIntoView === "function") el.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderLab() {
    /* الدوائر الجاهزة */
    const pb = $("#presetBtns");
    if (pb) pb.innerHTML = PRESETS.map(p =>
        `<button class="preset-btn" data-id="${p.id}"><span>${t(p.label)}</span><span class="tag">${p.tag}</span></button>`).join("");
    $$("#presetBtns .preset-btn").forEach(b => b.onclick = () => {
        loadCircuit(PRESETS.find(p => p.id === b.dataset.id).cols);
        showExperiment(null);
    });

    /* قائمة التجارب */
    const el = $("#expList");
    if (el) el.innerHTML = EXPERIMENTS.map((e, i) =>
        `<button class="exp-item" data-id="${e.id}"><span class="num">0${i + 1}</span><span>${t(e.title)}</span></button>`).join("");
    $$("#expList .exp-item").forEach(b => b.onclick = () => showExperiment(b.dataset.id));

    showExperiment(currentExp);   /* إعادة عرض التجربة باللغة الجديدة */
}
function showExperiment(id) {
    const box = $("#expDetail"); if (!box) return;
    currentExp = id;
    if (!id) {
        box.innerHTML = `<p style="color:var(--text-2)">${LANG === "ar"
            ? "اختر تجربة من القائمة لعرض شرحها النظري وخطوات التنفيذ، أو استخدم زر «شغّل» لتحميل الدائرة في المحاكي."
            : "Pick an experiment from the list for theory and steps, or press “Run” to load its circuit into the simulator."}</p>`;
        $$("#expList .exp-item").forEach(x => x.classList.remove("active"));
        return;
    }
    const e = EXPERIMENTS.find(x => x.id === id);
    $$("#expList .exp-item").forEach(x => x.classList.toggle("active", x.dataset.id === id));
    box.innerHTML = `
        <h3>${t(e.title)}</h3><span class="exp-en">${e.en}</span>
        <div class="exp-block"><h4><svg><use href="#ic-bulb"/></svg>${LANG === "ar" ? "الشرح النظري" : "Theory"}</h4><p style="color:var(--text-2)">${t(e.theory)}</p></div>
        <div class="exp-block"><h4><svg><use href="#ic-target"/></svg>${LANG === "ar" ? "الهدف من التجربة" : "Goal"}</h4><p style="color:var(--text-2)">${t(e.goal)}</p></div>
        <div class="exp-block"><h4><svg><use href="#ic-check"/></svg>${LANG === "ar" ? "خطوات التنفيذ" : "Steps"}</h4><ol>${e.steps.map(s => `<li>${t(s)}</li>`).join("")}</ol></div>
        <div class="exp-block"><h4><svg><use href="#ic-atom"/></svg>${LANG === "ar" ? "ماذا يلاحظ الطالب؟" : "What should the student notice?"}</h4><p style="color:var(--text-2)">${t(e.observe)}</p></div>
        <div class="exp-actions">
            <button class="btn btn-primary" id="expRun"><svg class="btn-ic"><use href="#ic-play"/></svg>${LANG === "ar" ? "شغّل الدائرة في Quirk" : "Run circuit in Quirk"}</button>
            <a class="btn btn-ghost" href="${quirkUrl(e.cols)}" target="_blank" rel="noopener"><svg class="btn-ic"><use href="#ic-open"/></svg>${LANG === "ar" ? "نافذة جديدة" : "New window"}</a>
        </div>`;
    $("#expRun").onclick = () => loadCircuit(e.cols);
}
$("#reloadQuirk").addEventListener("click", () => loadCircuit(currentCols));

/* ============ 9) الأنشطة التعليمية ============ */
$$("#actTabs .tab").forEach(b => b.onclick = () => {
    $$("#actTabs .tab").forEach(x => x.classList.toggle("active", x === b));
    $$(".activity").forEach(a => a.classList.toggle("active", a.id === "act-" + b.dataset.act));
});

/* --- نصوص ثابتة تتغير مع اللغة --- */
function renderActivitiesStatic() {
    const AR = LANG === "ar";
    const st = [
        ["#act-1 .act-head p", "قبل أن تشغّل المحاكاة، اختر إجابتك. ثم شغّل الدائرة وقيس 10 مرات لترى النتيجة.", "Choose your answer before running the simulation. Then run the circuit and measure 10 times."],
        ["#act-1 .q-block h4", "سؤال: ماذا سيظهر بعد تطبيق H ثم القياس؟", "Question: what appears after applying H then measuring?"],
        ["#a1Apply span", "طبّق بوابة H", "Apply H gate"],
        ["#a1Measure span", "قياس 10 مرات", "Measure 10 times"],
        ["#a1Reset span", "إعادة", "Reset"],
        ["#a2Run span", "ابنِ الدائرة وتحقّق", "Build and check"],
        ["#a2InQuirk span", "افتح في Quirk", "Open in Quirk"],
        ["#a2Reset span", "إعادة", "Reset"],
        ["#act-2 .act-head p", "اختر خطوتين لبناء دائرة بيل الكمية |00⟩ ← (|00⟩+|11⟩)/√2 ثم تحقّق من النتيجة.", "Pick two steps to build the quantum Bell circuit |00⟩ → (|00⟩+|11⟩)/√2 then check the result."],
        ["#act-3 .act-head p", "لكل مهمة اختر البوابة التي تحوّل الحالة الأولى إلى الحالة المستهدفة.", "For each task, pick the gate that transforms the initial state into the target state."],
        ["#act-4 .act-head p", "اسحب البوابات (أو انقر عليها ثم انقر الخانة) إلى الأسلاك لبلوغ الحالة المستهدفة.", "Drag gates (or click a gate then a slot) onto the wire to reach the target state."],
        ["#a3Next span", "المهمة التالية", "Next task"],
        ["#a3Restart span", "إعادة النشاط", "Restart activity"],
        ["#a4Run span", "شغّل الدائرة", "Run circuit"],
        ["#a4Clear span", "مسح", "Clear"],
        ["#a4New span", "الجولة التالية", "Next round"]
    ];
    st.forEach(([sel, ar, en]) => { const el = $(sel); if (el) el.textContent = AR ? ar : en; });
    if ($("#a1Feedback").dataset.txt) $("#a1Feedback").innerHTML = $("#a1Feedback").dataset.txt;
}

/* --- النشاط 1: توقع نتيجة H --- */
const A1 = { state: [[1, 0], [0, 0]], applied: false };
function a1Bars() {
    const s = A1.state;
    const p0 = (s[0][0] ** 2 + s[0][1] ** 2) * 100, p1 = (s[1][0] ** 2 + s[1][1] ** 2) * 100;
    $("#a1P0").style.width = p0 + "%"; $("#a1P1").style.width = p1 + "%";
    $("#a1V0").textContent = p0.toFixed(0) + "%"; $("#a1V1").textContent = p1.toFixed(0) + "%";
}
$("#a1Apply").onclick = () => {
    A1.state = apply1(A1.state, 1, "H", 0); A1.applied = true;
    $("#a1GateBox").textContent = "H"; a1Bars();
    $("#a1Measure").disabled = false;
    $("#a1Apply").disabled = true;
    fb("#a1Feedback", "ok", LANG === "ar"
        ? "ممتاز! طُبّقت بوابة H: الآن الكيوبت في تراكب |+⟩ والاحتمالات 50% / 50%."
        : "Great! H applied: the qubit is now in |+⟩ with 50% / 50% probabilities.");
};
$("#a1Measure").onclick = () => {
    let z = 0; $("#a1Log").innerHTML = "";
    for (let i = 0; i < 10; i++) { const m = measure(A1.state, 1); if (m.value === "0") z++; $("#a1Log").insertAdjacentHTML("beforeend", `<span class="res-chip">${m.value}</span>`); }
    fb("#a1Feedback", Math.abs(z - 5) <= 3 ? "ok" : "no", LANG === "ar"
        ? `النتيجة: ${z}×0 و ${10 - z}×1. ${Math.abs(z - 5) <= 3 ? "هذا يطابق نظرية 50/50 تقريباً." : "العينة صغيرة؛ جرّب مجدداً وستقترب من 50%."}`
        : `Result: ${z}×0 and ${10 - z}×1. ${Math.abs(z - 5) <= 3 ? "Matches the 50/50 theory." : "Small sample; try again and it approaches 50%."}`);
};
$("#a1Reset").onclick = () => {
    A1.state = [[1, 0], [0, 0]]; A1.applied = false;
    $("#a1GateBox").textContent = "|0⟩"; $("#a1Log").innerHTML = "";
    $("#a1Measure").disabled = true; $("#a1Apply").disabled = false;
    $("#a1Feedback").hidden = true; a1Bars();
};
$$("#a1Options .opt").forEach(b => b.onclick = () => {
    $$("#a1Options .opt").forEach(x => { x.classList.remove("correct", "wrong"); x.disabled = false; });
    const ok = b.dataset.correct === "2";
    b.classList.add(ok ? "correct" : "wrong");
    if (!ok) $$("#a1Options .opt")[2].classList.add("correct");
    fb("#a1Feedback", ok ? "ok" : "no", LANG === "ar"
        ? (ok ? "إجابة صحيحة! H تُنتج تراكباً 50/50 والنتيجة تظهر عند القياس فقط."
              : "الإجابة الصحيحة: 0 أو 1 باحتمال 50% لكل منهما — الكيوبت في تراكب حتى لحظة القياس.")
        : (ok ? "Correct! H creates a 50/50 superposition; the outcome appears only at measurement."
              : "Correct answer: 0 or 1 with 50% each — the qubit is in superposition until measured."));
});
function fb(sel, cls, html) { const e = $(sel); e.hidden = false; e.className = "feedback " + cls; e.innerHTML = html; e.dataset.txt = html; }

/* --- النشاط 2: بناء حالة بيل --- */
const A2 = { s1: null, s2: null };
$$("#act-2 .opt-row").forEach(row => {
    const group = row.dataset.group;
    $$(".opt", row).forEach(b => b.onclick = () => {
        $$(".opt", row).forEach(x => x.classList.remove("selected"));
        b.classList.add("selected");
        A2[group] = b.dataset.val;
    });
});
function a2Build() {
    let s = initState(2);
    if (A2.s1 && A2.s1 !== "I") s = apply1(s, 2, A2.s1, 0);
    if (A2.s2 === "CX") s = applyCNOT(s, 2, 0, 1);
    else if (A2.s2 === "H") s = apply1(s, 2, "H", 0);
    else if (A2.s2 === "SWAP") s = applySWAP(s, 2, 0, 1);
    return s;
}
function a2Cols() {
    const c = [];
    if (A2.s1 && A2.s1 !== "I") c.push([A2.s1, 1]);
    if (A2.s2 === "CX") c.push(["•", "X"]);
    else if (A2.s2 === "H") c.push(["H", 1]);
    else if (A2.s2 === "SWAP") c.push(["Swap", "Swap"]);
    c.push(["Measure", "Measure"]);
    return c;
}
$("#a2Run").onclick = () => {
    if (!A2.s1 || !A2.s2) {
        fb("#a2Feedback", "no", LANG === "ar" ? "اختر بوابة لكل خطوة أولاً ثم اضغط «ابنِ الدائرة»." : "Pick a gate for each step first, then press “Build”.");
        return;
    }
    const s = a2Build();
    const bell = [[S2, 0], [0, 0], [0, 0], [S2, 0]];
    const ok = sameState(s, bell);
    $("#a2State").textContent = fmtState(s, 2);
    fb("#a2Feedback", ok ? "ok" : "no", ok
        ? (LANG === "ar" ? "رائع! حصلت على حالة بيل (|00⟩+|11⟩)/√2 — أي تشابك حقيقي بين الكيوبتين."
                         : "Excellent! You built the Bell state (|00⟩+|11⟩)/√2 — real entanglement.")
        : (LANG === "ar" ? "ليست حالة بيل بعد. الترتيب الصحيح: H على q0 ثم CNOT. جرّب تعديل الخطوتين."
                         : "Not a Bell state yet. Correct order: H on q0 then CNOT. Adjust the two steps."));
};
$("#a2Reset").onclick = () => {
    A2.s1 = A2.s2 = null;
    $$("#act-2 .opt").forEach(x => x.classList.remove("selected"));
    $("#a2State").textContent = "|00⟩"; $("#a2Feedback").hidden = true;
};
$("#a2InQuirk").onclick = () => { loadCircuit(a2Cols()); go("#lab"); };

/* --- النشاط 3: اختر البوابة المناسبة --- */
const A3 = { i: 0, done: false };
const KEYS = { ar: ["أ", "ب", "ج", "د"], en: ["A", "B", "C", "D"] };
function stateOf(lbl) {
    if (lbl === "|0⟩") return [[1, 0], [0, 0]];
    if (lbl === "|1⟩") return [[0, 0], [1, 0]];
    if (lbl === "|+⟩") return [[S2, 0], [S2, 0]];
    if (lbl === "|−⟩") return [[S2, 0], [-S2, 0]];
    return [[1, 0], [0, 0]];
}
function a3Render() {
    const tk = A3_TASKS[A3.i];
    $("#a3Count").textContent = (LANG === "ar" ? `المهمة ${A3.i + 1} / ` : `Task ${A3.i + 1} / `) + A3_TASKS.length;
    $("#a3Bar").style.width = (A3.i / A3_TASKS.length * 100) + "%";
    $("#a3Task").innerHTML = `
        <div class="task-card">
            <div class="task-states">
                <div class="task-state"><small>${LANG === "ar" ? "الحالة الابتدائية" : "Initial state"}</small><b>${t(tk.from)}</b></div>
                <div class="task-arrow">←</div>
                <div class="task-state"><small>${LANG === "ar" ? "الحالة المستهدفة" : "Target state"}</small><b>${t(tk.to)}</b></div>
            </div>
            <div class="opt-row" id="a3Opts" style="justify-content:center">
                ${tk.options.map((g, i) => `<button class="opt" data-g="${g}"><b style="font-family:var(--font-tech)">${KEYS[LANG][i]}</b>&nbsp; ${g}</button>`).join("")}
            </div>
        </div>`;
    $$("#a3Opts .opt").forEach(b => b.onclick = () => a3Check(b, tk));
    $("#a3Feedback").hidden = true; $("#a3Next").hidden = true;
}
function a3Check(btn, tk) {
    let s = stateOf(t(tk.from));
    s = apply1(s, 1, btn.dataset.g, 0);
    const ok = sameState(s, stateOf(t(tk.to)));
    $$("#a3Opts .opt").forEach(x => x.disabled = true);
    btn.classList.add(ok ? "correct" : "wrong");
    if (!ok) $$("#a3Opts .opt").find(x => x.dataset.g === tk.answer)?.classList.add("correct");
    const prefix = ok
        ? (LANG === "ar" ? "صحيح! " : "Correct! ")
        : ((LANG === "ar" ? "الإجابة الصحيحة: " : "Right answer: ") + tk.answer + ". ");
    fb("#a3Feedback", ok ? "ok" : "no", prefix + t(tk.why));
    if (A3.i === A3_TASKS.length - 1) { $("#a3Next").hidden = true; $("#a3Restart").hidden = false; a3Final(); }
    else $("#a3Next").hidden = false;
    $("#a3Bar").style.width = ((A3.i + 1) / A3_TASKS.length * 100) + "%";
}
function a3Final() {
    $("#a3Count").textContent = LANG === "ar" ? "اكتمل النشاط!" : "Activity complete!";
}
$("#a3Next").onclick = () => { A3.i++; a3Render(); };
$("#a3Restart").onclick = () => { A3.i = 0; a3Render(); };

/* --- النشاط 4: السحب والأفلت --- */
const A4 = { round: 0, slots: [null, null, null, null], picked: null };
const PALETTE = ["X", "H", "Z", "S", "T"];
function a4Render() {
    $("#a4Palette").innerHTML = PALETTE.map(g => `<div class="gate-chip" draggable="true" data-g="${g}">${g}</div>`).join("");
    $("#a4Slots").innerHTML = A4.slots.map((g, i) =>
        `<div class="slot${g ? " filled" : ""}" data-i="${i}">${g || (LANG === "ar" ? "خ" : "#")}</div>`).join("");
    $("#a4Target").textContent = t(A4_ROUNDS[A4.round].target);
    $("#a4Round").textContent = (LANG === "ar" ? `الجولة ${A4.round + 1} / ` : `Round ${A4.round + 1} / `) + A4_ROUNDS.length;
    a4Wire();
    /* الأحداث */
    $$("#a4Palette .gate-chip").forEach(ch => {
        ch.addEventListener("dragstart", e => e.dataTransfer.setData("text/plain", ch.dataset.g));
        ch.addEventListener("click", () => {
            $$("#a4Palette .gate-chip").forEach(x => x.classList.remove("picked"));
            if (A4.picked === ch.dataset.g) { A4.picked = null; }
            else { A4.picked = ch.dataset.g; ch.classList.add("picked"); }
        });
    });
    $$("#a4Slots .slot").forEach(sl => {
        sl.addEventListener("dragover", e => { e.preventDefault(); sl.classList.add("over"); });
        sl.addEventListener("dragleave", () => sl.classList.remove("over"));
        sl.addEventListener("drop", e => { e.preventDefault(); sl.classList.remove("over"); a4Put(+sl.dataset.i, e.dataTransfer.getData("text/plain")); });
        sl.addEventListener("click", () => {
            if (A4.picked) { a4Put(+sl.dataset.i, A4.picked); A4.picked = null; $$("#a4Palette .gate-chip").forEach(x => x.classList.remove("picked")); }
            else if (A4.slots[+sl.dataset.i]) { A4.slots[+sl.dataset.i] = null; a4Render(); }
        });
    });
}
function a4Put(i, g) { if (g) { A4.slots[i] = g; a4Render(); } }
function a4Wire() {
    $$("#a4Slots .slot").forEach((sl, i) => sl.classList.toggle("filled", !!A4.slots[i]));
}
$("#a4Run").onclick = () => {
    let s = [[1, 0], [0, 0]];
    A4.slots.forEach(g => { if (g) s = apply1(s, 1, g, 0); });
    $("#a4State").textContent = fmtState(s, 1);
    const ok = sameState(s, A4_ROUNDS[A4.round].state);
    fb("#a4Feedback", ok ? "ok" : "no", ok
        ? (LANG === "ar" ? "ممتاز! وصلت الحالة المستهدفة تماماً." : "Excellent! You reached the exact target state.")
        : (LANG === "ar" ? `ليست الحالة المستهدفة بعد — حصلت على ${fmtState(s, 1)}. جرّب ترتيباً آخر من البوابات.` : `Not the target yet — you got ${fmtState(s, 1)}. Try a different gate order.`));
    if (ok && A4.round < A4_ROUNDS.length - 1) $("#a4New").hidden = false;
    if (ok && A4.round === A4_ROUNDS.length - 1) {
        $("#a4New").hidden = false;
        $("#a4New").textContent = LANG === "ar" ? "أعد الجولات" : "Restart rounds";
    }
};
$("#a4Clear").onclick = () => { A4.slots = [null, null, null, null]; a4Render(); $("#a4Feedback").hidden = true; };
$("#a4New").onclick = () => {
    if (A4.round === A4_ROUNDS.length - 1) A4.round = 0; else A4.round++;
    A4.slots = [null, null, null, null];
    $("#a4State").textContent = "|0⟩"; $("#a4Feedback").hidden = true; $("#a4New").hidden = true;
    $("#a4New").textContent = LANG === "ar" ? "الجولة التالية" : "Next round";
    a4Render();
};

/* ============ 10) الاختبار التفاعلي ============ */
const QZ = { i: 0, score: 0, locked: false };
function renderQuiz() {
    const body = $("#quizBody");
    if (QZ.i >= QUIZ.length) return quizResult();
    const q = QUIZ[QZ.i];
    $("#quizCounter").textContent = (LANG === "ar" ? `السؤال ${QZ.i + 1} / ` : `Question ${QZ.i + 1} / `) + QUIZ.length;
    $("#quizScore").textContent = QZ.score;
    $("#quizBar").style.width = ((QZ.i) / QUIZ.length * 100 || 3) + "%";
    QZ.locked = false;
    body.innerHTML = `
        <div class="q-text"><span class="q-num">${LANG === "ar" ? "سؤال" : "QUESTION"} ${QZ.i + 1}</span>${t(q.q)}</div>
        <div class="q-opts">${q.o.map((o, i) =>
            `<button class="q-opt" data-i="${i}"><span class="k">${KEYS[LANG][i] || i + 1}</span><span>${t(o)}</span></button>`).join("")}</div>
        <div id="qExp"></div>
        <div class="q-actions"><button class="btn btn-primary" id="qNext" disabled>${QZ.i === QUIZ.length - 1 ? (LANG === "ar" ? "عرض النتيجة" : "Show result") : (LANG === "ar" ? "السؤال التالي" : "Next question")}</button></div>`;
    $$("#quizBody .q-opt").forEach(b => b.onclick = () => answer(+b.dataset.i, b));
}
function answer(i, btn) {
    if (QZ.locked) return;
    QZ.locked = true;
    const q = QUIZ[QZ.i], ok = i === q.a;
    if (ok) QZ.score += 5;
    $$("#quizBody .q-opt").forEach(b => {
        b.disabled = true;
        const idx = +b.dataset.i;
        if (idx === q.a) b.classList.add("correct");
        else if (idx === i) b.classList.add("wrong");
    });
    $("#qExp").innerHTML = `<div class="q-exp">${ok ? (LANG === "ar" ? "إجابة صحيحة! " : "Correct! ") : (LANG === "ar" ? "الإجابة الصحيحة موضّحة بالأخضر. " : "The correct answer is highlighted. ")}${t(q.e)}</div>`;
    $("#quizScore").textContent = QZ.score;
    $("#qNext").disabled = false;
    $("#qNext").onclick = () => { QZ.i++; renderQuiz(); };
}
function quizResult() {
    const pct = Math.round(QZ.score / (QUIZ.length * 5) * 100);
    let msg;
    if (pct >= 90) msg = LANG === "ar" ? "ممتاز! أنت جاهز لمشروع تخرّج في الحوسبة الكمية." : "Excellent! You are ready for a quantum capstone project.";
    else if (pct >= 75) msg = LANG === "ar" ? "جيد جداً! راجع البوابات والتشابك وستتقن الموضوع." : "Very good! Review gates and entanglement to master it.";
    else if (pct >= 50) msg = LANG === "ar" ? "جيد — أعد قراءة المفاهيم الأساسية ثم أعد الاختبار." : "Good — reread the core concepts then retake the quiz.";
    else msg = LANG === "ar" ? "لا بأس! ابدأ من قسم المفاهيم وجرّب النشاطات ثم عد مجدداً." : "No problem! Start from Concepts, try the activities, then come back.";
    $("#quizBar").style.width = "100%";
    $("#quizBody").innerHTML = `
        <div class="quiz-result">
            <div class="result-ring" style="--p:${pct}%"><b>${pct}%</b><small>${QZ.score} / ${QUIZ.length * 5}</small></div>
            <h3>${LANG === "ar" ? "نتيجتك النهائية" : "Your final score"}: ${QZ.score} / ${QUIZ.length * 5}</h3>
            <p>${msg}</p>
            <div class="q-actions" style="justify-content:center">
                <button class="btn btn-primary" id="qAgain">${LANG === "ar" ? "أعد الاختبار" : "Retake quiz"}</button>
                <a class="btn btn-ghost" href="#lab">${LANG === "ar" ? "اذهب إلى المختبر" : "Go to the lab"}</a>
            </div>
        </div>`;
    $("#qAgain").onclick = () => { QZ.i = 0; QZ.score = 0; renderQuiz(); };
}

/* ============ 11) المشاريع ============ */
function renderProjects() {
    const g = $("#projectsGrid"); if (!g) return;
    g.innerHTML = PROJECTS.map(p => `
        <article class="card">
            <div class="card-ic"><svg><use href="#${p.icon}"/></svg></div>
            <h3>${t(p.title)}</h3>
            <span class="en">${p.en}</span>
            <p>${t(p.desc)}</p>
            <div class="proj-meta"><span>${t(p.level)}</span><span>${t(p.time)}</span></div>
            <ul class="proj-steps">${p.steps.map(s => `<li>${t(s)}</li>`).join("")}</ul>
            <button class="gate-try" data-cols='${JSON.stringify(p.cols)}'><svg class="btn-ic"><use href="#ic-play"/></svg>${LANG === "ar" ? "ابدأ داخل Quirk" : "Start in Quirk"}</button>
        </article>`).join("");
    $$("#projectsGrid .gate-try").forEach(b => b.onclick = () => {
        loadCircuit(JSON.parse(b.dataset.cols)); go("#lab");
    });
}

/* ============ 12) قسم المعلم + الطباعة ============ */
function renderTeacher() {
    const wl = $("#wsList");
    if (wl) wl.innerHTML = WORKSHEETS.map(w => `
        <div class="ws-item">
            <svg><use href="#ic-print"/></svg>
            <div class="ws-info"><b>${t(w.title)}</b><small>${t(w.sub)}</small></div>
            <button class="mini-btn" data-ws="${w.id}">${LANG === "ar" ? "طباعة" : "Print"}</button>
        </div>`).join("");
    $$("#wsList [data-ws]").forEach(b => b.onclick = () => printWorksheet(b.dataset.ws));

    const al = $("#assessList");
    if (al) al.innerHTML = ASSESSMENT.map(a => `<li>${t(a)}</li>`).join("");

    const cl = $("#classActList");
    if (cl) cl.innerHTML = CLASS_ACTIVITIES.map(a => `
        <div class="ws-item" style="align-items:flex-start"><svg><use href="#ic-teacher"/></svg>
        <div class="ws-info"><b style="font-weight:600;font-size:14.3px">${t(a)}</b></div></div>`).join("");
}
$("#printAssess").onclick = () => {
    $("#printArea").innerHTML = `
        <h1>${LANG === "ar" ? "أسئلة التقويم — الحوسبة الكمية" : "Assessment Questions — Quantum Computing"}</h1>
        <p>${LANG === "ar" ? "الاسم: ____________________   الصف: ______   التاريخ: __________" : "Name: ____________________   Class: ______   Date: __________"}</p>
        <ol>${ASSESSMENT.map(a => `<li>${t(a)}</li>`).join("")}</ol>
        <div class="foot">${LANG === "ar" ? "منصة اكتشف عالم الحوسبة الكمية — قسم العلوم والتقنية" : "Discover Quantum Computing platform — Science & Technology"}</div>`;
    window.print();
};
function printWorksheet(id) {
    const w = WORKSHEETS.find(x => x.id === id);
    const body = w.body.map(b => {
        if (b.t === "h") return `<h2>${LANG === "ar" ? b.ar : b.en}</h2>`;
        if (b.t === "q") return `<li>${LANG === "ar" ? b.ar : b.en}</li>`;
        if (b.t === "lines") return `<div class="ws-lines">${Array.from({ length: b.n }, () => `<div class="ws-line"></div>`).join("")}</div>`;
        return "";
    });
    $("#printArea").innerHTML = `
        <h1>${t(w.title)}</h1>
        <p><b>${t(w.sub)}</b></p>
        <p>${LANG === "ar" ? "الاسم: ____________________   الصف: ______   التاريخ: __________" : "Name: ____________________   Class: ______   Date: __________"}</p>
        ${body.join("")}
        <div class="foot">${LANG === "ar" ? "منصة اكتشف عالم الحوسبة الكمية — تُطبع لأغراض تعليمية" : "Discover Quantum Computing platform — printed for educational use"}</div>`;
    window.print();
}

/* ============ 13) المساعد التعليمي الذكي ============ */
const panel = $("#assistantPanel"), msgs = $("#chatMessages");
let welcomed = false;
function renderWelcome() {
    if (!msgs) return;
    if (msgs.children.length) return;   /* نحتفظ بالمحادثة الحالية */
    msgs.innerHTML = "";
    addMsg("bot", LANG === "ar"
        ? "أهلاً بك! أنا المساعد الكمّي 🤖 — اسألني عن الكيوبت، التراكب، التشابك، البوابات، أو كيف تستخدم Quirk.\nأستطيع أيضاً تحميل تجربة مناسبة داخل المحاكي مباشرة."
        : "Hello! I am the Quantum Assistant — ask me about qubits, superposition, entanglement, gates, or how to use Quirk.\nI can also load a matching experiment into the simulator.");
    welcomed = true;
}
function addMsg(who, text, exp) {
    const d = document.createElement("div");
    d.className = "msg " + who; d.textContent = text;
    if (exp) {
        const b = document.createElement("button");
        b.className = "m-act"; b.textContent = (LANG === "ar" ? "شغّل في Quirk: " : "Run in Quirk: ") + t(exp.name);
        b.onclick = () => { loadCircuit(exp.cols); go("#lab"); };
        d.appendChild(b);
    }
    msgs.appendChild(d); msgs.scrollTop = msgs.scrollHeight;
}
$("#assistantFab").onclick = () => {
    panel.classList.toggle("open");
    panel.setAttribute("aria-hidden", panel.classList.contains("open") ? "false" : "true");
    if (panel.classList.contains("open")) { renderWelcome(); $("#chatText").focus(); }
};
$("#asClose").onclick = () => { panel.classList.remove("open"); panel.setAttribute("aria-hidden", "true"); };
function renderSuggestions() {
    $("#chatSuggestions").innerHTML = AI_SUGGESTIONS.map(s => `<button class="sug">${s[LANG] || s.ar}</button>`).join("");
    $$("#chatSuggestions .sug").forEach(b => b.onclick = () => { $("#chatText").value = b.textContent; $("#chatForm").requestSubmit(); });
}
$("#chatForm").addEventListener("submit", e => {
    e.preventDefault();
    const q = $("#chatText").value.trim(); if (!q) return;
    addMsg("user", q); $("#chatText").value = "";
    setTimeout(() => botAnswer(q), 350);
});
function botAnswer(q) {
    const nq = norm(q);
    let best = null, bestScore = 0;
    AI_KB.forEach(item => {
        if (!item.k) return;
        let sc = 0;
        item.k.forEach(k => { if (nq.includes(norm(k))) sc += norm(k).length; });
        if (sc > bestScore) { bestScore = sc; best = item; }
    });
    if (best) { addMsg("bot", t(best.a), best.exp && !best.exp.null ? best.exp : null); return; }
    /* رد افتراضي مفيد */
    addMsg("bot", LANG === "ar"
        ? "سؤال ممتاز! لم أجد إجابة دقيقة له، لكن جرّب صياغة أبسط مثل: «ما هو الكيوبت؟» أو «اشرح التشابك» أو «كيف أستخدم Quirk؟».\nكما يمكنك فتح قسم «المفاهيم الأساسية» وتجربة الأنشطة الأربعة."
        : "Great question! I do not have a precise answer yet — try a simpler phrasing like “What is a qubit?”, “Explain entanglement” or “How do I use Quirk?”. You can also open Core Concepts and try the four activities.");
}

/* ============ 14) التشغيل الأولي ============ */
applyLang();          /* يبني كل المحتوى */
applyTheme();
renderSuggestions();
renderWelcome();
$("#a1Feedback").hidden = true;
a1Bars();
a3Render();
a4Render();
renderQuiz();
showExperiment(EXPERIMENTS[0].id);
loadCircuit(EXPERIMENTS[0].cols);
