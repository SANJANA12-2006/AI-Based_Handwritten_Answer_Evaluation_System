document.addEventListener("DOMContentLoaded", () => {

    const loader = document.getElementById("pageLoader");

    setTimeout(() => {
        if (loader) {
            loader.classList.add("hide");
        }
    }, 500);


    const navbar = document.getElementById("navbar");

    const handleScroll = () => {
        if (!navbar) return;

        if (window.scrollY > 20) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    };

    window.addEventListener("scroll", handleScroll);

    handleScroll();


    const mobileMenu = document.getElementById("mobileMenu");
    const navLinks = document.getElementById("navLinks");

    if (mobileMenu && navLinks) {

        mobileMenu.addEventListener("click", () => {
            navLinks.classList.toggle("mobile-open");
        });


        document.querySelectorAll(".nav-link").forEach(link => {

            link.addEventListener("click", () => {
                navLinks.classList.remove("mobile-open");
            });

        });

    }


    const revealElements = document.querySelectorAll(
        ".step-card, .feature-card, .role-item, .stat-item"
    );

    const revealObserver = new IntersectionObserver(
        entries => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.target.style.opacity = "1";
                    entry.target.style.transform = "translateY(0)";

                    revealObserver.unobserve(entry.target);
                }

            });

        },
        {
            threshold: 0.12
        }
    );


    revealElements.forEach(element => {

        element.style.opacity = "0";
        element.style.transform = "translateY(20px)";
        element.style.transition =
            "opacity 0.6s ease, transform 0.6s ease";

        revealObserver.observe(element);

    });

});