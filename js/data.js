/* =========================================================
   data.js — محتوى الموقع التعليمي (مفاهيم، بوابات، تجارب، اختبارات)
   كل النصوص ثنائية اللغة: ar = العربية ، en = الإنجليزية
   ========================================================= */

/* ---------- المفاهيم الأساسية الستة ---------- */
const CONCEPTS = [
    {
        id: "qubit",
        icon: "ic-atom",
        title: { ar: "ما هو الكيوبت؟", en: "What is a Qubit?" },
        en: "QUBIT",
        short: {
            ar: "الكيوبت هو وحدة المعلومات الكمية، ويمكن أن يكون في الحالة 0 و1 في آنٍ واحد.",
            en: "The qubit is the quantum information unit; it can be 0 and 1 at the same time."
        },
        long: [
            { ar: "في الحوسبة التقليدية نستخدم البت (Bit) الذي يأخذ قيمة 0 أو 1 فقط. أما الكيوبت (Quantum Bit) فهو النسخة الكمية منه، ويُمثَّل رياضياً بالمقدار |ψ⟩ = α|0⟩ + β|1⟩، حيث α وβ أعدادا معاملة (Amplitudes).",
              en: "Classical computers use bits that are either 0 or 1. A qubit is the quantum version, written as |ψ⟩ = α|0⟩ + β|1⟩, where α and β are complex amplitudes." },
            { ar: "الحالة |0⟩ تقابل البت الصفر، والحالة |1⟩ تقابل البت الواحد، أما الحالة المختلطة فهي التراكب. مربع القيمة المطلقة للمعامل يعطي احتمال كل نتيجة عند القياس، وجموعها = 1.",
              en: "|0⟩ corresponds to bit 0, |1⟩ to bit 1, and their mix is superposition. The squared magnitude of an amplitude gives the probability of each outcome, and they sum to 1." },
            { ar: "فيزيائياً يمكن تنفيذ كيوبت بجسيم مثل: اتجاه غزل الإلكترون، أو استقطاب الفوتون، أو مستوى الطاقة في ذرة. أي نظام كمي ثنائي الحالات يصلح.",
              en: "Physically a qubit can be an electron spin, a photon polarization, or an atomic energy level: any two-level quantum system works." }
        ],
        points: [
            { ar: "يُكتب بالصيغة |ψ⟩ = α|0⟩ + β|1⟩ مع |α|²+|β|² = 1.", en: "Written as |ψ⟩ = α|0⟩ + β|1⟩ with |α|²+|β|² = 1." },
            { ar: "المعاملات α و β أعداد مركبة (فيزيائية وطور).", en: "α and β are complex numbers (magnitude and phase)." },
            { ar: "عند القياس يخرج نتيجة عشوائية: 0 باحتمال |α|² و 1 باحتمال |β|².", en: "Measurement is random: 0 with probability |α|², 1 with probability |β|²." },
            { ar: "n كيوبت يمثّل 2ⁿ حالة في آنٍ واحد.", en: "n qubits represent 2ⁿ states at once." }
        ],
        illu: "qubit",
        example: "qubit",
        cols: [["H"], ["Measure"]]
    },
    {
        id: "bitqubit",
        icon: "ic-grid",
        title: { ar: "الفرق بين البت والكيوبت", en: "Bit vs Qubit" },
        en: "BIT vs QUBIT",
        short: {
            ar: "البت حالة واحدة فقط، أما الكيوبت فيحتفظ بكمية من الاحتمالات حتى لحظة القياس.",
            en: "A bit holds one state; a qubit keeps a spread of possibilities until measured."
        },
        long: [
            { ar: "البت (Bit) ثنائي القيمة: 0 أو 1 بشكل حاسم ولا وسيط. المعلومة تُخزَّن كتتابع من البتات (011010...).",
              en: "A bit is strictly 0 or 1 with nothing in between. Information is stored as bit strings (011010...)." },
            { ar: "الكيوبت يحمل تراكباً لحالتين مع طورين نسبيين، لذلك n كيوبت يمثّل 2ⁿ حالة معاً، بينما n بت يمثل حالة واحدة فقط. من هنا تأتي قوة الخوارزميات الكمية في البحث والتشابك.",
              en: "A qubit carries a superposition of both states with relative phases, so n qubits represent 2ⁿ states simultaneously, while n bits represent only one. This is the source of quantum speedups." },
            { ar: "لكن هذه القوة ليست مجاناً: لا يمكن نسخ الكيوبت (No-Cloning)، ويصعب قراءته دون تغييره، ويحتاج بيئة معزولة جداً من الضوضاء (Decoherence).",
              en: "The power is not free: qubits cannot be copied (no-cloning), reading them changes them, and they need extreme isolation from noise (decoherence)." }
        ],
        points: [
            { ar: "البت: قيمتان ثابتتان. الكيوبت: احتمالات مستمرة حتى القياس.", en: "Bit: two fixed values. Qubit: continuous probabilities until measurement." },
            { ar: "n بت → قيمة واحدة. n كيوبت → 2ⁿ حالة.", en: "n bits → one value. n qubits → 2ⁿ states." },
            { ar: "البت سهل النسخ والتخزين، الكيوبت حساس جداً.", en: "Bits are easy to copy and store; qubits are extremely fragile." },
            { ar: "الكمية ليست «أسرع دائماً» بل مناسبة لبعض المشكلات فقط.", en: "Quantum is not always faster — only for certain problems." }
        ],
        illu: "compare",
        example: "compare",
        cols: [["X"], ["Measure"]]
    },
    {
        id: "superposition",
        icon: "ic-atom",
        title: { ar: "التراكب الكمي Superposition", en: "Quantum Superposition" },
        en: "SUPERPOSITION",
        short: {
            ar: "الكيوبت يمكن أن يكون |0⟩ و|1⟩ معاً حتى نقيسه، عندها ينهار إلى إحداهما.",
            en: "A qubit can be both |0⟩ and |1⟩ until measured, then it collapses to one."
        },
        long: [
            { ar: "التراكب يعني وجود الحالتين معاً بوزن احتمالي. البوابة H هي أشهر بوابة تُنشئ التراكب: H|0⟩ = (|0⟩+|1⟩)/√2 وتُسمى الحالة |+⟩.",
              en: "Superposition means both states exist with probability weights. The H gate creates it: H|0⟩ = (|0⟩+|1⟩)/√2, called the |+⟩ state." },
            { ar: "من جهة رياضية المعاملات تُجمع مثل الموجات، وقد يتداخل إيجاباً (تعزيز) أو سلباً (إلغاء). هذا التداخل هو ما يجعل بعض الخوارزميات الكمية فعّالة.",
              en: "Amplitudes add like waves and can interfere constructively (boost) or destructively (cancel). This interference is what makes quantum algorithms effective." },
            { ar: "التراكب لا يعني «الحالة 0 و1 معاً بمعنى حرفي» بل معاملات فيزيائية؛ فعند القياس تظهر النتيجة دائماً 0 أو 1 فقط، أبداً رقماً كسرياً.",
              en: "Superposition does not mean '0 and 1 at once' literally; it means amplitudes. Measurement always yields 0 or 1, never a fraction." }
        ],
        points: [
            { ar: "H|0⟩ = |+⟩ و H|1⟩ = |−⟩.", en: "H|0⟩ = |+⟩ and H|1⟩ = |−⟩." },
            { ar: "القياس يُنهار للحالة 0 أو 1 باحتمال ناتج من المعاملات.", en: "Measurement collapses to 0 or 1 with amplitude-derived probability." },
            { ar: "التداخل الكمي أساس تسريع الخوارزميات.", en: "Quantum interference powers algorithmic speedups." }
        ],
        illu: "superposition",
        example: "superposition",
        cols: [["H"], ["Measure"]]
    },
    {
        id: "entanglement",
        icon: "ic-puzzle",
        title: { ar: "التشابك الكمي Entanglement", en: "Quantum Entanglement" },
        en: "ENTANGLEMENT",
        short: {
            ar: "كيوبتان متشابكان: قياس أحدهما يحدد الآخر فوراً مهما بعدت المسافة.",
            en: "Two entangled qubits: measuring one instantly fixes the other, however far apart."
        },
        long: [
            { ar: "التشابك حالة كمية لا تُحلَّل إلى حالتين مستقلين. أشهر مثال هي حالة بيل: |00⟩+|11⟩ فوق √2، أي أن الكيوبتين إما 00 أو 11 لكن لا نعرف أيهما قبل القياس.",
              en: "Entanglement is a joint state that cannot be split into independent states. The Bell state (|00⟩+|11⟩)/√2 means both qubits are 00 or 11 together, unknown before measurement." },
            { ar: "تُبنى ببوابة H على كيوبت ثم بوابة CNOT بينهما. عند قياس الأول نعرف الثاني فوراً؛ وهذا «التأثير الشبحي» لا ينقل معلومات بنفس السرعة لأن النتيجة عشوائية.",
              en: "It is built with H on one qubit followed by CNOT. Measuring the first reveals the second instantly; this 'spooky action' cannot send information faster than light because results are random." },
            { ar: "التشابك أساس لصالات القياس (Quantum Teleportation) وتكرار الأخطاء الكمية والحوسبة الموزعة.",
              en: "Entanglement underpins teleportation, quantum error correction and distributed computing." }
        ],
        points: [
            { ar: "حالة بيل: (|00⟩+|11⟩)/√2.", en: "Bell state: (|00⟩+|11⟩)/√2." },
            { ar: "البناء: H ثم CNOT.", en: "Construction: H then CNOT." },
            { ar: "قياس أحدهما يُحدّد الآخر (دالة موجية مشتركة).", en: "Measuring one determines the other (joint wavefunction)." },
            { ar: "لا يمكن استخدامه لنقل إشارة أسرع من الضوء.", en: "It cannot be used to signal faster than light." }
        ],
        illu: "entangle",
        example: "entangle",
        cols: [["H"], ["•", "X"], ["Measure", "Measure"]]
    },
    {
        id: "measurement",
        icon: "ic-target",
        title: { ar: "القياس Measurement", en: "Measurement" },
        en: "MEASUREMENT",
        short: {
            ar: "القياس يحوّل الحالة الكمّية العشوائية إلى رقم واضح: 0 أو 1، ويدمّر التراكب.",
            en: "Measurement turns the fuzzy quantum state into a definite 0 or 1, destroying superposition."
        },
        long: [
            { ar: "القياس عملية غير عكسية: قبله احتمالات، وبعده نتيجة مؤكدة. احتمال الحصول على 0 هو |α|² وعلى 1 هو |β|².",
              en: "Measurement is irreversible: probabilities before, a definite outcome after. Probability of 0 is |α|² and of 1 is |β|²." },
            { ar: "لو كرّرنا القياس 100 مرة على دائرة H فسنرى تقريباً 50 قفزة و50 قفزاً؛ هذا ما يفعله محاكي Quirk في لوحة القياس.",
              en: "Repeating the measurement 100 times on an H circuit gives about 50 zeros and 50 ones — exactly what Quirk's display shows." },
            { ar: "في الدوائر الكلاسيكية القياس لا يغيّر القيمة، بينما في الكمي يُحدث «انهيار الدالة الموجية» ويُفقد التراكب.",
              en: "Classical reading does not change a value; quantum measurement collapses the wavefunction and destroys superposition." }
        ],
        points: [
            { ar: "P(0) = |α|² , P(1) = |β|².", en: "P(0) = |α|² , P(1) = |β|²." },
            { ar: "لا يمكن قياس الكيوبت دون التأثير عليه.", en: "You cannot measure a qubit without affecting it." },
            { ar: "القياس المتكرر يعطي إحصاءً يطابق النسب المتوقعة.", en: "Repeated shots produce statistics matching the expected ratios." },
            { ar: "بعد القياس تعود الحالة إلى |0⟩ أو |1⟩.", en: "Afterwards the state is |0⟩ or |1⟩ again." }
        ],
        illu: "measure",
        example: "measure",
        cols: [["H"], ["Measure"]]
    },
    {
        id: "gates",
        icon: "ic-grid",
        title: { ar: "البوابات الكمية Quantum Gates", en: "Quantum Gates" },
        en: "QUANTUM GATES",
        short: {
            ar: "البوابة الكمية رياضيات وحدوية تُغيّر حالة الكيوبت، وهي المكوّن الأساسي للدائرة الكمية.",
            en: "A quantum gate is a unitary operation that changes a qubit's state — the building block of circuits."
        },
        long: [
            { ar: "البوابات الكمّية مصفوفات وحدوية (Transposed Conjugate × نفسها = المصفوفة الواحدة) أي تُحافظ على مجموع الاحتمالات. أشهرها H و X و Z و Y و S و T.",
              en: "Quantum gates are unitary matrices (U†U = I) so they preserve total probability. Famous ones: H, X, Z, Y, S, T." },
            { ar: "البوابات أحادية الخط: لا يمكن نسخ محتوى كيوبت داخل آخر (No-Cloning)، ولذلك توجد بوابات متحكّمة مثل CNOT التي تطبّق X على الهدف فقط إذا كان التحكم = 1.",
              en: "Gates are reversible and single-line: you cannot copy a qubit (no-cloning), hence controlled gates like CNOT apply X to the target only when the control is 1." },
            { ar: "في Quirk تسحب البوابة إلى السلك وتشاهد أثرها فوراً على شكل احتمالات وكرات بلوك، وهذا أفضل طريقة للفهم العملي.",
              en: "In Quirk you drag a gate onto a wire and instantly see probabilities and Bloch spheres update — the best way to learn by doing." }
        ],
        points: [
            { ar: "وحدوية: تحافظ على الاحتمالات.", en: "Unitary: preserves probabilities." },
            { ar: "عكسية: لكل بوابة بوابة عكسية.", en: "Reversible: every gate has an inverse." },
            { ar: "لا تُنتج نسخاً: No-Cloning.", en: "No cloning of quantum information." },
            { ar: "CNOT و SWAP تعمل على كيوبتين معاً.", en: "CNOT and SWAP act on two qubits together." }
        ],
        illu: "gates",
        example: "gates",
        cols: [["H"], ["•", "X"], ["Measure", "Measure"]]
    }
];

/* ---------- البوابات الكمية الثمانية ---------- */
const GATES = [
    {
        id: "X", sym: "X",
        name: { ar: "بوابة X (النَفْي)", en: "X Gate (NOT)" },
        func: { ar: "تقلب الحالة |0⟩ إلى |1⟩ والعكس — وهي مقابل نفّي NOT في الحوسبة التقليدية، وتساوي دوران 180° حول محور X.", en: "Flips |0⟩ to |1⟩ and vice versa — the quantum NOT, a 180° rotation about the X axis." },
        example: { ar: "ابدأ من |0⟩ ثم طبّق X فتحصل على |1⟩ ثم قِس. في Quirk: ضع X ثم Measure.", en: "Start at |0⟩, apply X to get |1⟩, then measure. In Quirk: place X then Measure." },
        matrix: [["0", "1"], ["1", "0"]],
        cols: [["X"], ["Measure"]]
    },
    {
        id: "Y", sym: "Y",
        name: { ar: "بوابة Y", en: "Y Gate" },
        func: { ar: "تدور حول محور Y بمقدار 180°: تحوّل |0⟩ إلى i|1⟩ و|1⟩ إلى −i|0⟩، فهي X مع طور مركّب.", en: "A 180° rotation about Y: |0⟩ → i|1⟩ and |1⟩ → −i|0⟩, i.e. X with a complex phase." },
        example: { ar: "طبّق Y على |0⟩ ثم H ثم قِس؛ ستجد توزيعاً عشوائياً يختلف في الطور عن X.", en: "Apply Y to |0⟩, then H, then measure: you get a random outcome with a different phase than X." },
        matrix: [["0", "−i"], ["i", "0"]],
        cols: [["Y"], ["Measure"]]
    },
    {
        id: "Z", sym: "Z",
        name: { ar: "بوابة Z (الطور)", en: "Z Gate (Phase)" },
        func: { ar: "تُغيّر إشارة |1⟩ إلى −|1⟩ وتخلي |0⟩ كما هي — تُسمى بوابة الطور (نصف دورة حول محور Z).", en: "Flips the sign of |1⟩ to −|1⟩ and leaves |0⟩ alone — a phase gate (half-turn about Z)." },
        example: { ar: "H ثم Z على |0⟩: تحصل على |−⟩ = (|0⟩−|1⟩)/√2 وقيسه للتأكد.", en: "H then Z on |0⟩ gives |−⟩ = (|0⟩−|1⟩)/√2 — measure to confirm." },
        matrix: [["1", "0"], ["0", "−1"]],
        cols: [["H"], ["Z"], ["Measure"]]
    },
    {
        id: "H", sym: "H",
        name: { ar: "بوابة هادامارд H", en: "Hadamard Gate (H)" },
        func: { ar: "بوّابة التراكب: تحوّل |0⟩ إلى |+⟩ و|1⟩ إلى |−⟩، أي تجعل الكيوبت في احتمالية متساوية 50/50.", en: "The superposition gate: |0⟩ → |+⟩ and |1⟩ → |−⟩, giving a 50/50 measurement chance." },
        example: { ar: "ضع H ثم Measure في Quirk وكرّر القياس: نحو نصف النتائج 0 ونصفها 1.", en: "Put H then Measure in Quirk and shoot: roughly half the results are 0 and half are 1." },
        matrix: [["1/√2", "1/√2"], ["1/√2", "−1/√2"]],
        cols: [["H"], ["Measure"]]
    },
    {
        id: "S", sym: "S",
        name: { ar: "بوابة S (ربع دورة)", en: "S Gate (Quarter turn)" },
        func: { ar: "تدور حول محور Z بمقدار 90°: تحوّل |+⟩ إلى |i⟩ أي تضيف طور i = e^{iπ/2} على الحالة |1⟩.", en: "A 90° rotation about Z: it turns |+⟩ into |i⟩, adding phase i = e^{iπ/2} to |1⟩." },
        example: { ar: "H ثم S: افتح دائرة بيل بترتيب مختلف ولاحظ تغيّر لوحة القياس.", en: "H then S: open a Bell-like circuit in a different order and watch the display change." },
        matrix: [["1", "0"], ["0", "i"]],
        cols: [["H"], ["Z^½"], ["Measure"]]
    },
    {
        id: "T", sym: "T",
        name: { ar: "بوابة T (ثمن دورة)", en: "T Gate (Eighth turn)" },
        func: { ar: "تدور بمقدار 45° حول Z وتضيف الطور e^{iπ/4}، وهي أساسية في كثير من خوارزميات التصحيح الكمي.", en: "A 45° Z-rotation adding phase e^{iπ/4}; essential in many error-corrected algorithms." },
        example: { ar: "H ثم T ثم قِس: الاحتمالات تبقى 50/50 لكن الطور يختلف — وهو ما يظهر في التداخل.", en: "H then T then measure: probabilities stay 50/50 but the phase changes — visible in interference." },
        matrix: [["1", "0"], ["0", "e^{iπ/4}"]],
        cols: [["H"], ["T"], ["Measure"]]
    },
    {
        id: "CNOT", sym: "•—X",
        name: { ar: "بوابة CNOT (التحكم بالنفّي)", en: "CNOT (Controlled-NOT)" },
        func: { ar: "بوابة على كيوبتين: إذا كان كيوبت التحكم = 1 فإنها تقلب الهدف X، وإذا كان 0 فلا شيء. وهي أساس بناء التشابك.", en: "A two-qubit gate: if the control qubit is 1 it applies X to the target, otherwise nothing. The backbone of entanglement." },
        example: { ar: "H على التحكم ثم CNOT ← حالة بيل (|00⟩+|11⟩)/√2، ثم قِس الكيوبتين معاً.", en: "H on the control then CNOT → Bell state (|00⟩+|11⟩)/√2; measure both together." },
        matrix: [["1 0 0 0", "0 1 0 0"], ["0 0 0 1", "0 0 1 0"]],
        cols: [["H"], ["•", "X"], ["Measure", "Measure"]]
    },
    {
        id: "SWAP", sym: "⇄",
        name: { ar: "بوابة SWAP (التبديل)", en: "SWAP Gate" },
        func: { ar: "تبديلاً حقيقياً بين حالتَي كيوبتين: |a,b⟩ ← |b,a⟩، وتُبنى من ثلاث بوابات CNOT في الدوائر الفيزيائية.", en: "Actually swaps two qubits: |a,b⟩ → |b,a⟩; in hardware it is built from three CNOTs." },
        example: { ar: "ضع X على السلك الأول ثم SWAP: ستنتقل القفزة إلى السلك الثاني، أي تبادلاً للبيانات.", en: "Put X on the first wire then SWAP: the flip moves to the second wire — data exchange." },
        matrix: [["1 0 0 0", "0 0 1 0"], ["0 1 0 0", "0 0 0 1"]],
        cols: [["X", 1], ["Swap", "Swap"], ["Measure", "Measure"]]
    }
];

/* ---------- الدوائر الجاهزة في المختبر ---------- */
const PRESETS = [
    { id: "x",  label: { ar: "بوابة X", en: "X Gate" }, tag: "X",  cols: [["X"], ["Measure"]] },
    { id: "h",  label: { ar: "بوابة H", en: "H Gate" }, tag: "H",  cols: [["H"], ["Measure"]] },
    { id: "z",  label: { ar: "بوابة Z", en: "Z Gate" }, tag: "Z",  cols: [["H"], ["Z"], ["Measure"]] },
    { id: "cx", label: { ar: "بوابة CNOT", en: "CNOT Gate" }, tag: "CX", cols: [["H"], ["•", "X"], ["Measure", "Measure"]] },
    { id: "bell",label: { ar: "حالة بيل Bell State", en: "Bell State" }, tag: "Bell", cols: [["H"], ["•", "X"], ["Measure", "Measure"], [1, "Bloch"]] }
];

/* ---------- تجارب مختبر Quirk ---------- */
const EXPERIMENTS = [
    {
        id: "bell",
        title: { ar: "تجربة 1: حالة بيل (Entangled Pair)", en: "Experiment 1: Bell State" },
        en: "BELL STATE",
        cols: [["H"], ["•", "X"], ["Measure", "Measure"]],
        theory: {
            ar: "نبني حالة بيل بخطوتين: بوابة H تُدخل الكيوبت الأول في تراكب، ثم بوابة CNOT تربطه بالثاني فتصير الحالة (|00⟩+|11⟩)/√2.",
            en: "We build the Bell state in two steps: H puts qubit 0 into superposition, then CNOT entangles it with qubit 1, giving (|00⟩+|11⟩)/√2."
        },
        goal: {
            ar: "أن يلاحظ الطالب أن نتائج القياس للسكين متشابهة دائماً (00 أو 11) رغم العشوائية.",
            en: "The student should notice that both wires always agree (00 or 11) despite the randomness."
        },
        steps: [
            { ar: "اضغط زر التجربة لتحميل الدائرة في المحاكي.", en: "Press the experiment button to load the circuit into the simulator." },
            { ar: "راقب لوحة القياس في الأسفل: ستظهر نسب 50% لـ 00 و 50% لـ 11.", en: "Watch the display below: it shows 50% for 00 and 50% for 11." },
            { ar: "أعد المحاكاة عدة مرات (Shoot) وسجّل عشر نتائج.", en: "Re-run (Shoot) several times and record ten results." },
            { ar: "احذف بوابة H ثم أعد التجربة: ماذا يحدث للتشابك؟", en: "Delete the H gate and repeat: what happens to entanglement?" }
        ],
        observe: {
            ar: "لا تظهر أبداً نتائج 01 أو 10 — الكيوبتان يتصرفان ككيوبت واحد متشابك، ولو حذفت H انتهى التشابك.",
            en: "You never see 01 or 10 — the pair behaves as one entangled unit, and removing H destroys the entanglement."
        }
    },
    {
        id: "sup",
        title: { ar: "تجربة 2: التراكب والقياس العشوائي", en: "Experiment 2: Superposition & Randomness" },
        en: "SUPERPOSITION",
        cols: [["H"], ["Measure"]],
        theory: {
            ar: "بوابة H تحوّل |0⟩ إلى |+⟩ = (|0⟩+|1⟩)/√2، أي احتمال متساوٍ للنتيجتين، ثم القياس يُنهار لواحدة منها.",
            en: "H turns |0⟩ into |+⟩ = (|0⟩+|1⟩)/√2, an equal mix, and measurement collapses it to one outcome."
        },
        goal: {
            ar: "اكتشاف أن قياساً واحداً عشوائي، لكن إحصاء 100 قياس يعطي تقريباً 50/50.",
            en: "Discover that one shot is random, but 100 shots give roughly 50/50."
        },
        steps: [
            { ar: "حمّل الدائرة واضغط Shoot لقياس واحد.", en: "Load the circuit and press Shoot for a single shot." },
            { ar: "اضغط 100 Shots لجمع عيّنة كبيرة.", en: "Press 100 Shots to collect a large sample." },
            { ar: "قارن النسبة العملية بالنظرية 50%.", en: "Compare the measured ratio with the theoretical 50%." },
            { ar: "جرّب إضافة X قبل H: هل يتغير الاحتمال؟ ولماذا؟", en: "Try adding X before H: does the probability change? Why?" }
        ],
        observe: {
            ar: "النتيجة الواحدة لا يمكن توقّعها، لكن المنحنى الإحصائي يستقر حول 50%: العشوائية في القياس لا في القانون.",
            en: "A single outcome is unpredictable, but the histogram settles near 50%: randomness is in the measurement, not the law."
        }
    },
    {
        id: "chsh",
        title: { ar: "تجربة 3: تأثير Z والتشابك (Phase)", en: "Experiment 3: Z Effect & Phase" },
        en: "PHASE Z",
        cols: [["H"], ["•", "X"], ["Z", 1], ["Measure", "Measure"]],
        theory: {
            ar: "بوابة Z تغيّر إشارة المعامل الخاص بـ |1⟩؛ على حالة بيل تُنتج الحالة (|00⟩−|11⟩)/√2، وهي حالة بيل أخرى بنفس الاحتمالات لكن طور مختلف.",
            en: "Z flips the sign of the |1⟩ amplitude; on a Bell pair it yields (|00⟩−|11⟩)/√2 — same probabilities, different phase."
        },
        goal: {
            ar: "تمييز أن الاحتمالات لا تتغيّر بينما الطور يتغيّر، وهذا ما يخفيه القياس العادي.",
            en: "See that probabilities stay the same while the phase changes — something ordinary measurement hides."
        },
        steps: [
            { ar: "شغّل الدائرة ولاحظ نسب القياس.", en: "Run the circuit and read the ratios." },
            { ar: "احذف Z وأعد التشغيل: هل تختلف النسب؟", en: "Remove Z and rerun: do the ratios change?" },
            { ar: "استبدل Z بـ H لتركيب تشابك مختلف وقارن.", en: "Replace Z with H to build a different entanglement and compare." }
        ],
        observe: {
            ar: "نسب القياس 50/50 في الحالتين، لكن الفرق بين |00⟩+|11⟩ و|00⟩−|11⟩ يظهر عند إضافة بوابة H إضافية (تجربة التداخل).",
            en: "Both give 50/50 measurements; the +/− difference appears when you add an extra H (an interference test)."
        }
    },
    {
        id: "swap",
        title: { ar: "تجربة 4: تبديل البيانات بـ SWAP", en: "Experiment 4: Data Swap" },
        en: "SWAP",
        cols: [["X", 1], ["Swap", "Swap"], ["Measure", "Measure"]],
        theory: {
            ar: "نطبّق X على السلك الأول فقط، ثم نطبّق SWAP لنقل الحالة بين السلكين.",
            en: "We apply X only to the first wire, then SWAP to move the state between wires."
        },
        goal: {
            ar: "فهم أن المعلومات الكمّية تنتقل بين الكيوبتين دون نسخها.",
            en: "Understand that quantum information moves between qubits without being copied."
        },
        steps: [
            { ar: "حمّل الدائرة ولاحظ أن النتيجة 01 (القفزة انتقلت).", en: "Load the circuit: the result is 01 (the flip moved)." },
            { ar: "أضف Measure على السلك الثاني قبل SWAP ولاحظ اختلاف المنطق.", en: "Add Measure on wire 2 before SWAP and observe the difference." },
            { ar: "جرّب X على السلكين معاً ثم SWAP: ما النتيجة؟", en: "Try X on both wires then SWAP: what is the result?" }
        ],
        observe: {
            ar: "|10⟩ تصبح |01⟩ بعد SWAP: تبديل حقيقي للحالة وليس نسخاً، لأن النسخ ممنوع فيزيائياً (No-Cloning).",
            en: "|10⟩ becomes |01⟩ after SWAP: a real exchange, not a copy — copying is forbidden physically (no-cloning)."
        }
    },
    {
        id: "ghz",
        title: { ar: "تجربة 5: حالة GHZ ثلاثية الكيوبتات", en: "Experiment 5: 3-Qubit GHZ" },
        en: "GHZ STATE",
        cols: [["H"], ["•", "X"], ["•", 1, "X"], ["Measure", "Measure", "Measure"]],
        theory: {
            ar: "نطبّق H ثم CNOT متسلسلتين لبناء الحالة (|000⟩+|111⟩)/√2 وتُسمى GHZ، وهي تعميم حالة بيل لثلاثة كيوبتات.",
            en: "H followed by two CNOTs builds (|000⟩+|111⟩)/√2, the GHZ state — a three-qubit generalization of Bell."
        },
        goal: {
            ar: "رؤية أن الثلاثة كيوبتات تعطي 000 أو 111 فقط، أي تشابك ممتد.",
            en: "See that the three qubits give only 000 or 111 — multipartite entanglement."
        },
        steps: [
            { ar: "حمّل الدائرة وشغّل 100 قياس.", en: "Load the circuit and take 100 shots." },
            { ar: "راقب لوحة القياس: هل تظهر 010 أو 101؟", en: "Watch the display: do you see 010 or 101?" },
            { ar: "احذف CNOT الثانية ولاحظ نصف التشابك المفقود.", en: "Remove the second CNOT and notice the lost entanglement." }
        ],
        observe: {
            ar: "ستظهر 000 و 111 فقط؛ أي تشويش وسيط يكسر التشابك فوراً ويسمح بظهور قيم أخرى.",
            en: "Only 000 and 111 appear; any middle noise instantly breaks entanglement and lets other values show."
        }
    },
    {
        id: "interf",
        title: { ar: "تجربة 6: التداخل الكمي H–H", en: "Experiment 6: Quantum Interference (H–H)" },
        en: "INTERFERENCE",
        cols: [["H"], ["H"], ["Measure"]],
        theory: {
            ar: "بوابة H مرتين = هوية: التراكب يُنشأ ثم يُلغى بعملية التداخل (H² = I)، فتعود الحالة إلى |0⟩ تماماً.",
            en: "H twice is the identity: the superposition is created then cancelled by interference (H² = I), returning to |0⟩."
        },
        goal: {
            ar: "إدراك أن المعاملات تتداخل كالموجات وأن بعض الطرق يمكن إلغاؤها تماماً.",
            en: "Realize amplitudes interfere like waves and some paths cancel completely."
        },
        steps: [
            { ar: "شغّل الدائرة مع H واحدة فقط: 50/50.", en: "Run with a single H: 50/50." },
            { ar: "أضف H ثانية وأعد القياس: النتيجة 0 دائماً.", en: "Add a second H: the result is always 0." },
            { ar: "اجعل الثانية Z بدل H وقارن النتيجة.", en: "Make the second gate Z instead of H and compare." }
        ],
        observe: {
            ar: "الحالة تعود إلى |0⟩ بنسبة 100% — هذا هو التداخل الإيجابي الذي تعتمد عليه الخوارزميات الكمّية مثل Grover.",
            en: "The state returns to |0⟩ with 100% probability — the constructive interference quantum algorithms like Grover rely on."
        }
    }
];

/* ---------- الأنشطة: مهام النشاط 3 ---------- */
const A3_TASKS = [
    { from: { ar: "|0⟩", en: "|0⟩" }, to: { ar: "|1⟩", en: "|1⟩" }, options: ["X", "H", "Z"], answer: "X",
      why: { ar: "بوابة X تقلب الحالة |0⟩ إلى |1⟩ مثل نفّي NOT.", en: "Gate X flips |0⟩ to |1⟩, like classical NOT." } },
    { from: { ar: "|0⟩", en: "|0⟩" }, to: { ar: "|+⟩", en: "|+⟩" }, options: ["X", "H", "Z"], answer: "H",
      why: { ar: "بوابة H تُدخل التراكب: H|0⟩ = (|0⟩+|1⟩)/√2 = |+⟩.", en: "Gate H creates superposition: H|0⟩ = |+⟩." } },
    { from: { ar: "|1⟩", en: "|1⟩" }, to: { ar: "|−⟩", en: "|−⟩" }, options: ["X", "H", "Z"], answer: "H",
      why: { ar: "H|1⟩ = (|0⟩−|1⟩)/√2 = |−⟩، أي تراكب بإشارة سالبة.", en: "H|1⟩ = (|0⟩−|1⟩)/√2 = |−⟩, a superposition with a minus sign." } },
    { from: { ar: "|+⟩", en: "|+⟩" }, to: { ar: "|−⟩", en: "|−⟩" }, options: ["X", "H", "Z"], answer: "Z",
      why: { ar: "بوابة Z تقلب إشارة |1⟩ فقط فتصبح (|0⟩−|1⟩)/√2 = |−⟩.", en: "Z flips the sign of |1⟩ only, giving (|0⟩−|1⟩)/√2 = |−⟩." } },
    { from: { ar: "|−⟩", en: "|−⟩" }, to: { ar: "|1⟩", en: "|1⟩" }, options: ["X", "H", "Z"], answer: "H",
      why: { ar: "H تُلغي التراكب: H|−⟩ = |1⟩ (لأن H² = هوية).", en: "H undoes superposition: H|−⟩ = |1⟩ (since H² = I)." } }
];

/* ---------- جولات النشاط 4 (السحب والأفلت) ---------- */
const A4_ROUNDS = [
    { target: { ar: "|1⟩", en: "|1⟩" }, state: [[0, 0], [1, 0]] },
    { target: { ar: "|−⟩", en: "|−⟩" }, state: [[Math.SQRT1_2,0],[-Math.SQRT1_2,0]] },
    { target: { ar: "(|0⟩+i|1⟩)/√2", en: "(|0⟩+i|1⟩)/√2" }, state: [[Math.SQRT1_2,0],[0,Math.SQRT1_2]] },
    { target: { ar: "−|1⟩", en: "−|1⟩" }, state: [[0,0],[-1,0]] }
];

/* ---------- الاختبار التفاعلي (20 سؤالاً) ---------- */
const QUIZ = [
    { q: { ar: "ما الوحدة الأساسية للمعلومة في الحوسبة التقليدية؟", en: "What is the basic unit of classical information?" },
      o: [{ ar:"الكيوبت", en:"Qubit" }, { ar:"البت", en:"Bit" }, { ar:"البوابة", en:"Gate" }, { ar:"الملف", en:"File" }],
      a: 1, e: { ar: "البت Bit يأخذ قيمتين فقط: 0 أو 1.", en: "A bit has only two values: 0 or 1." } },
    { q: { ar: "ما الوحدة الأساسية في الحوسبة الكمية؟", en: "What is the basic unit of quantum computing?" },
      o: [{ ar:"البايت", en:"Byte" }, { ar:"الصفحة", en:"Page" }, { ar:"الكيوبت", en:"Qubit" }, { ar:"المسار", en:"Track" }],
      a: 2, e: { ar: "الكيوبت هو النسخة الكمية من البت.", en: "The qubit is the quantum version of the bit." } },
    { q: { ar: "أي حالة لا يمكن أن يأخذها البت التقليدي؟", en: "Which state can a classical bit NOT take?" },
      o: [{ ar:"0", en:"0" }, { ar:"1", en:"1" }, { ar:"التراكب (0 و1 معاً)", en:"Superposition (0 and 1)" }, { ar:"لا شيء مما سبق", en:"None of these" }],
      a: 2, e: { ar: "التراكب ميزة كميّة خاصة بالكيوبت.", en: "Superposition is unique to qubits." } },
    { q: { ar: "ماذا تفعل بوابة H على الحالة |0⟩؟", en: "What does the H gate do to |0⟩?" },
      o: [{ ar:"تُبقيها |0⟩", en:"Keeps |0⟩" }, { ar:"تُحوّلها إلى |1⟩", en:"Turns it into |1⟩" }, { ar:"تُحوّلها إلى تراكب |+⟩", en:"Turns it into |+⟩" }, { ar:"تُتلف الكيوبت", en:"Destroys the qubit" }],
      a: 2, e: { ar: "H|0⟩ = (|0⟩+|1⟩)/√2 وهي الحالة |+⟩.", en: "H|0⟩ = (|0⟩+|1⟩)/√2, the |+⟩ state." } },
    { q: { ar: "بوابة X تقابل أي بوابة منطقية تقليدية؟", en: "Which classical gate does X correspond to?" },
      o: [{ ar:"AND", en:"AND" }, { ar:"OR", en:"OR" }, { ar:"NOT", en:"NOT" }, { ar:"NAND", en:"NAND" }],
      a: 2, e: { ar: "X تقلب 0 إلى 1 والعكس، أي NOT.", en: "X flips 0 to 1 and back — NOT." } },
    { q: { ar: "التشابك الكمي يعني:", en: "Quantum entanglement means:" },
      o: [{ ar:"توصيل الأسلاك في لوحة الدوائر", en:"Wiring the circuit board" },
          { ar:"قياس أحدهما يحدد الآخر فوراً", en:"Measuring one instantly determines the other" },
          { ar:"أن الكيوبتين متطابقاً دائماً", en:"The two qubits are always identical" },
          { ar:"أن السرعة تزداد", en:"Speed increases" }],
      a: 1, e: { ar: "حالة كميّة مشتركة لا يمكن حلّها إلى حالتين مستقلتين.", en: "A joint state that cannot be split into two independent states." } },
    { q: { ar: "عند قياس الحالة |+⟩ فإن النتيجة تكون:", en: "Measuring |+⟩ gives:" },
      o: [{ ar:"0 دائماً", en:"Always 0" }, { ar:"1 دائماً", en:"Always 1" }, { ar:"0 أو 1 احتمال 50% لكل منهما", en:"0 or 1 with 50% each" }, { ar:"قيمة كسرية", en:"A fraction" }],
      a: 2, e: { ar: "المعاملان متساويان: |1/√2|² = 0.5.", en: "Equal amplitudes: |1/√2|² = 0.5." } },
    { q: { ar: "أي بوابات تُستخدم لبناء حالة بيل؟", en: "Which gates build a Bell state?" },
      o: [{ ar:"X ثم Z", en:"X then Z" }, { ar:"H ثم CNOT", en:"H then CNOT" }, { ar:"H فقط", en:"H only" }, { ar:"SWAP فقط", en:"SWAP only" }],
      a: 1, e: { ar: "H تُنشئ التراكب و CNOT تُنشئ التشابك.", en: "H creates superposition, CNOT creates entanglement." } },
    { q: { ar: "بوابة Z تقوم بـ:", en: "The Z gate:" },
      o: [{ ar:"تقلب |0⟩ إلى |1⟩", en:"Flips |0⟩ to |1⟩" }, { ar:"تُنشئ تراكباً", en:"Creates superposition" },
          { ar: "تُغيّر إشارة |1⟩ فقط", en:"Changes the sign of |1⟩ only" }, { ar:"تتبادل كيوبتين", en:"Swaps two qubits" }],
      a: 2, e: { ar: "Z: |0⟩→|0⟩ و |1⟩→−|1⟩ (بوابة طور).", en: "Z: |0⟩→|0⟩ and |1⟩→−|1⟩ (phase gate)." } },
    { q: { ar: "ما المبدأ الذي يمنع نسخ حالة كيوبت؟", en: "Which principle forbids copying a qubit?" },
      o: [{ ar:"No-Cloning", en:"No-Cloning" }, { ar:"No-Following", en:"No-Following" }, { ar:"Copy-Right", en:"Copy-Right" }, { ar:"Speed-Limit", en:"Speed-Limit" }],
      a: 0, e: { ar: "مبدأ عدم النسخ ناتج رياضي مثبت في الميكانيكا الكمّية.", en: "No-cloning is a proven theorem of quantum mechanics." } },
    { q: { ar: "في بوابة CNOT فإن الكيوبت الأول يُسمى:", en: "In CNOT, the first qubit is called:" },
      o: [{ ar:"الهدف", en:"Target" }, { ar:"التحكم", en:"Control" }, { ar:"المفتاح", en:"Key" }, { ar:"الناتج", en:"Output" }],
      a: 1, e: { ar: "التحكم (•) يقرر هل تُطبَّق X على الهدف.", en: "The control (•) decides whether X is applied to the target." } },
    { q: { ar: "القياس في الميكانيكا الكمّية يُسمى:", en: "Quantum measurement is also called:" },
      o: [{ ar:"انهيار الدالة الموجية", en:"Wavefunction collapse" }, { ar:"انفجار الموجة", en:"Wave explosion" }, { ar:"تداخل", en:"Interference" }, { ar:"تشويش", en:"Noise" }],
      a: 0, e: { ar: "تنتقل من احتمالات إلى حالة مؤكدة واحدة.", en: "It goes from probabilities to one definite state." } },
    { q: { ar: "كم حالة تمثّل كيوبتان معاً؟", en: "How many states do two qubits represent?" },
      o: [{ ar:"2", en:"2" }, { ar:"3", en:"3" }, { ar:"4", en:"4" }, { ar:"8", en:"8" }],
      a: 2, e: { ar: "2ⁿ حيث n=2 ← 4 حالات: 00 و 01 و 10 و 11.", en: "2ⁿ with n=2 → 4 states: 00, 01, 10, 11." } },
    { q: { ar: "n كيوبت يمثّل عدداً من الحالات يساوي:", en: "n qubits represent how many states?" },
      o: [{ ar:"2n", en:"2n" }, { ar:"n²", en:"n²" }, { ar:"2ⁿ", en:"2ⁿ" }, { ar:"n!", en:"n!" }],
      a: 2, e: { ar: "النمو الأسّي هو مصدر القوة والصعوبة معاً.", en: "Exponential growth is both the power and the difficulty." } },
    { q: { ar: "بوابة S تضيف طوراً مقداره:", en: "The S gate adds a phase of:" },
      o: [{ ar:"90° (i)", en:"90° (i)" }, { ar:"45°", en:"45°" }, { ar:"180°", en:"180°" }, { ar:"0°", en:"0°" }],
      a: 0, e: { ar: "S تدور 90° حول محور Z.", en: "S rotates 90° about the Z axis." } },
    { q: { ar: "بوابة T تضيف طوراً مقداره:", en: "The T gate adds a phase of:" },
      o: [{ ar:"π/2", en:"π/2" }, { ar:"π/4", en:"π/4" }, { ar:"π", en:"π" }, { ar:"π/8", en:"π/8" }],
      a: 1, e: { ar: "T تدور 45° = π/4 حول Z.", en: "T rotates 45° = π/4 about Z." } },
    { q: { ar: "بوابة SWAP تعمل على:", en: "The SWAP gate acts on:" },
      o: [{ ar:"كيوبت واحد", en:"One qubit" }, { ar:"كيوبتين", en:"Two qubits" }, { ar:"ثلاثة كيوبتات", en:"Three qubits" }, { ar:"لا شيء", en:"Nothing" }],
      a: 1, e: { ar: "|a,b⟩ ← |b,a⟩ أي تبديل بين سلكين.", en: "|a,b⟩ ← |b,a⟩, exchanging two wires." } },
    { q: { ar: "أي مما يلي ليس بوابة كميّة؟", en: "Which of these is NOT a quantum gate?" },
      o: [{ ar:"Hadamard", en:"Hadamard" }, { ar:"Pauli-X", en:"Pauli-X" }, { ar:"CNOT", en:"CNOT" }, { ar:"AND", en:"AND" }],
      a: 3, e: { ar: "AND بوابة منطقية غير عكسية ولا تصلح كمياً.", en: "AND is a non-reversible classical gate, unusable in quantum circuits." } },
    { q: { ar: "خوارزمية Shor الكميّة تُستخدم في:", en: "Shor's quantum algorithm is used for:" },
      o: [{ ar:"تكسير الأعداد المركّبة", en:"Factoring large numbers" }, { ar:"رسم الصور", en:"Drawing images" }, { ar:"تشغيل الألعاب", en:"Running games" }, { ar:"ضغط الملفات", en:"Compressing files" }],
      a: 0, e: { ar: "تكسير الأعداد الكبيرة يهدد تشفير RSA.", en: "Factoring big numbers threatens RSA encryption." } },
    { q: { ar: "لماذا نحتاج حساباً كمياً؟", en:"Why do we need quantum computing?" },
      o: [{ ar:"لأنه أسرع في كل المهام", en:"It is faster at everything" },
          { ar:"لأنه يحلّ بعض المشكلات (البحث، المحاكاة) بشكل عملي تعذّر حله كلاسيكياً", en:"It solves some problems (search, simulation) that are intractable classically" },
          { ar:"لأنه يستهلك طاقة أقل فقط", en:"It only uses less power" },
          { ar:"لأنه لا يحتاج برمجة", en:"It needs no programming" }],
      a: 1, e: { ar: "الحوسبة الكمية ليست بديلاً عاماً للحاسب، بل أداة لفئة معينة من المشكلات.", en:"Quantum is not a general replacement, but a tool for a class of problems." } }
];

/* ---------- المشاريع ---------- */
const PROJECTS = [
    {
        icon: "ic-target",
        title: { ar: "مُولّد أرقام عشوائية كمّي", en: "Quantum Random Number Generator" },
        en: "QRNG",
        desc: { ar: "استخدم تراكب البوابة H وقياسات متكررة لتوليد سلسلة ثنائية عشوائية حقيقية، ثم قارن توزيعها بتوزيع مولّد شجري (Pseudo Random).",
                en: "Use H superposition and repeated shots to produce a real random bit string, then compare it with a pseudo-random (tree) generator." },
        steps: [
            { ar: "ابنِ دائرة: H ثم Measure على كيوبت واحد.", en: "Build: H then Measure on one qubit." },
            { ar: "شغّل 100 قياس وانسخ النتائج 0/1 كسلسلة.", en: "Run 100 shots and copy the 0/1 results as a string." },
            { ar: "احسب نسبة الـ 0 وقارنها بالقيمة 0.5.", en: "Compute the ratio of zeros and compare with 0.5." },
            { ar: "اجعل الدائرة 8 كيوبتات لتوليد بايت كامل عشوائي.", en: "Expand to 8 qubits to generate a full random byte." },
            { ar: "اكتب تقريراً: لماذا تكون النتيجة كمّية أكثر عشوائية؟", en: "Write a report: why is the quantum result more random?" }
        ],
        level: { ar: "مبتدئ", en: "Beginner" }, time: { ar: "20 دقيقة", en: "20 min" },
        cols: [["H"], ["Measure"]]
    },
    {
        icon: "ic-puzzle",
        title: { ar: "محاكاة عمل Bell State", en: "Simulating a Bell State" },
        en: "BELL",
        desc: { ar: "ابنِ زوجاً متشابكاً واقرأ نتائج القياس ثم عدّل الدائرة لاختبار حدود التشابك.",
                en: "Build an entangled pair, read the measurement results, then modify the circuit to test the limits of entanglement." },
        steps: [
            { ar: "H على q0 ثم CNOT من q0 إلى q1.", en: "H on q0 then CNOT from q0 to q1." },
            { ar: "سجّل 20 نتيجة للقياس: كم مرة تطابق السلكان؟", en: "Record 20 shots: how often do the wires agree?" },
            { ar: "أضف X على q1 قبل القياس وفسّر النتيجة.", en: "Add X to q1 before measuring and explain." },
            { ar: "قارن الحالتين |Φ+⟩ و |Φ−⟩ بإضافة Z.", en: "Compare |Φ+⟩ and |Φ−⟩ by adding Z." },
            { ar: "اشرح كيف يُستخدم التشابك في Teleportation.", en: "Explain how entanglement enables teleportation." }
        ],
        level: { ar: "متوسط", en: "Intermediate" }, time: { ar: "30 دقيقة", en: "30 min" },
        cols: [["H"], ["•", "X"], ["Measure", "Measure"]]
    },
    {
        icon: "ic-flask",
        title: { ar: "تجربة القياس الكمّي", en: "Quantum Measurement Experiment" },
        en: "MEASUREMENT",
        desc: { ar: "دراسة إحصائية للقياس: مقارنة نسب القياس الفعلية بالاحتمالات النظرية لعدة حالات.",
                en: "A statistical study of measurement: compare measured frequencies with theoretical probabilities for several states." },
        steps: [
            { ar: "جهّز جدولاً بأعمدة: الدائرة، القياسات، النسبة النظرية.", en: "Prepare a table: circuit, shots, theoretical ratio." },
            { ar: "جرّب |0⟩ فقط ثم H ثم H ثم Z.", en: "Try |0⟩ only, then H, then H+H, then H+Z." },
            { ar: "كل حالة: 100 قياس واحسب النسبة.", en: "For each: 100 shots and compute the ratio." },
            { ar: "ارسم مخططاً (Bar Chart) للنتائج.", en: "Draw a bar chart of the results." },
            { ar: "استنتج أثر الطور Z على القياس.", en: "Conclude how the Z phase affects measurement." }
        ],
        level: { ar: "متوسط", en: "Intermediate" }, time: { ar: "40 دقيقة", en: "40 min" },
        cols: [["H"], ["Measure"]]
    },
    {
        icon: "ic-grid",
        title: { ar: "مقارنة الحوسبة التقليدية والكمّية", en: "Classical vs Quantum Computing" },
        en: "COMPARE",
        desc: { ar: "مشروع بحثي قصير يشرح الفروق الجوهرية مع تجارب عملية مصوّرة من Quirk.",
                en: "A short research project explaining the core differences, illustrated with practical Quirk screenshots." },
        steps: [
            { ar: "جدول مقارنة: بت/كيوبت، تسلسلي/متزامن، تخزين.", en: "Comparison table: bit/qubit, sequential/parallel, storage." },
            { ar: "اشرح مبدأ التداخل مع تجربة H–H المصوّرة.", en: "Explain interference using the H–H experiment screenshot." },
            { ar: "اذكر تطبيقات: Grover، محاكاة الجزيئات، التشفير.", en: "List applications: Grover, molecular simulation, cryptography." },
            { ar: "ناقش التحديات: Decoherence، الأخطاء، الحرارة.", en: "Discuss challenges: decoherence, errors, cooling." },
            { ar: "قدّم عرضاً 3 دقائق أمام الصف.", en: "Present a 3-minute talk to the class." }
        ],
        level: { ar: "مبتدئ", en: "Beginner" }, time: { ar: "45 دقيقة", en: "45 min" },
        cols: [["X"], ["H"], ["Measure"]]
    }
];

/* ---------- بيانات قسم المعلم ---------- */
const WORKSHEETS = [
    { id:"w1", title:{ ar:"ورقة عمل 1: المفاهيم الأساسية", en:"Worksheet 1: Core Concepts" },
      sub:{ ar:"مفاضلة بت/كيوبت + تراكب + تشابك", en:"Bit/qubit + superposition + entanglement" },
      body: [
        { t:"h", ar:"أولاً: عرّف المصطلحات", en:"Part A: Define the terms" },
        { t:"lines", n:4 },
        { t:"q", ar:"1) اكتب معادلة الحالة الكمّية لكيوبت واحد وفسّر معناها.", en:"1) Write the state equation of one qubit and explain it." },
        { t:"q", ar:"2) ما الفرق بين البت والكيوبت؟ مثالان.", en:"2) Difference between bit and qubit? Two examples." },
        { t:"q", ar:"3) اشرح التراكب بلغتك مع رسم توضيحي.", en:"3) Explain superposition in your own words with a drawing." },
        { t:"h", ar:"ثانياً: تطبيق عملي على Quirk", en:"Part B: Practical work in Quirk" },
        { t:"q", ar:"4) ابنِ دائرة H ثم Measure وسجّل 20 قياساً.", en:"4) Build H then Measure and record 20 shots." },
        { t:"q", ar:"5) ما نسبة الـ 0 التي حصلت؟ قارنها بالنظرية.", en:"5) What ratio of 0 did you get? Compare with theory." },
        { t:"q", ar:"6) ابنِ حالة بيل وسجّل 10 نتائج للسكين معاً.", en:"6) Build a Bell state and record 10 two-wire results." },
        { t:"lines", n:3 }
      ] },
    { id:"w2", title:{ ar:"ورقة عمل 2: البوابات الكمية", en:"Worksheet 2: Quantum Gates" },
      sub:{ ar:"X، Y، Z، H، S، T، CNOT، SWAP", en:"X, Y, Z, H, S, T, CNOT, SWAP" },
      body: [
        { t:"h", ar:"أولاً: أكمل الجدول", en:"Part A: Complete the table" },
        { t:"q", ar:"1) اكتب مصفوفة كل من X و Z و H.", en:"1) Write the matrices of X, Z and H." },
        { t:"q", ar:"2) ما ناتج H|0⟩؟ وما ناتج X|1⟩؟", en:"2) What is H|0⟩? And X|1⟩?" },
        { t:"q", ar:"3) ارسم دائرة بيل بمسميات البوابات.", en:"3) Draw a Bell circuit labelling the gates." },
        { t:"h", ar:"ثانياً: صواب أم خطأ", en:"Part B: True or False" },
        { t:"q", ar:"4) بوابة Z تُغيّر قيمة الكيوبت من 0 إلى 1.", en:"4) Z changes the qubit value from 0 to 1." },
        { t:"q", ar:"5) بوابة H وحدها تُنتج تراكباً 50/50.", en:"5) H alone creates a 50/50 superposition." },
        { t:"q", ar:"6) CNOT تعمل على كيوبت واحد فقط.", en:"6) CNOT works on a single qubit only." },
        { t:"h", ar:"ثالثاً: تجربة", en:"Part C: Experiment" },
        { t:"q", ar:"7) سجّل أثر إضافة Z بعد H على نتائج القياس.", en:"7) Record the effect of adding Z after H on measurements." },
        { t:"lines", n:4 }
      ] },
    { id:"w3", title:{ ar:"ورقة عمل 3: مختبر Quirk خطوة بخطوة", en:"Worksheet 3: Quirk Lab Step by Step" },
      sub:{ ar:"تعلّم بالممارسة + لقطات شاشة", en:"Learning by doing + screenshots" },
      body: [
        { t:"h", ar:"المهمة 1: التراكب", en:"Task 1: Superposition" },
        { t:"q", ar:"1) افتح Quirk وضِع H ثم Measure. ماذا ترى في اللوحة؟", en:"1) Open Quirk, place H then Measure. What do you see?" },
        { t:"lines", n:2 },
        { t:"h", ar:"المهمة 2: التشابك", en:"Task 2: Entanglement" },
        { t:"q", ar:"2) ابنِ H + CNOT وصوّر لوحة القياس.", en:"2) Build H + CNOT and screenshot the display." },
        { t:"q", ar:"3) احذف H: هل يبقى التشابك؟ اشرح.", en:"3) Remove H: does entanglement remain? Explain." },
        { t:"lines", n:2 },
        { t:"h", ar:"المهمة 3: التداخل", en:"Task 3: Interference" },
        { t:"q", ar:"4) ضع H مرتين. لاحظ النتيجة وفسّرها.", en:"4) Place H twice. Observe and explain the result." },
        { t:"lines", n:3 }
      ] }
];

const ASSESSMENT = [
    { ar:"عرّف الكيوبت وقارنه بالبت في ثلاثة أسطر.", en:"Define the qubit and compare it with the bit in three lines." },
    { ar:"اكتب معادلة الحالة الكمّية وحدّد المعاملات.", en:"Write the quantum state equation and identify the amplitudes." },
    { ar:"ماذا يحدث للكيوبت عند القياس؟ ولماذا؟", en:"What happens to a qubit when measured? Why?" },
    { ar:"اذكر خطوتين لبناء حالة بيل مع رسم الدائرة.", en:"Give two steps to build a Bell state with the circuit drawn." },
    { ar:"اشرح فرق الطور الذي تُحدثه بوابة Z.", en:"Explain the phase change produced by the Z gate." },
    { ar:"لماذا يُسمّى قياس الكيوبت «انهياراً»؟", en:"Why is qubit measurement called 'collapse'?" },
    { ar:"كم حالة يمثّل 4 كيوبتات؟ وضّح الحساب.", en:"How many states do 4 qubits represent? Show the calculation." },
    { ar:"اذكر تطبيقين للحوسبة الكمّية مع تفسير موجز.", en:"Two quantum computing applications with a brief explanation." },
    { ar:"ما التحديات الهندسية أمام بناء حواسيب كمّية؟", en:"What engineering challenges stand in the way of quantum computers?" },
    { ar:"صوّر من Quirk دائرة H ثم CNOT واكتب نتائج 10 قياسات.", en:"Screenshot an H + CNOT circuit from Quirk and list 10 measurement results." }
];

const CLASS_ACTIVITIES = [
    { ar:"نشاط جماعي «صُنّاع الحالات»: فرقتان، كل فريق يبني حالة بيل خلال دقيقتين والفريق الآخر يتحقق بالقياس.",
      en:"Group activity 'State Builders': two teams; each builds a Bell state in two minutes while the other verifies by measurement." },
    { ar:"تحدي التنبؤ: يعرض المعلم دائرة ويكتب الطالب توقّعه للنتيجة قبل التشغيل (تغذية راجعة فورية).",
      en:"Prediction challenge: the teacher shows a circuit and students write their predicted result before running it (instant feedback)." },
    { ar:"سباق التصحيح: يُعطى طالب دائرة بها خطأ منطقي (مثل H بعد Measure) ويكتشفها خلال 60 ثانية.",
      en:"Repair race: a student receives a faulty circuit (e.g. H after Measure) and must find the bug in 60 seconds." },
    { ar:"محاضرة مصغّرة (3 دقائق) لكل طالب عن أحد المفاهيم باستخدام بطاقة من الموقع.",
      en:"A 3-minute mini-talk by each student about one concept using a card from the site." },
    { ar:"ورشة «صمّم تجربة»: كل طالب يخترع تجربة جديدة في Quirk ويكتب هدفها وملاحظاتها.",
      en:"'Design an experiment' workshop: each student invents a new Quirk experiment with goal and observations." }
];

/* ---------- المساعد التعليمي: قاعدة المعرفة ---------- */
const AI_KB = [
    { k:["كيوبت","qubit","كيوبتات","quantum bit","الكيوبت"],
      a:{ ar:"الكيوبت هو وحدة الحوسبة الكمية: يُكتب |ψ⟩ = α|0⟩ + β|1⟩، أي أنه يحمل تراكباً بين الصفر والواحد حتى لحظة القياس، واحتمال كل نتيجة = مربع المقدار للمعامل (|α|² و |β|²).\nجرّب: ضع بوابة H على كيوبت وقِس مراراً في Quirk.",
          en:"A qubit is written |ψ⟩ = α|0⟩ + β|1⟩: it holds a superposition of 0 and 1 until measured, and each outcome's probability is the squared magnitude of its amplitude (|α|², |β|²).\nTry: put an H gate on a qubit and measure repeatedly in Quirk." },
      exp:{ name:{ar:"تجربة: تراكب مع H", en:"Experiment: H superposition"}, cols:[["H"],["Measure"]] } },

    { k:["تراكب","superposition","التراكب","هادامارد","hadamard","H gate","بوابة h"],
      a:{ ar:"التراكب يعني أن الكيوبت يمثل عدة قيم في آنٍ واحد بمعاملات فيزيائية. بوابة H هي الأشهر لإنشائه:\nH|0⟩ = (|0⟩+|1⟩)/√2 = |+⟩\nولهذا يخرج من القياس 0 أو 1 باحتمال 50% لكل منهما. التراكب يُلغى فور القياس (انهيار).",
          en:"Superposition means a qubit represents several values at once through amplitudes. H creates it:\nH|0⟩ = (|0⟩+|1⟩)/√2 = |+⟩\nSo measurement gives 0 or 1 with 50% each. Measurement destroys it (collapse)." },
      exp:{ name:{ar:"تجربة: قياس عشوائي 50/50", en:"Experiment: 50/50 measurement"}, cols:[["H"],["Measure"]] } },

    { k:["تشابك","entanglement","متشابك","بيل","bell","حالة بيل"],
      a:{ ar:"التشابك حالة كميّة مشتركة لا تُحلَّل. حالة بيل = (|00⟩+|11⟩)/√2 وتُبنى بـ H ثم CNOT. عند قياس الكيوبت الأول تظهر 0 أو 1، ويظهر الثاني القيمة نفسها فوراً، ولا تظهر 01 أو 10 أبداً.",
          en:"Entanglement is a shared state that cannot be split. Bell state = (|00⟩+|11⟩)/√2 built with H then CNOT. Measuring the first gives 0 or 1 and the second always matches — 01/10 never appear." },
      exp:{ name:{ar:"تجربة: حالة بيل", en:"Experiment: Bell state"}, cols:[["H"],["•","X"],["Measure","Measure"]] } },

    { k:["قياس","measurement","انهيار","collapse","احتمالية","احتمال"],
      a:{ ar:"القياس يحوّل الاحتمالات إلى نتيجة مؤكدة: P(0)=|α|²، P(1)=|β|². العملية غير عكسية وتُدمر التراكب. لو كرّرت القياس 100 مرة على دائرة H ستحصل على ما يقارب 50 و50 — الفردي عشوائي والإحصاء منتظم.",
          en:"Measurement turns probabilities into a definite result: P(0)=|α|², P(1)=|β|². It is irreversible and destroys superposition. Repeat it 100 times on an H circuit and you get about 50/50 — random per shot, regular in aggregate." },
      exp:{ name:{ar:"تجربة: 100 قياس", en:"Experiment: 100 shots"}, cols:[["H"],["Measure"]] } },

    { k:["cnot","التحكم","not الكممي","control","cx"],
      a:{ ar:"CNOT بوابة على كيوبتين: التحكم (•) والهدف (X). إذا كان التحكم = 1 تنقلب الحالة الهدف (يعمل X)، وإذا كان 0 فلا شيء. هي أداة بناء التشابك الأساسية في كل الدوائر.",
          en:"CNOT acts on two qubits: control (•) and target (X). If the control is 1 the target flips (X), otherwise nothing. It is the main entanglement-building tool." },
      exp:{ name:{ar:"تجربة: CNOT", en:"Experiment: CNOT"}, cols:[["H"],["•","X"],["Measure","Measure"]] } },

    { k:["بوابة x","x gate","نف","not","قلب"],
      a:{ ar:"بوابة X = نفّي NOT الكممي: |0⟩ ← |1⟩ و|1⟩ ← |0⟩. رياضياً مصفوفة [[0,1],[1,0]]، وهي دوران 180° حول محور X.",
          en:"Gate X is the quantum NOT: |0⟩ → |1⟩ and |1⟩ → |0⟩. Its matrix is [[0,1],[1,0]], a 180° rotation about X." },
      exp:{ name:{ar:"تجربة: بوابة X", en:"Experiment: X gate"}, cols:[["X"],["Measure"]] } },

    { k:["بوابة z","z gate","طور","phase"],
      a:{ ar:"بوابة Z لا تغيّر القيمة بل الإشارة: |1⟩ ← −|1⟩ و|0⟩ كما هي. تُعرف بوابة الطور، وهي أساسية لفهم التداخل الكمي. احتمالات القياس لا تتغيّر بينما يتغيّر الطور.",
          en:"Gate Z changes the sign, not the value: |1⟩ → −|1⟩ while |0⟩ stays. It is a phase gate, crucial for interference. Measurement probabilities stay the same; only the phase changes." },
      exp:{ name:{ar:"تجربة: Z بعد H", en:"Experiment: Z after H"}, cols:[["H"],["Z"],["Measure"]] } },

    { k:["swap","تبديل"],
      a:{ ar:"SWAP تبديل حقيقي بين كيوبتين: |a,b⟩ ← |b,a⟩. في الدوائر الفيزيائية تُبنى من ثلاث CNOT. استخدمها لنقل «القفزة» من سلك إلى آخر دون نسخ.",
          en:"SWAP truly exchanges two qubits: |a,b⟩ → |b,a⟩. Hardware builds it from three CNOTs. Use it to move a flip between wires without copying." },
      exp:{ name:{ar:"تجربة: SWAP", en:"Experiment: SWAP"}, cols:[["X",1],["Swap","Swap"],["Measure","Measure"]] } },

    { k:["quirk","quirk كيف","المحاكي","محاكاة","كيف ابدأ","طريقة الاستخدام"],
      a:{ ar:"طريقة الاستخدام في Quirk:\n1) اسحب البوابة من الشريط العلوي إلى السلك.\n2) أضف Measure لرؤية الاحتمالات.\n3) اللوحة السفلية تعرض النسب وكرات بلوك لحظياً.\n4) زر Shoot يعيد العيّنة لرؤية الإحصاء.\nمن داخل موقعنا: افتح «مختبر Quirk» واختر تجربة جاهزة فتُحمَّل تلقائياً.",
          en:"How to use Quirk:\n1) Drag a gate from the top toolbox onto a wire.\n2) Add Measure to see probabilities.\n3) The bottom display shows ratios and Bloch spheres live.\n4) Shoot re-runs samples for statistics.\nOn this site: open 'Quirk Lab' and pick an experiment — it loads automatically." },
      exp:{ name:{ar:"ابدأ بتجربة بيل", en:"Start with Bell"}, cols:[["H"],["•","X"],["Measure","Measure"]] } },

    { k:["فرق","الفرق بين","comparing","البت والكيوبت","classic","تقليدي"],
      a:{ ar:"الفرق الجوهري: البت قيمة واحدة ثابتة (0 أو 1)، الكيوبت يحمل تراكباً بأطوار. n بت ← حالة واحدة، n كيوبت ← 2ⁿ حالة. لكن الكيوبت لا يُنسخ ويتأثر بالتشويش، فالكمية ليست «أسرع في كل شيء» بل في فئات معينة من المشكلات.",
          en:"Core difference: a bit is one fixed value (0 or 1); a qubit carries superposition with phases. n bits → one state, n qubits → 2ⁿ states. But qubits cannot be copied and are fragile — quantum is faster only for certain problem classes." },
      exp:{ null: true } },

    { k:["تطبيقات","استخدامات","شروع","shor","grover","تشفير","محاكاة الجزيئات","ai","ذكاء"],
      a:{ ar:"أبرز التطبيقات: كسر الأعداد المركّبة (خوارزمية Shor وتهدّد RSA)، البحث (Grover يسرّع البحث غير المرتّب)، محاكاة الجزيئات والأدوية، التحسين والتعلّم الآلي، والاتصالات الآمنة QKD.",
          en:"Top applications: factoring (Shor, threatening RSA), search (Grover for unsorted databases), molecular/drug simulation, optimization and machine learning, plus secure quantum key distribution." },
      exp:{ null: true } },

    { k:["مشاريع","مشروع","نشاط","اريد اعمل","أريد أن أفعل"],
      a:{ ar:"مشاريع جاهزة لك: مولّد أرقام عشوائية كمّي، محاكاة Bell State، تجربة القياس الكمّي، ومقارنة الحوسبة التقليدية والكمّية — كلها في قسم «المشاريع» مع خطوات التنفيذ وزر تشغيل في Quirk.",
          en:"Ready projects: quantum random number generator, Bell state simulation, quantum measurement experiment, and classical vs quantum comparison — all in the Projects section with steps and a Quirk run button." },
      exp:{ null: true } },

    { k:["لا افهم","صعب","مستحيل","مبتدئ","كيف ابدأ","ابدا"],
      a:{ ar:"ابدأ بهذه السلسلة (15 دقيقة):\n1) افتح «ما هو الكيوبت» في قسم المفاهيم.\n2) شغّل النشاط 1 (توقع نتيجة H).\n3) افتح تجربة التراكب في المختبر.\n4) أجب عن أول 5 أسئلة في الاختبار.\nبالتوفيق!",
          en:"Start with this 15-minute path:\n1) Open 'What is a qubit' in Concepts.\n2) Run Activity 1 (predict H).\n3) Load the superposition experiment in the Lab.\n4) Answer the first 5 quiz questions.\nGood luck!" },
      exp:{ null: true } },

    { k:["من اين اجد","اوراق عمل","المعلم","تقويم","ورقة"],
      a:{ ar:"قسم «للمعلم» يحتوي أهداف الدرس، 3 أوراق عمل قابلة للطباعة، 10 أسئلة تقويم، وأنشطة صفية جاهزة. يمكنك طباعة أي ورقة مباشرة بالزر المخصص.",
          en:"The Teacher Zone has lesson objectives, 3 printable worksheets, 10 assessment questions and ready classroom activities — each printable with its own button." },
      exp:{ null: true } }
];

/* مجموعات الاقتراحات في المساعد */
const AI_SUGGESTIONS = [
    { ar:"ما هو الكيوبت؟", en:"What is a qubit?" },
    { ar:"اشرح التراكب", en:"Explain superposition" },
    { ar:"ما حالة Bell؟", en:"What is a Bell state?" },
    { ar:"كيف أستخدم Quirk؟", en:"How do I use Quirk?" },
    { ar:"الفرق بين البت والكيوبت", en:"Bit vs qubit" },
    { ar:"اقترح تجربة", en:"Suggest an experiment" }
];
