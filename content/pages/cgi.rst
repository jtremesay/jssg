---
title: Images générés par ordinateur
slug: cgi
---

Quelques expérimentations avec la création d'images par ordinateur.

Triangle de Sierpinski
======================

Ici, un `triangle de Sierpinski <https://fr.wikipedia.org/wiki/Triangle_de_Sierpi%C5%84ski>`_ généré dans une image SVG avec du vanilla typescript.

.. raw:: html

    <script src="/static/gen/cgi.js" type="module"></script>
    <p>
        <label>
            Récursion
            <input id="sierpinski-input" type="range" min="0" max="7" value="1">
        </label>
    </p>
    <svg class="sierpinski" data-sierpinski-input="sierpinski-input" version="1.1" width="400" height="400" viewBox="0 0 1 1" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="black" />
    </svg>


.. code-block:: typescript

    function create_triangles(deep: number) {
        if (deep == 0) {
            const path = document.createElementNS("http://www.w3.org/2000/svg", "path")
            path.setAttribute("d", `M 0.5,0L${0.5 - Math.sin(Math.PI / 3) / 2},0.75 ${0.5 + Math.sin(Math.PI / 3) / 2},0.75Z`)
            path.setAttribute("fill", "yellow")
            path.classList.add("triangle")
            return path
        }

        const g = document.createElementNS("http://www.w3.org/2000/svg", "g")
        g.classList.add("triangle")

        const triangle_a = create_triangles(deep - 1)
        triangle_a.setAttribute("transform", `scale(0.5, 0.5) translate(0.5, 0)`)
        g.appendChild(triangle_a)

        const triangle_b = create_triangles(deep - 1)
        triangle_b.setAttribute("transform", `scale(0.5, 0.5) translate(${0.5 - Math.sin(Math.PI / 3) / 2}, 0.75)`)
        g.appendChild(triangle_b)

        const triangle_c = create_triangles(deep - 1)
        triangle_c.setAttribute("transform", `scale(0.5, 0.5) translate(${0.5 + Math.sin(Math.PI / 3) / 2}, 0.75)`)
        g.appendChild(triangle_c)

        return g
    }

    function sierpinski(svg: SVGElement) {
        const input = document.getElementById(svg.dataset.sierpinskiInput ?? "sierpinski-input") as HTMLInputElement
        if (input !== null) {
            input.addEventListener("input", (event) => {
                svg.querySelectorAll(".triangle").forEach((triangles) => triangles.remove())
                svg.appendChild(create_triangles(parseInt((event.target as HTMLInputElement).value)))
            })
            svg.appendChild(create_triangles(parseInt(input.value)))
        } else {
            svg.appendChild(create_triangles(1))
        }
    }

    document.querySelectorAll("svg.sierpinski").forEach((svg) => sierpinski(svg as SVGElement))