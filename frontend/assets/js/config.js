/* ==========================================================
   Kanya Jewelers — Shared Frontend Configuration
   Update these values for your deployment.
   ========================================================== */

const CONFIG = {
  // Base URL of the FastAPI backend (no trailing slash)
  API_BASE_URL:" https://kanya-jewelary.onrender.com",

  SHOP_NAME: "Kanya Jewellers",
  SHOP_PHONE_DISPLAY: "+91 9370432627",
  SHOP_PHONE_TEL: "+919370432627",
  SHOP_WHATSAPP: "919370432627", // digits only, with country code
  SHOP_EMAIL: "suryankitbharbade123@gmail.com",
  SHOP_ADDRESS: "123 Sarafa Bazaar, Sitabuldi, Nagpur, Maharashtra 440012, India",
  SHOP_HOURS: "Mon – Sat: 10:30 AM – 8:30 PM | Sunday: 11:00 AM – 6:00 PM",
  MAP_EMBED_SRC:
    "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1281.6837891660734!2d76.58254574807339!3d18.397349114530286!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bcf835f43d398f9%3A0x21f85d5cbd9397a!2sKanya%20jewellers!5e1!3m2!1sen!2sin!4v1784029197013!5m2!1sen!2sin",
};

function whatsappLink(prefilledText) {
  const text = encodeURIComponent(prefilledText || "Hello Kanya Jewelers, I would like to know more about your collection.");
  return `https://wa.me/${CONFIG.SHOP_WHATSAPP}?text=${text}`;
}
