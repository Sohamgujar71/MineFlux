gsap.registerPlugin(ScrollTrigger);

const select = (e) => document.querySelector(e);
const selectAll = (e) => document.querySelectorAll(e);

const loader = select('.loader');
const loaderInner = select('.loader .inner');
const progressBar = select('.loader .progress');

// Initialize the loader
function initLoader() {
    const tlLoaderIn = gsap.timeline({
        defaults: { duration: 1.1, ease: 'power2.out' },
        onComplete: initContent // Proceed to main content after loader finishes
    });

    const image = select('.loader__image img');
    const mask = select('.loader__image--mask');
    const line1 = select('.loader__title--mask:nth-child(1) span');
    const line2 = select('.loader__title--mask:nth-child(2) span');
    const loaderContent = select('.loader__content');

    // Make sure the loader is visible at the start
    gsap.set(loader, { autoAlpha: 1 });
    gsap.set(loaderContent, { autoAlpha: 1 });

    tlLoaderIn
        .to(loaderInner, { scaleY: 1, transformOrigin: 'bottom', ease: 'power1.inOut' })
        .from(mask, { yPercent: 100 }, '-=0.6')
        .from(image, { yPercent: -80 }, '-=0.6')
        .from([line1, line2], { yPercent: 100, stagger: 0.1 }, '-=0.4');

    const tlLoaderOut = gsap.timeline({
        defaults: { duration: 1.2, ease: 'power2.inOut' },
        delay: 1
    });

    tlLoaderOut
        .to([line1, line2], { yPercent: -500, stagger: 0.2 })
        .to([loader, loaderContent], { yPercent: -100 }, 0.2);

    const tlLoader = gsap.timeline();
    tlLoader
        .add(tlLoaderIn)
        .add(tlLoaderOut);
}

// Barba.js Page Transitions
barba.init({
    transitions: [{
        once() {
            initLoader();
        },
        async leave({ current }) {
            try {
                await pageTransitionIn(current);
            } catch (error) {
                console.error('Error during page transition in', error);
            }
        },
        enter({ next }) {
            try {
                pageTransitionOut(next);
            } catch (error) {
                console.error('Error during page transition out', error);
            }
        }
    }]
});


function initContent() {
    // Show the main content and remove the loading class
    document.body.classList.remove('is-loading');
    select('#main').style.visibility = 'visible';
    ScrollTrigger.refresh(); // Refresh ScrollTrigger after content is revealed
}

function pageTransitionIn({ container }) {
    return gsap.timeline({
        defaults: { duration: 0.8, ease: 'power1.inOut' }
    })
    .set(loaderInner, { autoAlpha: 0 })
    .fromTo(loader, { yPercent: -100 }, { yPercent: 0 }) // Brings loader down
    .fromTo('.loader__mask', { yPercent: 80 }, { yPercent: 0 }, 0) // Mask animation
    .to(container, { y: 150 }, 0); // Slide content into view
}

function pageTransitionOut({ container }) {
    return gsap.timeline({
        defaults: { duration: 0.8, ease: 'power1.inOut' },
        onComplete: () => initContent() // Init content once the loader moves out
    })
    .to(loader, { yPercent: 100 }) // Moves loader up
    .to('.loader__mask', { yPercent: -80 }, 0) // Moves mask out
    .from(container, { y: -150 }, 0); // Slide content out of view
}

document.addEventListener("DOMContentLoaded", function () {
    // Start loading animation when the DOM is fully loaded
    document.body.classList.add('is-loading');
    initLoader();
});
