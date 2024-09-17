gsap.from("#page2 #map", {
    scale: 0.5,
    delay: 1,
    duration: 1,
    ease: "back.out(1.4)", // Smooth and pop effect
    scrollTrigger: "#page2 #map"
});


// Set the "finished" state as the initial state
gsap.set(".feature-card2", {
    x: -280,
    rotate: 10
});

gsap.set(".feature-card1", {
    x: 280,
    rotate: -10
});

// Now animate it back to the original state
gsap.to(".feature-card2", {
    x: 0, // Move back to the original position
    duration: 2,
    delay: 1,
    rotate: 0, // Reset the rotation
    scrollTrigger: ".feature-card2"
});

gsap.to(".feature-card1", {
    x: 0, // Move back to the original position
    duration: 2,
    delay: 1,
    rotate: 0, // Reset the rotation
    scrollTrigger: ".feature-card1"
});

var tl = gsap.timeline()
tl.from(".navbar h1",{
    y:-30,
    opacity:0,
    duration:1,
    delay:0.3
})

tl.from(".nav-links>a",{
    y:-30,
    opacity:0,
    duration:0.8,
    stagger:0.3
})

// Animate the logo and text to jump into the screen
// Professional animation for logo and text
gsap.from(".logo-container", {
    scale: 0.8, // Start slightly smaller
    opacity: 0, // Start hidden
    y: 50, // Start from slightly below
    duration: 1.2, // Duration of the animation
    ease: "power3.out" // Smooth and professional easing
});

