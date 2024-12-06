# WTG (Web to GUI) — это инновационная библиотека для разработчиков, которая позволяет интегрировать интерактивные HTML-сайты с анимациями и динамическим контентом в настольные GUI-приложения. Используя WTG, вы можете создавать веб-страницы с мощными анимациями и плавными переходами и отображать их прямо в вашем приложении.

## Ключевые особенности:
# 🌐 Интеграция HTML и GUI: Легко встраивайте HTML, CSS и JavaScript в графические интерфейсы.
# ✨ Поддержка анимаций: Используйте популярные библиотеки, такие как GSAP, для создания плавных анимаций.
# ⚡ Мгновенный запуск: Просто передайте HTML-контент, и приложение сразу отобразит веб-страницу.
# 📱 Адаптивность: Поддержка современных стандартов HTML5 и CSS3 для создания отзывчивых интерфейсов.
# 🛠️ Лёгкость настройки: Никаких сложных конфигураций — достаточно простого кода для запуска.
Пример использования:
from WTG import HtmlViewerApp

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Animated Website</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js" defer></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js" defer></script>
  <script>
  document.addEventListener("DOMContentLoaded", () => {
    gsap.from("nav h1", {
      duration: 1,
      y: -50,
      opacity: 0,
      ease: "bounce.out",
    });
    gsap.from("nav a", {
      duration: 1,
      opacity: 0,
      stagger: 0.3,
      delay: 0.5,
    });
    gsap.utils.toArray(".section").forEach((section) => {
      gsap.fromTo(
        section,
        { opacity: 0, y: 50 },
        {
          opacity: 1,
          y: 0,
          scrollTrigger: {
            trigger: section,
            start: "top 80%",
            toggleActions: "play none none reverse",
          },
          duration: 1.2,
          ease: "power4.out",
        }
      );
    });
  });
  </script>
</head>
<body>
  <header>
    <nav>
      <h1>Dynamic Animations</h1>
      <ul>
        <li><a href="#home">Home</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#contact">Contact</a></li>
      </ul>
    </nav>
  </header>
  <section id="home" class="section">
    <h2>Welcome to Our Animated World</h2>
    <p>Experience smooth and beautiful animations.</p>
  </section>
  <section id="about" class="section">
    <h2>About Us</h2>
    <p>We create immersive web experiences.</p>
  </section>
  <section id="contact" class="section">
    <h2>Contact Us</h2>
    <p>Get in touch for collaborations and projects.</p>
  </section>
  <footer>
    <p>© 2024 Dynamic Animations. All rights reserved.</p>
  </footer>
</body>
</html>
"""

app = HtmlViewerApp(html_content=html_content)
app.run()


# Преимущества:
Быстрое прототипирование: Разрабатывайте сложные интерфейсы с анимациями за считанные минуты.
Широкие возможности кастомизации: Используйте весь потенциал веб-технологий в нативных приложениях.
Простой и интуитивно понятный API: Позволяет минимизировать количество кода и сосредоточиться на дизайне.
С WTG ваши приложения станут современными, динамичными и удобными для пользователей, объединяя мощь веба и гибкость настольных приложений.