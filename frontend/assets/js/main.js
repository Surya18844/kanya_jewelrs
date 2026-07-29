/* ==========================================================
   Kanya Jewelers — Shared Frontend Logic
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  initNavbar();
  injectContactShortcuts();
  initScrollAnimations();
});

/* ---------------- Navbar ---------------- */
function initNavbar() {
  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", () => links.classList.toggle("open"));
    links.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => links.classList.remove("open"))
    );
  }

  // Highlight current page
  const current = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav-links a").forEach((a) => {
    if (a.getAttribute("href") === current) a.classList.add("active");
  });
}

/* ---------------- WhatsApp / Call shortcuts ---------------- */
function injectContactShortcuts() {
  document.querySelectorAll("[data-whatsapp]").forEach((el) => {
    el.href = whatsappLink(el.dataset.whatsapp !== "1" ? el.dataset.whatsapp : undefined);
    el.target = "_blank";
    el.rel = "noopener";
  });
  document.querySelectorAll("[data-call]").forEach((el) => {
    el.href = `tel:${CONFIG.SHOP_PHONE_TEL}`;
  });
  document.querySelectorAll("[data-shop-phone]").forEach((el) => (el.textContent = CONFIG.SHOP_PHONE_DISPLAY));
  document.querySelectorAll("[data-shop-email]").forEach((el) => {
    el.textContent = CONFIG.SHOP_EMAIL;
    if (el.tagName === "A") el.href = `mailto:${CONFIG.SHOP_EMAIL}`;
  });
  document.querySelectorAll("[data-shop-address]").forEach((el) => (el.textContent = CONFIG.SHOP_ADDRESS));
  document.querySelectorAll("[data-shop-hours]").forEach((el) => (el.textContent = CONFIG.SHOP_HOURS));

  const floatBtn = document.querySelector(".float-whatsapp");
  if (floatBtn) {
    floatBtn.href = whatsappLink();
    floatBtn.target = "_blank";
    floatBtn.rel = "noopener";
  }

  const mapFrame = document.querySelector("#shopMap");
  if (mapFrame) mapFrame.src = CONFIG.MAP_EMBED_SRC;

  document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
}

/* ---------------- Simple scroll-reveal animation ---------------- */
function initScrollAnimations() {
  const items = document.querySelectorAll(".reveal");
  if (!items.length || !("IntersectionObserver" in window)) return;
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );
  items.forEach((el) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(24px)";
    el.style.transition = "all 0.7s ease";
    observer.observe(el);
  });
}

/* ---------------- API helper ---------------- */
async function apiRequest(path, options = {}) {
  const res = await fetch(`${CONFIG.API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  let data = null;
  try {
    data = await res.json();
  } catch (e) {
    /* no body */
  }
  if (!res.ok) {
    const message = (data && (data.detail || data.message)) || "Something went wrong. Please try again.";
    throw new Error(typeof message === "string" ? message : "Something went wrong. Please try again.");
  }
  return data;
}

/* ---------------- Product card renderer ---------------- */
function productCardHTML(product) {
  const img = product.image_url || "assets/images/placeholder.jpg";
  const category = product.category ? product.category.name : "Jewellery";
  const desc = product.description || "Exquisite handcrafted piece from our premium collection.";
  return `
    <div class="card reveal">
      <div class="card-img-wrap">
        <span class="card-category">${escapeHTML(category)}</span>
        <img src="${escapeHTML(img)}" alt="${escapeHTML(product.name)}" loading="lazy" />
      </div>
      <div class="card-body">
        <h3>${escapeHTML(product.name)}</h3>
        <p>${escapeHTML(desc)}</p>
      </div>
    </div>`;
}

function escapeHTML(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function formatCurrency(value) {
  const num = Number(value);
  if (Number.isNaN(num)) return "--";
  return "₹" + num.toLocaleString("en-IN", { maximumFractionDigits: 2 });
}

function formatDateTime(isoString) {
  try {
    const d = new Date(isoString);
    return d.toLocaleString("en-IN", {
      day: "2-digit", month: "short", year: "numeric",
      hour: "2-digit", minute: "2-digit",
    });
  } catch (e) {
    return isoString;
  }
}
