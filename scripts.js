document.addEventListener("DOMContentLoaded", function () {

    // دکمه Let's Talk: تنها .btn-53 که مستقیم فرزند .hero-content است
    const letsTalk = document.querySelector('.hero-content > .btn-53');

    // مقصد: باکس فرم تماس
    const contactBox = document.querySelector('.form-container.contact-box');

    if (letsTalk && contactBox) {
        letsTalk.addEventListener('click', function () {
            contactBox.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    }

});

// form func

emailjs.init("gwi6eirufmo2K9Sf7");

const contactForm = document.getElementById('contactForm');

if (contactForm) {
    contactForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const name = document.querySelector('#name').value.trim();
        const email = document.querySelector('#email').value.trim();
        const number = document.querySelector('#number').value.trim();
        const message = document.querySelector('#textarea').value.trim();

        if (!name || !email || !number || !message) {
            alert('Please fill in all fields.');
            return;
        }

        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            alert('Please enter a valid email address.');
            return;
        }

        const submitBtn = contactForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;

        emailjs.send("service_hpsfbqh", "loidj5z", {
            name: name,
            email: email,
            number: number,
            message: message
        })
        .then(function () {
            alert(`Thank you ${name}! Your message has been sent.`);
            contactForm.reset();
        })
        .catch(function (error) {
            alert('Something went wrong. Please try again.');
            console.error('EmailJS error:', error);
        })
        .finally(function () {
            submitBtn.disabled = false;
        });
    });
}
// IntersectionObserver func

const sections = document.querySelectorAll('section');

const observer = new IntersectionObserver(
    function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('show-section');
                observer.unobserve(entry.target);
            }
        });
    },
    { threshold: 0.15 }
);

sections.forEach(function (section) {
    section.classList.add('hidden-section');
    observer.observe(section);
});

// project func



// hover me

const cards = document.querySelectorAll('.services .btn, .skills .btn');

cards.forEach(function (card) {
    card.addEventListener('mouseenter', function () {
        card.classList.add('active-card');
    });
    card.addEventListener('mouseleave', function () {
        card.classList.remove('active-card');
    });
});
// EmailJS init