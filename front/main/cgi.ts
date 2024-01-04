/*
 * Computer Generated Images
 * Copyright (C) 2023 Jonathan Tremesaygues
 *
 * cgi.ts
 *
 * This program is free software: you can redistribute it and/or modify it under
 * the terms of the GNU General Public License as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option) any later
 * version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with
 * this program. If not, see <https://www.gnu.org/licenses/>.
 */

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
