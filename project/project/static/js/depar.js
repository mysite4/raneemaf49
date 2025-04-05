function showSection(sectionId) {
    // إخفاء جميع الأقسام
    let sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.style.display = 'none';  // إخفاء جميع الأقسام
    });

    // إظهار القسم المحدد
    let activeSection = document.getElementById(sectionId);
    if (activeSection) {
        activeSection.style.display = 'block';  // إظهار القسم الذي تم تحديده
    }
}
