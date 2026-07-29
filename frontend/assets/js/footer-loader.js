/* Injects the shared site footer into <footer id="siteFooter"></footer> */
(function () {
  const el = document.getElementById("siteFooter");
  if (!el) return;

  el.innerHTML = `
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <span class="brand-name gold-text" style="font-family:var(--font-heading);">Kanya Jewelers</span>
          <p>Crafting trust and elegance since 1998. Hallmark certified gold and silver jewellery for every occasion.</p>
          <div class="social-icons">
            <a href="#" aria-label="Facebook">f</a>
            <a href="https://www.instagram.com/kanya_jewellers/" aria-label="Instagram">ig</a>
            <a href="#" aria-label="YouTube">yt</a>
          </div>
        </div>
        <div class="footer-col">
          <h4>Quick Links</h4>
          <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="about.html">About Us</a></li>
            <li><a href="collection.html">Collection</a></li>
            <li><a href="rates.html">Gold &amp; Silver Rates</a></li>
            <li><a href="gallery.html">Gallery</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Categories</h4>
          <ul>
            <li><a href="collection.html?category=rings">Rings</a></li>
            <li><a href="collection.html?category=necklaces">Necklaces</a></li>
            <li><a href="collection.html?category=bangles">Bangles</a></li>
            <li><a href="collection.html?category=bridal-collection">Bridal Collection</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Contact</h4>
          <ul>
            <li data-shop-address style="color:#b8b8b8;font-size:14px;"></li>
            <li><a href="tel:" data-call data-shop-phone></a></li>
            <li><a href="mailto:" data-shop-email></a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        &copy; <span data-year></span> Kanya Jewelers. All Rights Reserved. &nbsp;|&nbsp;
        <a href="privacy-policy.html">Privacy Policy</a>
      </div>
    </div>
  `;

  // re-run shortcut binding for the newly injected footer content
  if (typeof injectContactShortcuts === "function") injectContactShortcuts();
})();
