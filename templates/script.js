const API_BASE = "http://localhost:8000/api/v1";


// Global holat
let current = 0;
let total = 0;
let slides = [];
let selectedSprintId = null;
let selectedProductId = null;
let allProducts = [];

const wrapper = document.getElementById('slides-wrapper');
const progress = document.getElementById('progress');
const counter = document.getElementById('counter');
const homeBtn = document.getElementById('homeBtn');
const loader = document.getElementById('loader');
const sprintSelect = document.getElementById('sprintSelect');
const filterContainer = document.querySelector('.filter-container');


async function initApp() {
    try {
        showLoader(true);
        // Sprintlar va Mahsulotlarni parallel yuklash
        const [sprintsRes, prodRes] = await Promise.all([
            fetch(`${API_BASE}/sprints/`, {headers: {'Accept-Language': currentLang}}),
            fetch(`${API_BASE}/products/`, {headers: {'Accept-Language': currentLang}})
        ]);
        const sprints = await sprintsRes.json();
        allProducts = await prodRes.json();

        if (sprints.length > 0) {
            sprintSelect.innerHTML = sprints.map(s =>
                `<option value="${s.id}">${s.name}</option>`
            ).join('');
            selectedSprintId = sprintSelect.value;
        }

        // Bosh sahifani chizish (async funksiya bo'lgani uchun await bilan)
        await renderStartPage(allProducts);
        showLoader(false);
    } catch (err) {
        console.error("Xatolik:", err);
        showLoader(false);
    }
}

async function renderStartPage(products) {
    selectedProductId = null;
    if (filterContainer) filterContainer.style.display = 'block';

    const sprintId = sprintSelect.value;
    const sprintText = sprintSelect.options[sprintSelect.selectedIndex]?.text || "";

    showLoader(true);

    // HAR BIR MAHSULOT UCHUN ALOHIDA COUNTNI ANIQLASH
    // Bu qism har bir product uchun /features/?product=ID&sprint=ID so'rovini yuboradi
    const productsWithCount = await Promise.all(products.map(async (p) => {
        try {
            const res = await fetch(`${API_BASE}/features/?product=${p.id}&sprint=${sprintId}`, {
                headers: {'Accept-Language': currentLang}
            });
            const features = await res.json();
            return {...p, current_count: features.length};
        } catch {
            return {...p, current_count: 0};
        }
    }));

    let html = `
        <div class="slide active title-slide">
            <div class="sprint-badge">SD Platform</div>
            <h1>Loyihani tanlang</h1>
            <div class="subtitle">Sprint: ${sprintText}</div>
            <div class="app-cards-row">
                ${productsWithCount.map(p => `
                    <div class="app-card" onclick="loadFeatures(${p.id})">
                        <img src="${p.image}" alt="${p.title}">
                        <div class="app-card-info">
                            <h3>${p.title}</h3>
                            <div class="count">${p.current_count} ta yangilik →</div>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;

    wrapper.innerHTML = html;
    resetNavigation();
    showLoader(false);
}

async function loadFeatures(productId) {
    selectedProductId = productId;
    const sprintId = sprintSelect.value;

    try {
        showLoader(true);
        const res = await fetch(`${API_BASE}/features/?product=${productId}&sprint=${sprintId}`, {
            headers: {'Accept-Language': currentLang}
        });
        const features = await res.json();

        if (filterContainer) filterContainer.style.display = 'none';

        if (features.length === 0) {
            renderEmptyState();
        } else {
            renderFeatureSlides(features);
        }
        showLoader(false);
    } catch (err) {
        console.error("Xatolik:", err);
        showLoader(false);
    }
}

function renderEmptyState() {
    wrapper.innerHTML = `
        <div class="slide active title-slide">
            <div class="sprint-badge" style="color: #ff4d4d; border-color: #ff4d4d;">Natija yo'q</div>
            <h1>Yangiliklar mavjud emas</h1>
            <p class="subtitle">Ushbu mahsulot bo'yicha tanlangan sprintda hech qanday ma'lumot topilmadi.</p>
            <button class="nav-btn" style="width: auto; padding: 0 25px; margin-top: 30px;" onclick="goBackHome()">← Orqaga qaytish</button>
        </div>
    `;
    resetNavigation();
}

function renderFeatureSlides(features) {
    let html = "";

    features.forEach((feat, index) => {
        const fileCount = feat.features_files?.length || 0;
        // Rasmlar ko'p bo'lsa chapga tiraladi, kam bo'lsa o'rtada turadi
        const galleryClass = fileCount > 2 ? 'justify-start' : 'justify-center';

        const imagesHtml = fileCount > 0
            ? feat.features_files.map(file => `
                <div class="screenshot-item">
                    <img src="${file.image}" class="zoomable" alt="Screenshot">
                </div>
              `).join('')
            : '<div class="screenshot-placeholder">Rasm yuklanmagan</div>';

        html += `
            <div class="slide">
                <div class="feature-header">
                    <div class="feature-number web">${index + 1}</div>
                    <div class="feature-title">${feat.title}</div>
                </div>
                <div class="feature-body">
                    <div class="feature-gallery ${galleryClass}">
                        ${imagesHtml}
                    </div>
                </div>
                <div class="feature-description">
                    ${feat.description}
                </div>
            </div>
        `;
    });

    html += `
        <div class="slide end-slide">
            <h2>E'tiboringiz uchun rahmat!</h2>
            <button class="nav-btn" style="width: auto; padding: 0 25px; margin-top: 20px;" onclick="goBackHome()">Bosh sahifaga qaytish</button>
        </div>
    `;

    wrapper.innerHTML = html;
    resetNavigation();
    if (slides.length > 0) slides[0].classList.add('active');
    updateUI();
}

function goBackHome() {
    if (filterContainer) filterContainer.style.display = 'block';
    renderStartPage(allProducts);
}

function resetNavigation() {
    slides = document.querySelectorAll('.slide');
    total = slides.length;
    current = 0;
    updateUI();
}

function nextSlide() {
    if (current < total - 1) {
        slides[current].classList.remove('active');
        slides[current].classList.add('exit-left');
        current++;
        slides[current].classList.add('active');
        updateUI();
    }
}

function prevSlide() {
    if (current > 0) {
        slides[current].classList.remove('active');
        current--;
        slides[current].classList.remove('exit-left');
        slides[current].classList.add('active');
        updateUI();
    }
}

function updateUI() {
    if (progress) progress.style.width = total > 0 ? ((current + 1) / total * 100) + '%' : '0%';
    if (counter) counter.textContent = total > 0 ? `${current + 1} / ${total}` : '0 / 0';
    if (homeBtn) homeBtn.classList.toggle('visible', selectedProductId !== null);
}

function showLoader(status) {
    if (loader) loader.style.display = status ? 'flex' : 'none';
}

async function exportToPDF() {
    window.print();
}

sprintSelect.addEventListener('change', async () => {
    await renderStartPage(allProducts);
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') {
        e.preventDefault();
        nextSlide();
    }
    if (e.key === 'ArrowLeft') {
        e.preventDefault();
        prevSlide();
    }
});


initApp();