/* ==========================================================
   Kanya Jewelers — Admin Dashboard Logic
   ========================================================== */

let categoriesCache = [];

document.addEventListener("DOMContentLoaded", () => {
  requireAdminAuth();
  initSidebar();
  loadCategories().then(() => {
    loadProducts();
  });
  loadGallery();
  loadRates();
  loadEnquiries();
  bindProductModal();
  bindGalleryUpload();
  bindRateForms();
});

function showToast(message, isError = false) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.className = `toast show${isError ? " error" : ""}`;
  setTimeout(() => toast.classList.remove("show"), 3200);
}

/* ---------------- Sidebar navigation ---------------- */
function initSidebar() {
  document.querySelectorAll(".nav-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".nav-btn").forEach((b) => b.classList.remove("active"));
      document.querySelectorAll(".admin-panel").forEach((p) => p.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById(btn.dataset.panel).classList.add("active");
    });
  });
}

/* ---------------- Categories ---------------- */
async function loadCategories() {
  try {
    categoriesCache = await adminApiRequest("/api/categories");
    const select = document.getElementById("productCategory");
    select.innerHTML = categoriesCache
      .map((c) => `<option value="${c.id}">${escapeHTML(c.name)}</option>`)
      .join("");
  } catch (err) {
    showToast(err.message, true);
  }
}

/* ---------------- Products ---------------- */
async function loadProducts() {
  const tbody = document.getElementById("productsTableBody");
  try {
    const products = await adminApiRequest("/api/products?active_only=false");
    if (!products.length) {
      tbody.innerHTML = `<tr><td colspan="5">No products yet. Click "Add New Product" to get started.</td></tr>`;
      return;
    }
    tbody.innerHTML = products
      .map(
        (p) => `
      <tr>
        <td><img class="thumb" src="${escapeHTML(p.image_url || '../assets/images/placeholder.jpg')}" alt="${escapeHTML(p.name)}" /></td>
        <td>${escapeHTML(p.name)}</td>
        <td>${escapeHTML(p.category ? p.category.name : '—')}</td>
        <td><span class="badge ${p.is_active ? 'badge-gold' : 'badge-off'}">${p.is_active ? 'Active' : 'Hidden'}</span></td>
        <td>
          <button class="icon-btn" title="Edit" onclick='openProductModal(${JSON.stringify(p).replace(/'/g, "&#39;")})'>✏️</button>
          <button class="icon-btn danger" title="Delete" onclick="deleteProduct(${p.id})">🗑️</button>
        </td>
      </tr>`
      )
      .join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="5">Failed to load products: ${escapeHTML(err.message)}</td></tr>`;
  }
}

function bindProductModal() {
  const backdrop = document.getElementById("productModalBackdrop");
  document.getElementById("addProductBtn").addEventListener("click", () => openProductModal());
  document.getElementById("productModalClose").addEventListener("click", () => backdrop.classList.remove("open"));
  backdrop.addEventListener("click", (e) => { if (e.target === backdrop) backdrop.classList.remove("open"); });

  document.getElementById("productImageFile").addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const preview = document.getElementById("productImagePreview");
    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";

    try {
      const formData = new FormData();
      formData.append("file", file);
      const result = await adminApiRequest("/api/upload/image", { method: "POST", body: formData });
      document.getElementById("productImageUrl").value = result.url;
    } catch (err) {
      showToast(`Image upload failed: ${err.message}`, true);
    }
  });

  document.getElementById("productForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const msgEl = document.getElementById("productFormMsg");
    msgEl.className = "form-msg";

    const id = document.getElementById("productId").value;
    const payload = {
      name: document.getElementById("productName").value.trim(),
      category_id: Number(document.getElementById("productCategory").value),
      description: document.getElementById("productDescription").value.trim(),
      image_url: document.getElementById("productImageUrl").value || null,
      is_active: document.getElementById("productActive").checked,
    };

    try {
      if (id) {
        await adminApiRequest(`/api/products/${id}`, { method: "PUT", body: JSON.stringify(payload) });
        showToast("Product updated successfully.");
      } else {
        await adminApiRequest("/api/products", { method: "POST", body: JSON.stringify(payload) });
        showToast("Product added successfully.");
      }
      document.getElementById("productModalBackdrop").classList.remove("open");
      loadProducts();
    } catch (err) {
      msgEl.classList.add("error");
      msgEl.textContent = err.message;
    }
  });
}

function openProductModal(product) {
  const backdrop = document.getElementById("productModalBackdrop");
  const title = document.getElementById("productModalTitle");
  const preview = document.getElementById("productImagePreview");
  document.getElementById("productFormMsg").textContent = "";
  document.getElementById("productFormMsg").className = "form-msg";

  if (product) {
    title.textContent = "Edit Product";
    document.getElementById("productId").value = product.id;
    document.getElementById("productName").value = product.name;
    document.getElementById("productCategory").value = product.category ? product.category.id : "";
    document.getElementById("productDescription").value = product.description || "";
    document.getElementById("productImageUrl").value = product.image_url || "";
    document.getElementById("productActive").checked = product.is_active;
    if (product.image_url) {
      preview.src = product.image_url;
      preview.style.display = "block";
    } else {
      preview.style.display = "none";
    }
  } else {
    title.textContent = "Add New Product";
    document.getElementById("productForm").reset();
    document.getElementById("productId").value = "";
    document.getElementById("productImageUrl").value = "";
    preview.style.display = "none";
  }
  backdrop.classList.add("open");
}

async function deleteProduct(id) {
  if (!confirm("Delete this product? This cannot be undone.")) return;
  try {
    await adminApiRequest(`/api/products/${id}`, { method: "DELETE" });
    showToast("Product deleted.");
    loadProducts();
  } catch (err) {
    showToast(err.message, true);
  }
}

/* ---------------- Gallery ---------------- */
async function loadGallery() {
  const grid = document.getElementById("galleryAdminGrid");
  try {
    const images = await adminApiRequest("/api/gallery");
    if (!images.length) {
      grid.innerHTML = "No gallery images yet.";
      return;
    }
    grid.innerHTML = images
      .map(
        (img) => `
      <div class="gallery-admin-item">
        <img src="${escapeHTML(img.image_url)}" alt="${escapeHTML(img.caption || '')}" />
        <button class="del-overlay" title="Delete" onclick="deleteGalleryImage(${img.id})">✕</button>
      </div>`
      )
      .join("");
  } catch (err) {
    grid.innerHTML = `Failed to load gallery: ${escapeHTML(err.message)}`;
  }
}

function bindGalleryUpload() {
  document.getElementById("galleryUploadInput").addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      const formData = new FormData();
      formData.append("file", file);
      const uploadResult = await adminApiRequest("/api/upload/image", { method: "POST", body: formData });
      const params = new URLSearchParams({ image_url: uploadResult.url, caption: "" });
      await adminApiRequest(`/api/gallery?${params.toString()}`, { method: "POST" });
      showToast("Image added to gallery.");
      loadGallery();
    } catch (err) {
      showToast(err.message, true);
    } finally {
      e.target.value = "";
    }
  });
}

async function deleteGalleryImage(id) {
  if (!confirm("Delete this gallery image?")) return;
  try {
    await adminApiRequest(`/api/gallery/${id}`, { method: "DELETE" });
    showToast("Image deleted.");
    loadGallery();
  } catch (err) {
    showToast(err.message, true);
  }
}

/* ---------------- Rates ---------------- */
async function loadRates() {
  try {
    const [gold, silver] = await Promise.all([
      adminApiRequest("/api/rates/gold"),
      adminApiRequest("/api/rates/silver"),
    ]);
    document.getElementById("gold22Input").value = gold.rate_per_gram_22k;
    document.getElementById("gold24Input").value = gold.rate_per_gram_24k;
    document.getElementById("silverGramInput").value = silver.rate_per_gram;
    document.getElementById("silverKgInput").value = silver.rate_per_kg;
  } catch (err) {
    showToast(err.message, true);
  }
}

function bindRateForms() {
  document.getElementById("goldRateForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      await adminApiRequest("/api/rates/gold", {
        method: "PUT",
        body: JSON.stringify({
          rate_per_gram_22k: Number(document.getElementById("gold22Input").value),
          rate_per_gram_24k: Number(document.getElementById("gold24Input").value),
        }),
      });
      showToast("Gold rate updated instantly.");
    } catch (err) {
      showToast(err.message, true);
    }
  });

  document.getElementById("silverRateForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      await adminApiRequest("/api/rates/silver", {
        method: "PUT",
        body: JSON.stringify({
          rate_per_gram: Number(document.getElementById("silverGramInput").value),
          rate_per_kg: Number(document.getElementById("silverKgInput").value),
        }),
      });
      showToast("Silver rate updated instantly.");
    } catch (err) {
      showToast(err.message, true);
    }
  });
}

/* ---------------- Enquiries ---------------- */
async function loadEnquiries() {
  const tbody = document.getElementById("enquiriesTableBody");
  try {
    const messages = await adminApiRequest("/api/contact");
    if (!messages.length) {
      tbody.innerHTML = `<tr><td colspan="6">No enquiries yet.</td></tr>`;
      return;
    }
    tbody.innerHTML = messages
      .map(
        (m) => `
      <tr>
        <td>${escapeHTML(m.name)}</td>
        <td>${escapeHTML(m.phone)}</td>
        <td>${escapeHTML(m.email || '—')}</td>
        <td style="max-width:260px;">${escapeHTML(m.message)}</td>
        <td>${formatDateTimeAdmin(m.created_at)}</td>
        <td><button class="icon-btn danger" title="Delete" onclick="deleteEnquiry(${m.id})">🗑️</button></td>
      </tr>`
      )
      .join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="6">Failed to load enquiries: ${escapeHTML(err.message)}</td></tr>`;
  }
}

async function deleteEnquiry(id) {
  if (!confirm("Delete this enquiry?")) return;
  try {
    await adminApiRequest(`/api/contact/${id}`, { method: "DELETE" });
    showToast("Enquiry deleted.");
    loadEnquiries();
  } catch (err) {
    showToast(err.message, true);
  }
}

/* ---------------- Helpers ---------------- */
function escapeHTML(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function formatDateTimeAdmin(isoString) {
  try {
    const d = new Date(isoString);
    return d.toLocaleString("en-IN", { day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" });
  } catch (e) {
    return isoString;
  }
}
