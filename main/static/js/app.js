document.addEventListener("DOMContentLoaded", function () {
    // =================================================================
    // بخش ۱: پارتیکل‌های ۳بعدی (Section 2 - Particles Canvas)
    // =================================================================
    (function initParticlesSection() {
        const container = document.getElementById("particles-canvas");
        if (!container || typeof THREE === "undefined") return;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(
            75,
            container.clientWidth / container.clientHeight,
            0.1,
            1000,
        );
        const renderer = new THREE.WebGLRenderer({
            alpha: true,
            antialias: false, // غیرفعال کردن برای کاهش بار GPU
            powerPreference: "low-power", // درخواست استفاده از حالت کم‌مصرف
        });

        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(0.5);
        container.appendChild(renderer.domElement);

        // Particle System Setup
        const count = 60;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(count * 3);

        for (let i = 0; i < count * 3; i += 3) {
            positions[i] = (Math.random() - 0.5) * 15;
            positions[i + 1] = (Math.random() - 0.5) * 10;
            positions[i + 2] = (Math.random() - 0.5) * 10;
        }

        geometry.setAttribute(
            "position",
            new THREE.BufferAttribute(positions, 3),
        );

        const material = new THREE.PointsMaterial({
            color: 0x2196f3,
            size: 0.12,
            transparent: true,
            opacity: 0.8,
        });

        const points = new THREE.Points(geometry, material);
        scene.add(points);

        camera.position.z = 6;

        let mouseX = 0;
        let mouseY = 0;

        // کد قبلی mousemove را کاملا پاک کنید و این کد بهینه را جایگزین کنید:
        let mouseTicking = false;
        window.addEventListener("mousemove", (e) => {
            if (!mouseTicking) {
                window.requestAnimationFrame(() => {
                    mouseX = (e.clientX / window.innerWidth - 0.5) * 0.5;
                    mouseY = (e.clientY / window.innerHeight - 0.5) * 0.5;
                    mouseTicking = false;
                });
                mouseTicking = true;
            }
        }, { passive: true });

        let pClock = new THREE.Clock();
        let pDelta = 0;
        let pInterval = 1 / 30; // 3۰ فریم بر ثانیه
        let pAnimId = null;

        function animateParticles() {
            pAnimId = requestAnimationFrame(animateParticles);
            pDelta += pClock.getDelta();

            if (pDelta > pInterval) {
                points.rotation.y += 0.0015;
                points.rotation.x += 0.001;

                camera.position.x += (mouseX - camera.position.x) * 0.05;
                camera.position.y += (-mouseY - camera.position.y) * 0.05;

                renderer.render(scene, camera);
                pDelta = pDelta % pInterval;
            }
        }

        // توقف رندر هنگام اسکرول و خارج شدن از دید
        const pObserver = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        animateParticles();
                    } else {
                        cancelAnimationFrame(pAnimId);
                    }
                });
            },
            { threshold: 0.1 },
        );
        pObserver.observe(container);

        window.addEventListener("resize", () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });
    })();

    // =================================================================
    // بخش ۲: کارفرمایان برتر (3D Globe + Tech Tower + Interactive Cards)
    // =================================================================
    (function initEmployersSection() {
        // 1. THREE.JS Scene Setup
        const empCanvasContainer = document.getElementById(
            "employers-3d-canvas",
        );
        if (empCanvasContainer && typeof THREE !== "undefined") {
            const empScene = new THREE.Scene();
            const empCamera = new THREE.PerspectiveCamera(
                60,
                empCanvasContainer.clientWidth /
                empCanvasContainer.clientHeight,
                0.1,
                1000,
            );
            const empRenderer = new THREE.WebGLRenderer({
                alpha: true,
                antialias: true,
            });

            empRenderer.setSize(
                empCanvasContainer.clientWidth,
                empCanvasContainer.clientHeight,
            );
            empRenderer.setPixelRatio(0.5);
            empCanvasContainer.appendChild(empRenderer.domElement);

            const empWorldGroup = new THREE.Group();
            empScene.add(empWorldGroup);

            // 3D Wireframe Globe
            const empGlobeGeo = new THREE.SphereGeometry(3.2, 24, 24);
            const empGlobeMat = new THREE.MeshBasicMaterial({
                color: 0x0d47a1,
                wireframe: true,
                transparent: true,
                opacity: 0.25,
            });
            const empGlobe = new THREE.Mesh(empGlobeGeo, empGlobeMat);
            empWorldGroup.add(empGlobe);

            // Central Tech Tower
            const empTowerGeo = new THREE.CylinderGeometry(0.3, 0.6, 4, 6);
            const empTowerMat = new THREE.MeshBasicMaterial({
                color: 0x2196f3,
                wireframe: true,
                transparent: true,
                opacity: 0.6,
            });
            const empTower = new THREE.Mesh(empTowerGeo, empTowerMat);
            empWorldGroup.add(empTower);

            // Network Nodes Grid
            const empNodesCount = 40;
            const empNodePositions = new Float32Array(empNodesCount * 3);

            for (let i = 0; i < empNodesCount * 3; i += 3) {
                const u = Math.random();
                const v = Math.random();
                const theta = u * 2.0 * Math.PI;
                const phi = Math.acos(2.0 * v - 1.0);
                const r = 3.3;

                empNodePositions[i] = r * Math.sin(phi) * Math.cos(theta);
                empNodePositions[i + 1] = r * Math.sin(phi) * Math.sin(theta);
                empNodePositions[i + 2] = r * Math.cos(phi);
            }

            const empNodeGeo = new THREE.BufferGeometry();
            empNodeGeo.setAttribute(
                "position",
                new THREE.BufferAttribute(empNodePositions, 3),
            );
            const empNodeMat = new THREE.PointsMaterial({
                color: 0x64b5f6,
                size: 0.1,
                transparent: true,
                opacity: 0.9,
            });
            const empNodes = new THREE.Points(empNodeGeo, empNodeMat);
            empWorldGroup.add(empNodes);

            empCamera.position.z = 7;
            empCamera.position.y = 1;

            let empMouseX = 0,
                empMouseY = 0;
            window.addEventListener("mousemove", (e) => {
                empMouseX = (e.clientX / window.innerWidth - 0.5) * 0.4;
                empMouseY = (e.clientY / window.innerHeight - 0.5) * 0.4;
            });

            let empClock = new THREE.Clock();
            let empDelta = 0;
            let empInterval = 1 / 30;
            let empAnimId = null;

            function renderEmp3D() {
                empAnimId = requestAnimationFrame(renderEmp3D);
                empDelta += empClock.getDelta();

                if (empDelta > empInterval) {
                    empWorldGroup.rotation.y += 0.002;
                    empTower.rotation.y -= 0.005;

                    empCamera.position.x +=
                        (empMouseX - empCamera.position.x) * 0.05;
                    empCamera.position.y +=
                        (-empMouseY + 1 - empCamera.position.y) * 0.05;
                    empCamera.lookAt(empScene.position);

                    empRenderer.render(empScene, empCamera);
                    empDelta = empDelta % empInterval;
                }
            }

            // توقف رندر هنگام اسکرول
            const empObserver = new IntersectionObserver(
                (entries) => {
                    entries.forEach((entry) => {
                        if (entry.isIntersecting) {
                            renderEmp3D();
                        } else {
                            cancelAnimationFrame(empAnimId);
                        }
                    });
                },
                { threshold: 0.1 },
            );
            empObserver.observe(empCanvasContainer);

            window.addEventListener("resize", () => {
                empCamera.aspect =
                    empCanvasContainer.clientWidth /
                    empCanvasContainer.clientHeight;
                empCamera.updateProjectionMatrix();
                empRenderer.setSize(
                    empCanvasContainer.clientWidth,
                    empCanvasContainer.clientHeight,
                );
            });
        }

        // 2. GSAP Scroll Reveal & Counter
        if (
            typeof gsap !== "undefined" &&
            typeof ScrollTrigger !== "undefined"
        ) {
            gsap.registerPlugin(ScrollTrigger);

            gsap.utils.toArray(".employer-reveal").forEach((el, index) => {
                gsap.to(el, {
                    scrollTrigger: {
                        trigger: el,
                        start: "top 85%",
                        toggleActions: "play none none none",
                    },
                    opacity: 1,
                    y: 0,
                    duration: 0.8,
                    delay: index * 0.1,
                    ease: "power2.out",
                });
            });

            document
                .querySelectorAll(".employer-counter")
                .forEach((counter) => {
                    const target = +counter.getAttribute("data-target");
                    ScrollTrigger.create({
                        trigger: counter,
                        start: "top 90%",
                        onEnter: () => {
                            gsap.to(counter, {
                                innerText: target,
                                duration: 2,
                                snap: { innerText: 1 },
                                ease: "power1.out",
                                onUpdate: function () {
                                    counter.innerText = Math.ceil(
                                        this.targets()[0].innerText,
                                    ).toLocaleString("fa-IR");
                                },
                            });
                        },
                    });
                });
        }

        // 3. CSS 3D Tilt & Glow
        document.querySelectorAll(".employer-tilt-card").forEach((card) => {
            let isTicking = false;

            card.addEventListener("mousemove", (e) => {
                if (!isTicking) {
                    window.requestAnimationFrame(() => {
                        const rect = card.getBoundingClientRect();
                        const x = e.clientX - rect.left;
                        const y = e.clientY - rect.top;

                        card.style.setProperty("--emp-mouse-x", `${x}px`);
                        card.style.setProperty("--emp-mouse-y", `${y}px`);

                        const centerX = rect.width / 2;
                        const centerY = rect.height / 2;
                        const rotateX = ((y - centerY) / centerY) * -8;
                        const rotateY = ((x - centerX) / centerX) * 8;

                        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
                        isTicking = false;
                    });
                    isTicking = true;
                }
            });

            card.addEventListener("mouseleave", () => {
                card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)`;
            });
        });
    })();
});
(function () {
    document.addEventListener("DOMContentLoaded", function () {
        if (
            typeof gsap !== "undefined" &&
            typeof ScrollTrigger !== "undefined"
        ) {
            gsap.registerPlugin(ScrollTrigger);

            gsap.utils.toArray(".cta-reveal").forEach((el, index) => {
                gsap.to(el, {
                    scrollTrigger: {
                        trigger: el,
                        start: "top 85%",
                        toggleActions: "play none none none",
                    },
                    opacity: 1,
                    y: 0,
                    duration: 0.8,
                    delay: index * 0.15,
                    ease: "power2.out",
                });
            });
        }
    });
})();
// comment
(function () {
    document.addEventListener("DOMContentLoaded", function () {
        // Tab Switching
        const btnJobseekers = document.getElementById("btn-jobseekers");
        const btnEmployers = document.getElementById("btn-employers");
        const tabJobseekers = document.getElementById("tab-jobseekers-content");
        const tabEmployers = document.getElementById("tab-employers-content");

        if (btnJobseekers && btnEmployers && tabJobseekers && tabEmployers) {
            btnJobseekers.addEventListener("click", () => {
                btnJobseekers.classList.add(
                    "bg-[#2196F3]",
                    "text-white",
                    "shadow-lg",
                    "shadow-[#2196F3]/30",
                );
                btnJobseekers.classList.remove("text-slate-400");

                btnEmployers.classList.remove(
                    "bg-[#2196F3]",
                    "text-white",
                    "shadow-lg",
                    "shadow-[#2196F3]/30",
                );
                btnEmployers.classList.add("text-slate-400");

                tabEmployers.classList.add("hidden");
                tabJobseekers.classList.remove("hidden");
            });

            btnEmployers.addEventListener("click", () => {
                btnEmployers.classList.add(
                    "bg-[#2196F3]",
                    "text-white",
                    "shadow-lg",
                    "shadow-[#2196F3]/30",
                );
                btnEmployers.classList.remove("text-slate-400");

                btnJobseekers.classList.remove(
                    "bg-[#2196F3]",
                    "text-white",
                    "shadow-lg",
                    "shadow-[#2196F3]/30",
                );
                btnJobseekers.classList.add("text-slate-400");

                tabJobseekers.classList.add("hidden");
                tabEmployers.classList.remove("hidden");
            });
        }

        // GSAP Scroll Reveal
        if (
            typeof gsap !== "undefined" &&
            typeof ScrollTrigger !== "undefined"
        ) {
            gsap.registerPlugin(ScrollTrigger);

            gsap.utils.toArray(".testimonial-reveal").forEach((el, index) => {
                gsap.to(el, {
                    scrollTrigger: {
                        trigger: el,
                        start: "top 85%",
                        toggleActions: "play none none none",
                    },
                    opacity: 1,
                    y: 0,
                    duration: 0.8,
                    delay: index * 0.12,
                    ease: "power2.out",
                });
            });
        }

        // 3D Tilt Effect
        document.querySelectorAll(".testimonial-tilt-card").forEach((card) => {
            card.addEventListener("mousemove", (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = ((y - centerY) / centerY) * -6;
                const rotateY = ((x - centerX) / centerX) * 6;

                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-6px)`;
            });

            card.addEventListener("mouseleave", () => {
                card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)`;
            });
        });
    });
})();
//blog
(function () {
    document.addEventListener("DOMContentLoaded", function () {
        // GSAP Scroll Reveal
        if (
            typeof gsap !== "undefined" &&
            typeof ScrollTrigger !== "undefined"
        ) {
            gsap.registerPlugin(ScrollTrigger);

            gsap.utils.toArray(".blog-reveal").forEach((el, index) => {
                gsap.to(el, {
                    scrollTrigger: {
                        trigger: el,
                        start: "top 85%",
                        toggleActions: "play none none none",
                    },
                    opacity: 1,
                    y: 0,
                    duration: 0.8,
                    delay: index * 0.12,
                    ease: "power2.out",
                });
            });
        }
    });
})();
// const canvas = document.getElementById("3d-globe");
// const ctx = canvas.getContext("2d");

// function resizeCanvas() {
//     canvas.width = canvas.parentElement.offsetWidth;
//     canvas.height = canvas.parentElement.offsetHeight;
// }
// window.addEventListener("resize", resizeCanvas);
// resizeCanvas();

// // ایجاد نقاط کره سه بعدی
// const dots = [];
// const numDots = 180;
// const radius = 220;

// for (let i = 0; i < numDots; i++) {
//     const theta = Math.acos(2 * Math.random() - 1);
//     const phi = 2 * Math.PI * Math.random();
//     dots.push({
//         x: radius * Math.sin(theta) * Math.cos(phi),
//         y: radius * Math.sin(theta) * Math.sin(phi),
//         z: radius * Math.cos(theta),
//     });
// }

// let angleY = 0;
// let angleX = 0;

// let globeLastTime = 0;
// let globeInterval = 1000 / 40; // ۴۰ فریم بر ثانیه
// let globeAnimId = null;

// function render3D(currentTime) {
//     globeAnimId = requestAnimationFrame(render3D);

//     if (!globeLastTime) globeLastTime = currentTime;
//     const elapsed = currentTime - globeLastTime;

//     if (elapsed > globeInterval) {
//         globeLastTime = currentTime - (elapsed % globeInterval);

//         ctx.clearRect(0, 0, canvas.width, canvas.height);

//         const centerX = canvas.width / 2;
//         const centerY = canvas.height / 2;

//         angleY += 0.003;
//         angleX += 0.001;

//         dots.forEach((dot) => {
//             let x1 = dot.x * Math.cos(angleY) - dot.z * Math.sin(angleY);
//             let z1 = dot.z * Math.cos(angleY) + dot.x * Math.sin(angleY);

//             let y1 = dot.y * Math.cos(angleX) - z1 * Math.sin(angleX);
//             let z2 = z1 * Math.cos(angleX) + dot.y * Math.sin(angleX);

//             const scale = 300 / (300 + z2);
//             const x2d = x1 * scale + centerX;
//             const y2d = y1 * scale + centerY;

//             const alpha = Math.max(0.1, (z2 + radius) / (2 * radius));
//             ctx.fillStyle = `rgba(144, 202, 249, ${alpha})`;
//             ctx.beginPath();
//             ctx.arc(x2d, y2d, 1.8 * scale, 0, Math.PI * 2);
//             ctx.fill();
//         });
//     }
// }

// توقف رندر کانواس هنگام خارج شدن از دید
if (canvas) {
    const globeObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    render3D();
                } else {
                    cancelAnimationFrame(globeAnimId);
                }
            });
        },
        { threshold: 0.1 },
    );
    globeObserver.observe(canvas);
}
