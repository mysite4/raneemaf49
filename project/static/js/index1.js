document.getElementById("viewMoreBtn").addEventListener("click", function () {
  // تحديد جميع البطاقات
  const allCards = document.querySelectorAll(".card-item");

  // التحقق إذا كانت البطاقات المخفية موجودة
  const hiddenCards = Array.from(allCards).filter(card => card.classList.contains("d-none"));

  if (hiddenCards.length > 0) {
    // إظهار جميع البطاقات
    hiddenCards.forEach((card) => {
      card.classList.remove("d-none");
    });
    this.textContent = "View Less"; // تغيير نص الزر
  } else {
    // إخفاء البطاقات الإضافية (ابتداءً من البطاقة الرابعة)
    allCards.forEach((card, index) => {
      if (index >= 3) {
        card.classList.add("d-none");
      }
    });
    this.textContent = "View More"; // إعادة النص
  }
});

document.addEventListener("DOMContentLoaded", () => {
    const circles = document.querySelectorAll(".progress-circle");
  
    // Function to start animation
    const startAnimation = (circle) => {
      const value = parseInt(circle.getAttribute("data-value"));
      const label = circle.getAttribute("data-label");
      const maxValue = parseInt(circle.getAttribute("data-max")) || 100;
  
      // Create SVG elements
      const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      const background = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      const foreground = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  
      // Set attributes for background circle
      background.setAttribute("class", "background");
      background.setAttribute("cx", "70");
      background.setAttribute("cy", "70");
      background.setAttribute("r", "70");
  
      // Set attributes for foreground circle
      foreground.setAttribute("class", "foreground");
      foreground.setAttribute("cx", "70");
      foreground.setAttribute("cy", "70");
      foreground.setAttribute("r", "70");
  
      // Append circles to SVG
      svg.appendChild(background);
      svg.appendChild(foreground);
      circle.appendChild(svg);
  
      // Add value display
      const valueElement = document.createElement("div");
      valueElement.className = "value";
      valueElement.textContent = "0";
      circle.appendChild(valueElement);
  
      // Add label
      const labelElement = document.createElement("div");
      labelElement.className = "label";
      labelElement.textContent = label;
      circle.appendChild(labelElement);
  
      // Animate the circle and value
      let progress = 0;
      const interval = setInterval(() => {
        progress++;
        const offset = 440 - (440 * progress) / maxValue;
        foreground.style.strokeDashoffset = offset;
        valueElement.textContent = `${progress}`;
  
        if (progress === value) {
          clearInterval(interval);
        }
      }, 10);
    };
  
    // Intersection Observer setup
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            startAnimation(entry.target); // Start animation when visible
            observer.unobserve(entry.target); // Stop observing after animation starts
          }
        });
      },
      { threshold: 0.1 } // Trigger when 10% of the element is visible
    );
  
    // Observe each circle
    circles.forEach((circle) => observer.observe(circle));
  });
  


  document.addEventListener('DOMContentLoaded', function () {
  const slider = document.querySelector('.news-slider');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');

  let scrollAmount = 0;
  const scrollStep = 320; // عرض العنصر + المسافة بين العناصر

  prevBtn.addEventListener('click', function () {
    slider.scrollBy({
      left: -scrollStep,
      behavior: 'smooth'
    });
  });

  nextBtn.addEventListener('click', function () {
    slider.scrollBy({
      left: scrollStep,
      behavior: 'smooth'
    });
  });
});















function showContent(sectionId) {
  // تحديد المكان الذي سيتم فيه عرض المحتوى
  const contentContainer = document.getElementById('content-container');
  
  // إخفاء المحتوى الحالي
  contentContainer.classList.remove('fade-in');
  contentContainer.innerHTML = ''; // إزالة المحتوى القديم

  // تحديد المحتوى الجديد
  let newContent;
  if (sectionId === 'الموارد البشرية') {
    newContent = '<h3>الموارد البشرية</h3><h4>يعد قسم الموارد البشرية من الأقسام الحيوية في شركتنا حيث يهتم بتوظيف الكفاءات وتنمية مهارات الموظفين. يركز هذا القسم على خلق بيئة عمل مريحة وملهمة تساعد على تحسين الأداء العام.</h4>';
  } else if (sectionId === 'الشؤون القانونية') {
    newContent = '<h3>الشؤون القانونية</h3><h4>قسم الشؤون القانونية يتولى مسؤولية حماية حقوق الشركة وموظفيها من خلال توفير المشورة القانونية وإعداد العقود واتفاقيات الشراكة.</h4>';
  } else if (sectionId === 'الإدارة') {
    newContent = '<h3>الإدارة</h3><h4>يعتبر قسم الإدارة هو القلب النابض الذي ينسق جميع العمليات داخل الشركة ويضمن تحقيق أهدافها الاستراتيجية.</h4>';
  }

  // إضافة المحتوى الجديد
  contentContainer.innerHTML = newContent;

  // إضافة تأثير الظهور
  setTimeout(() => {
    contentContainer.classList.add('fade-in');
  }, 10);
}








  // استمع لحركة التمرير
  window.addEventListener("scroll", function () {
    const navbar = document.querySelector(".navbar"); // حدد عنصر النيف بار
    if (window.scrollY > 50) { // إذا تجاوز التمرير 50px
      navbar.classList.add("navbar-fixed"); // أضف الفئة لتفعيل الخلفية والظل
    } else {
      navbar.classList.remove("navbar-fixed"); // أزل الفئة عندما تعود للأعلى
    }
  });









  let currentIndex = 0;
  const images = document.querySelector('.carousel-images');
  const totalImages = document.querySelectorAll('.gallery-item').length;
  
  // تعيين الحركة التلقائية للتنقل بين الصور
  const autoSlide = setInterval(() => {
    currentIndex++;
    if (currentIndex >= totalImages / 5) {
      currentIndex = 0; // العودة إلى أول شريحة بعد الانتهاء من جميع الشرائح
    }
    images.style.transform = `translateX(-${currentIndex * 20}%)`; // الانتقال للشريحة التالية
  }, 1000); // التبديل بين الصور كل 3 ثوانٍ
  