/**
 * Brand tokens for the Hyvä theme. Merge into web/tailwind/tailwind.config.js (Tailwind v3, Hyvä 1.3.x).
 * For Tailwind v4 themes (Hyvä 1.4+), use theme-v4.css instead.
 * Also add the homepage template folder to `content` so the classes are compiled
 * (for example the theme's Magento_Cms/templates/home directory, all .phtml files).
 */
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#EEF4FC', 100: '#D9E6F8', 200: '#B3CDF0', 300: '#82ACE4', 400: '#4F86D3',
          500: '#2A6CC4', 600: '#1A5FB4', 700: '#154D93', 800: '#123F77', 900: '#0F335F'
        },
        navy: { 700: '#1A2D42', 800: '#0F1D2E', 900: '#0A1628' }
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        display: ['"Space Grotesk"', 'Inter', 'ui-sans-serif', 'sans-serif']
      }
    }
  }
};
