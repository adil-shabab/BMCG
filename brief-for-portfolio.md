# PROJECT BRIEF

## 1. Project Name

**BMCG – Accounting & Finance Solutions** (marketing website)

## 2. Project Overview

BMCG is a multi-page marketing and lead-generation website for an accounting and auditing firm serving businesses and individuals in the UAE and UK. It presents the firm's services, team, credibility signals (stats, client testimonials), and provides a contact channel for prospective clients to book an appointment or send an enquiry. The site is a fully client-side, static front-end implementation built by customising a purchased HTML template ("Wexico" by Awaiken) with BMCG-specific branding, content, and service offerings. Its primary purpose is to communicate the firm's value proposition and convert visitors into enquiries.

## 3. Key Features

- Responsive multi-page site (Home, About, Services, Service Detail, Contact) with a shared sticky header and footer.
- Services catalogue covering six offerings: Bookkeeping (UAE & UK), VAT Returns & Filing (UAE & UK), Corporate Tax Services, Year-End Financial Preparation, Internal Audit & Risk Management, and Financial Analysis & Advisory.
- Service detail page with process steps, benefits, category sidebar, and a call-to-action box.
- Contact page with a validated enquiry form (first/last name, email, phone, message) and inline field-level error messages.
- Embedded Google Map showing the firm's Dubai location, plus contact info blocks (address, phone numbers, email addresses).
- Animated statistic counters ("state counter") that count up when scrolled into view.
- Client testimonials carousel with autoplay and prev/next navigation.
- Scroll-triggered entrance animations for text and images throughout the pages.
- Custom animated cursor, page preloader, and video lightbox popup.
- Mobile off-canvas navigation menu.

## 4. Technology Stack

- **Frontend:** HTML5, CSS3 (hand-authored `custom.css` using CSS custom properties as design tokens), Bootstrap (grid, components, utilities), vanilla DOM + jQuery.
- **Backend:** None in this repository. The contact form performs an AJAX `POST` to `form-process.php`; that server-side handler is not part of the codebase.
- **Database:** None.
- **APIs:** None consumed programmatically. Google Maps is included as an `<iframe>` embed.
- **Authentication:** None (public marketing site).
- **Third-party services / integrations:** Google Maps (embed), Google Fonts (Plus Jakarta Sans), Font Awesome icon font (self-hosted webfonts).
- **Deployment / Infrastructure:** No deployment configuration present. It is a static site deployable to any static host or CDN.
- **Important libraries / tools:**
  - jQuery 3.7.1
  - Bootstrap (CSS + JS bundle)
  - GSAP with ScrollTrigger and SplitText (scroll and text animations)
  - Swiper.js (testimonial slider)
  - WOW.js (on-scroll reveal animations)
  - jQuery CounterUp + Waypoints (animated counters)
  - Magnific Popup (video/image lightbox)
  - SlickNav (responsive mobile menu)
  - SmoothScroll, custom `magiccursor.js` (magic cursor)
  - `validator.min.js` (Bootstrap-style form validation)

## 5. Architecture

The project is a purely client-side, static multi-page website. Each HTML page is self-contained and repeats shared markup (header navigation, footer, newsletter block). All pages share a single stylesheet set (`custom.css` plus vendor CSS) and a single script set, with page behaviour centralised in `js/function.js`, which initialises the preloader, mobile menu, testimonial Swiper, animated counters, GSAP scroll/text animations, WOW.js, the video lightbox, and contact-form validation. Styling is driven by CSS custom properties defined in `:root` (primary/secondary/accent/text/divider colours and font family), keeping the theme centralised. The contact form is validated in the browser and then submitted via jQuery AJAX to a `form-process.php` endpoint (not included here), with success/error feedback rendered inline. The map is delivered through a Google Maps embed iframe. There is no build step, bundler, package manifest, or server component in the repository.

## 6. User Roles

Not applicable. The site has a single audience — public/anonymous visitors (prospective and existing clients). There is no authentication, no account system, and no admin interface in the codebase.

## 7. Important Pages / Modules

- **`index.html` – Home:** hero with appointment CTA, about-company highlights, services overview, about section with video popup, animated state counters, "Why Choose Us", "We Help" areas, testimonials carousel, CTA box, newsletter block, footer.
- **`about.html` – About Us:** page header, company/about content, company planning section, "Why Choose Us", team section, satisfied-client block, testimonials, state counters.
- **`services.html` – Services:** page header and a grid of the six service offerings, "Why Choose Us", testimonials, CTA box.
- **`service-single.html` – Service Detail:** featured image, entry content, process steps, service benefits, customer-benefits section, category list sidebar, and sidebar CTA box.
- **`contact.html` – Contact:** section intro, contact form, contact info items (location / phone / email), and a Google Maps location section.
- **`js/function.js`:** the site's behaviour module (all interactive component initialisation).
- **`css/custom.css`:** the project's design system and all page styling (~4,000 lines, sectioned by page/component, with a responsive block).

## 8. Technical Highlights

- **Coordinated scroll animation system:** GSAP `ScrollTrigger` with `SplitText` powers three reusable text-animation styles (character/word/line staggering) plus an image "reveal" wipe effect, layered with WOW.js for section fade-ins.
- **Design tokens in CSS:** a centralised `:root` custom-property palette and font variable make the whole multi-page theme adjustable from one place.
- **Progressive-enhancement contact form:** `validator.js` provides accessible, per-field inline validation with `help-block` error containers before an AJAX submission, and success/failure states are reflected back into the DOM.
- **Performance-aware counters:** statistics animate only when scrolled into the viewport via Waypoints + CounterUp rather than on page load.
- **Custom interaction details:** an animated "magic cursor", a branded preloader, smooth-scroll, and a Magnific Popup iframe lightbox for the promo video.
- **Responsive navigation:** desktop Bootstrap navbar degrades to a SlickNav off-canvas menu on smaller breakpoints.
- **Self-hosted icon fonts:** Font Awesome served from local `webfonts/` (woff2 + ttf) to avoid an external icon CDN dependency.

## 9. Integrations

- **Google Maps** – location map embedded via iframe on the Contact page (Dubai, UAE).
- **Google Fonts** – "Plus Jakarta Sans" loaded from the Google Fonts CDN.
- **Contact form endpoint** – client-side AJAX targets `form-process.php` for enquiry submission handling (server handler not present in this repository).
- No payment gateway, email service SDK, analytics, or cloud service integration is present in the codebase.

## 10. Deployment

No deployment or infrastructure configuration is included in the repository — there is no Docker setup, CI/CD pipeline, environment/config file, `package.json`, or build tooling. The project is a static bundle of HTML, CSS, JS, images, and webfonts that can be served directly by any static web host, object storage + CDN, or shared hosting. If the contact form is to function, a `form-process.php` handler must be provided by the hosting environment (implying a PHP-capable server for that single feature).

## 11. Portfolio Summary

- **One-line description:** A responsive, animation-rich static marketing website for a UAE/UK accounting and auditing firm, built by customising and extending an HTML template with bespoke content, styling, and interactions.

- **Short portfolio description:** BMCG is a five-page front-end marketing site for an accounting practice, presenting services, team, credibility metrics, and a validated enquiry form. It layers GSAP ScrollTrigger/SplitText, Swiper, WOW.js and animated counters over a Bootstrap grid, with a centralised CSS-custom-property theme and a shared JavaScript behaviour module. The build is dependency-light and deployable to any static host.

- **Technology stack:** HTML5, CSS3 (CSS custom properties), Bootstrap, jQuery, GSAP (ScrollTrigger, SplitText), Swiper.js, WOW.js, CounterUp/Waypoints, Magnific Popup, SlickNav, Google Maps embed, Google Fonts, Font Awesome.

- **5 strongest features:**
  1. Multi-style scroll-triggered text and image animation system built on GSAP ScrollTrigger + SplitText.
  2. Fully responsive multi-page layout with a Bootstrap navbar that converts to an off-canvas mobile menu.
  3. Accessible, inline-validated contact form with AJAX submission and DOM feedback states.
  4. Viewport-triggered animated statistics counters and an autoplaying testimonials carousel.
  5. Centralised, token-driven theming via CSS custom properties across the whole site.

- **Project category:** Front-end / Static marketing website (corporate services / business landing site).
